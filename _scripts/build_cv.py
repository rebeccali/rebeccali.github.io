#!/usr/bin/env python3
"""Build _data/cv.yml from the LaTeX résumé.

_resume/resume.tex is the source of truth for CV content. This script reads
the semantic macros defined there — \\resumeEducation, \\resumeJob,
\\resumePublication, \\resumeSkill, \\resumeLeadership — grouped by the
\\section they sit under, and writes the YAML that /cv/ renders from.

What this script does NOT own:

  _data/cv_page.yml   page furniture: title, headings, nav labels, section
                      ids. Hand-written, never overwritten.
  _data/orgs.yml      logos. Entries are linked to it through ORG_KEYS below.

Anything in the résumé below \\end{document} is ignored, as it is by LaTeX.

Usage:
    python3 _scripts/build_cv.py            rewrite _data/cv.yml
    python3 _scripts/build_cv.py --check    exit 1 if it would change
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEX = ROOT / "_resume" / "resume.tex"
OUT = ROOT / "_data" / "cv.yml"

# Which logo in _data/orgs.yml belongs to an entry. Matched as a substring of
# the entry's organisation (jobs) or degree line (education); the longest match
# wins, so "MIT Media Lab" beats "MIT". An entry that matches nothing is an
# error rather than a silently logo-less row.
ORG_KEYS = {
    "Commonwealth Fusion Systems": "cfs",
    "Vicarious Surgical": "vicarious",
    "DeepMind": "deepmind",
    "University of Pennsylvania, GRASP Lab": "grasp",
    "Kitty Hawk Corp": "kittyhawk",
    "MIT Media Lab": "medialab",
    "University of Pennsylvania": "upenn",
    "MIT": "mit",
}

# One row per \section in the résumé, in résumé order:
#
#   anchor  the /cv/#... id. Changing one breaks any existing link to it.
#   nav     label for the nav strip, when the heading is too long for it.
#   kind    how to read the entries underneath.
#
# A \section that is not listed here is an error, so a new résumé section
# cannot quietly go missing from the website.
SECTIONS = {
    "Education":                       ("education",    None,           "education"),
    "Employment":                      ("experience",   None,           "jobs"),
    "Selected Publications & Patents": ("publications", "Publications", "publications"),
    "Skills":                          ("skills",       None,           "skills"),
    "Leadership":                      ("leadership",   None,           "bullets"),
}


# --------------------------------------------------------------------------
# LaTeX reading
# --------------------------------------------------------------------------

def strip_comments(tex: str) -> str:
    """Drop % comments, keeping \\% escapes."""
    out = []
    for line in tex.splitlines():
        cut = None
        for i, ch in enumerate(line):
            if ch == "%" and (i == 0 or line[i - 1] != "\\"):
                cut = i
                break
        out.append(line if cut is None else line[:cut])
    return "\n".join(out)


def read_group(s: str, i: int) -> tuple[str, int]:
    """Read one balanced {...} starting at or after index i."""
    while i < len(s) and s[i].isspace():
        i += 1
    if i >= len(s) or s[i] != "{":
        raise ValueError(f"expected '{{' at {i}: {s[i:i + 40]!r}")
    depth, start = 0, i
    while i < len(s):
        if s[i] == "\\":
            i += 2
            continue
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[start + 1:i], i + 1
        i += 1
    raise ValueError(f"unbalanced braces from {start}")


def macro_calls(tex: str, name: str, nargs: int) -> list[list[str]]:
    """Every \\name{...}{...} in source order, as lists of raw arguments."""
    calls = []
    for m in re.finditer(r"\\" + name + r"(?![a-zA-Z])", tex):
        i = m.end()
        args = []
        for _ in range(nargs):
            arg, i = read_group(tex, i)
            args.append(arg)
        calls.append(args)
    return calls


# --------------------------------------------------------------------------
# LaTeX -> HTML
# --------------------------------------------------------------------------

ESCAPES = {"&": "&amp;", "<": "&lt;", ">": "&gt;"}
SYMBOLS = {r"\CC": "C++", r"\LaTeX": "LaTeX", r"\TeX": "TeX", r"\ldots": "…"}
WRAPPERS = {"textbf": "strong", "textit": "em", "emph": "em", "textsc": None,
            "mbox": None, "small": None, "makecell": None}


def esc(text: str) -> str:
    return "".join(ESCAPES.get(c, c) for c in text)


def to_html(s: str) -> str:
    """Convert résumé LaTeX to the inline HTML the site renders."""
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch != "\\":
            out.append(esc(ch))
            i += 1
            continue
        m = re.match(r"\\([a-zA-Z]+)", s[i:])
        if not m:                                   # \& \% \_ \$ \# \\ ...
            nxt = s[i + 1] if i + 1 < len(s) else ""
            out.append(" " if nxt == "\\" else esc(nxt))
            i += 2
            continue
        name, j = m.group(1), i + m.end()
        token = "\\" + name
        if token in SYMBOLS:
            out.append(SYMBOLS[token])
            i = j
            continue
        if name == "href":
            url, j = read_group(s, j)
            label, j = read_group(s, j)
            out.append(f'<a href="{esc(to_text(url))}">{to_html(label)}</a>')
            i = j
            continue
        if name in WRAPPERS:
            inner, j = read_group(s, j)
            tag = WRAPPERS[name]
            body = to_html(inner)
            out.append(f"<{tag}>{body}</{tag}>" if tag else body)
            i = j
            continue
        i = j                                       # unknown macro: drop it
    text = "".join(out)
    text = text.replace("---", "—").replace("--", "–").replace("~", " ")
    return re.sub(r"\s+", " ", text).strip()


def to_text(s: str) -> str:
    """Same, but without markup — for URLs and author names."""
    return re.sub(r"<[^>]+>", "", to_html(s))


# --------------------------------------------------------------------------
# Entry builders
# --------------------------------------------------------------------------

def org_key(label: str) -> str:
    matches = [(len(k), v) for k, v in ORG_KEYS.items() if k in label]
    if not matches:
        sys.exit(f"error: no logo mapping for {label!r}.\n"
                 f"       Add it to ORG_KEYS in {Path(__file__).name} "
                 f"and to _data/orgs.yml.")
    return max(matches)[1]


def build_education(body: str) -> list[dict]:
    entries = []
    for degree, location, dates in macro_calls(body, "resumeEducation", 3):
        title = to_html(degree)
        entries.append({"org": org_key(to_text(degree)), "title": title,
                        "meta": to_html(location), "when": to_html(dates)})
    return entries


def build_jobs(body: str) -> list[dict]:
    entries = []
    for org, role, location, dates, desc in macro_calls(body, "resumeJob", 5):
        entries.append({"org": org_key(to_text(org)), "title": to_html(org),
                        "role": to_html(role), "meta": to_html(location),
                        "when": to_html(dates), "body": to_html(desc)})
    return entries


def split_authors(raw: str) -> list[str]:
    """'A, B, C and D,' -> ['A', 'B', 'C', 'D']."""
    text = to_text(raw).strip().rstrip(",")
    names = []
    for chunk in text.split(", "):
        names.extend(p.strip() for p in re.split(r"\s+and\s+", chunk))
    out = []
    for name in names:
        name = name.strip().rstrip(",")
        if re.fullmatch(r"et\s+al\.?", name):
            name = "et al."                  # the site keys the join on this
        else:
            name = name.rstrip("*")          # equal-contribution mark: no legend on the page
        if name:
            out.append(name)
    return out


def build_publications(body: str) -> list[dict]:
    entries = []
    for authors, title, url, venue, year in macro_calls(body, "resumePublication", 5):
        entry = {"authors": split_authors(authors), "title": to_html(title),
                 "venue": to_html(venue), "year": to_html(year)}
        if url.strip():
            entry["url"] = to_text(url)
        entries.append(entry)
    return entries


def build_skills(body: str) -> list[dict]:
    return [{"term": to_html(term), "detail": to_html(detail)}
            for term, detail in macro_calls(body, "resumeSkill", 2)]


def build_bullets(body: str) -> list[str]:
    return [to_html(line) for (line,) in macro_calls(body, "resumeLeadership", 1)]


BUILDERS = {"education": ("entries", build_education),
            "jobs": ("entries", build_jobs),
            "publications": ("entries", build_publications),
            "skills": ("groups", build_skills),
            "bullets": ("items", build_bullets)}

# What the site template calls each kind.
SITE_TYPES = {"education": "entries", "jobs": "entries",
              "publications": "publications", "skills": "skills",
              "bullets": "bullets"}


def parse(tex: str) -> list[dict]:
    tex = strip_comments(tex)
    tex = tex.split(r"\end{document}")[0]
    chunks = re.split(r"\\section\{((?:[^{}]|\\.)*)\}", tex)[1:]
    sections = []
    for heading_raw, body in zip(chunks[::2], chunks[1::2]):
        heading = to_html(heading_raw)
        meta = SECTIONS.get(html.unescape(heading))
        if meta is None:
            sys.exit(f"error: unknown résumé section {heading!r}.\n"
                     f"       Add it to SECTIONS in {Path(__file__).name}.")
        anchor, nav, kind = meta
        field, builder = BUILDERS[kind]
        section = {"id": anchor, "heading": heading}
        if nav:
            section["nav"] = nav
        section["type"] = SITE_TYPES[kind]
        section[field] = builder(body)
        sections.append(section)
    return sections


# --------------------------------------------------------------------------
# YAML output
# --------------------------------------------------------------------------

PLAIN_OK = re.compile(r"^[A-Za-z][^:#\n]*$")
WIDTH = 96


def quoted(text: str) -> str:
    """The shortest safe single-line form of a scalar."""
    if PLAIN_OK.match(text) and ": " not in text and " #" not in text:
        return text
    return "'" + text.replace("'", "''") + "'"


def flow(items: list[str]) -> str:
    return "[" + ", ".join(
        i if re.fullmatch(r"[A-Za-z][\w .-]*", i) else "'" + i.replace("'", "''") + "'"
        for i in items) + "]"


def emit_scalar(prefix: str, value, indent: int) -> list[str]:
    """`prefix` is "key:" or "-"; folds only when a single line will not fit."""
    text = str(value)
    line = f"{' ' * indent}{prefix} {quoted(text)}"
    if len(line) <= WIDTH or " " not in text:
        return [line]
    pad = " " * (indent + 2)
    wrapped = textwrap.wrap(text, width=WIDTH - len(pad),
                            break_long_words=False, break_on_hyphens=False)
    return [f"{' ' * indent}{prefix} >-"] + [pad + w for w in wrapped]


def emit(node, indent: int = 0) -> list[str]:
    pad = " " * indent
    lines = []
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, list) and value and all(
                    isinstance(v, str) for v in value):
                one = f"{pad}{key}: {flow(value)}"
                if len(one) <= WIDTH:
                    lines.append(one)
                    continue
            if isinstance(value, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.extend(emit(value, indent + 2))
            else:
                lines.extend(emit_scalar(f"{key}:", value, indent))
    elif isinstance(node, list):
        for item in node:
            if isinstance(item, dict):
                inner = emit(item, indent + 2)
                lines.append(f"{pad}- {inner[0].lstrip()}")
                lines.extend(inner[1:])
            else:
                lines.extend(emit_scalar("-", item, indent))
    return lines


HEADER = f"""\
# GENERATED FILE - do not edit.
#
# Built from {TEX.relative_to(ROOT)} by {Path(__file__).relative_to(ROOT)}.
# Edit the résumé and re-run:
#
#     python3 {Path(__file__).relative_to(ROOT)}
#
# Page furniture (title, nav labels, section ids) lives in _data/cv_page.yml,
# which this script never touches.
"""


def render(sections) -> str:
    return HEADER + "\n" + "\n".join(emit({"sections": sections})) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the generated file is out of date")
    args = ap.parse_args()

    sections = parse(TEX.read_text(encoding="utf-8"))
    text = render(sections)

    if args.check:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print(f"{OUT.relative_to(ROOT)} is out of date - run "
                  f"python3 {Path(__file__).relative_to(ROOT)}")
            return 1
        print(f"{OUT.relative_to(ROOT)} is up to date")
        return 0

    OUT.write_text(text, encoding="utf-8")
    counts = ", ".join(
        f"{len(s.get('entries') or s.get('groups') or s.get('items'))} {s['heading'].lower()}"
        for s in sections)
    print(f"wrote {OUT.relative_to(ROOT)}: {counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
