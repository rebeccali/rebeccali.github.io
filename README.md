# rebecca.li

Single-page personal site. Jekyll on GitHub Pages, served from `master` at the apex
domain `rebecca.li` (see `CNAME`).

## Structure

Text and layout are kept apart: everything you would want to *edit* — prose,
job titles, dates, publications, links — lives in `_data/*.yml`, and the `.html`
files are loops over it.

```
_data/profile.yml     Name, tagline, meta description, portrait, every link,
                      and the CV PDF path.
_data/home.yml        Home page: bio paragraphs, the "where I've worked" list,
                      the contact block.
_data/cv.yml          CV page content. GENERATED from the resume - see below.
_data/cv_page.yml     CV page furniture: title, headings, nav labels.
_data/orgs.yml        Logo registry: one entry per company or org, shared by
                      the home page and the CV.

index.html            Home page template. Loops over _data/home.yml.
cv.html               CV template at /cv/. Loops over _data/cv.yml.
_layouts/default.html Bare HTML shell.
_includes/head.html   Meta tags, OG/Twitter cards, stylesheet link.
_includes/entry.html  One CV entry: logo, title, role, dates, prose.
_includes/authors.html  An author list, with my name bolded.
_includes/links.html  A <ul> of links, chosen by key from profile.yml.
_includes/logo.html   An org's logo, or a lettermark if it has no file.
_includes/footer.html The copyright line.

_resume/resume.tex    The resume, in LaTeX. Source of truth for the CV.
_scripts/build_cv.py  Reads the resume, writes _data/cv.yml.

assets/img/logos/     Square logo files, 128x128.
assets/css/site.css   The stylesheet. Hand-written, no build step.
assets/cv-*.pdf       CV, copied in from the resume repo (see below).
_archive/             Retired blog posts. Not built, not published.
photography/          Pre-generated gallery HTML from the old site. Still live at
                      /photography/<gallery>/, deliberately unlinked from the site.
img/                  Images for the archived posts.
assets/css/main.css   Legacy stylesheets. The photography galleries load these.
assets/css/gallery.css  Do not delete.
assets/fonts/font-awesome/  Ditto — the galleries reference it.
```

`_config.yml` holds build settings only. One practical consequence: edits to
`_data/` show up on the next page load under `jekyll serve`, while edits to
`_config.yml` need the server restarted.

## Editing the content

Each data file starts with a comment explaining its own shape; the short version:

- **Change a job title, date or paragraph** — find it in `_data/home.yml` (home
  page) or `_data/cv.yml` (CV) and edit the string. Prose fields accept inline
  HTML, so a `<a href="...">link</a>` in the middle of a sentence is fine.
- **Change anything on the CV** — edit `_resume/resume.tex` and re-run the
  build script. `_data/cv.yml` is generated; edits to it are overwritten.
- **Change an email address or profile link** — `links:` in
  `_data/profile.yml`, once, for every page that uses it.
- **Take down the "currently looking" callout** — delete the `availability:`
  key in `_data/home.yml` and the paragraph disappears.

## Local development

**Requires Ruby 3.3.** Not Ruby 4, and not macOS system Ruby.

```sh
brew install ruby@3.3                          # once
export PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH"   # every new shell

bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>.

To avoid retyping the `export`, add this to `~/.zshrc`:

```sh
serve-site() {
  PATH="/opt/homebrew/opt/ruby@3.3/bin:$PATH" bundle exec jekyll serve "$@"
}
```

There is no CSS build step — `assets/css/site.css` is edited directly.

### Why the Ruby version matters

Two separate traps, both of which produce confusing errors:

**`bundle` and `ruby` come from different installs.** Homebrew symlinks `ruby`
into `/opt/homebrew/bin` but deliberately does *not* symlink `bundle`, because it
would collide with the one Apple ships. So on a default PATH, `ruby` is Homebrew
Ruby 4 while `bundle` is system Ruby 2.6's — and 2.6's bundler cannot read a
lockfile written by bundler 4:

```
Could not find 'bundler' (4.0.16) required by your Gemfile.lock
```

Don't `gem install bundler:4.0.16` to chase this; it installs the gem into the
wrong Ruby. Put a real Ruby's `bin` directory first on PATH instead — those
directories *do* contain `bundle`.

**Ruby 4 can't build the dependencies.** The `github-pages` gem pins an old
dependency tree that includes `rdiscount`, whose native extension fails to
compile on Ruby 4.0:

```
An error occurred while installing rdiscount (2.1.7), and Bundler cannot continue.
```

Ruby 3.3 is the newest version that works. If GitHub Pages ever drops
`github-pages` in favour of plain `jekyll`, this constraint goes away.

Check which you're actually using with `ruby -v && bundle -v` — both should come
from `ruby@3.3`, and `bundle -v` should report 4.x.

## Adding a logo

Logos live in `assets/img/logos/` and are wired up in `_data/orgs.yml`. An org
with no `logo:` line falls back to a coloured lettermark, so the page is never
broken by a missing file.

To add one: drop a square PNG or SVG (128x128, transparent background) into
`assets/img/logos/`, then add the filename to that org in `_data/orgs.yml`:

```yaml
cfs:
  name: Commonwealth Fusion Systems
  url: https://cfs.energy
  logo: cfs.png     # add this line; `mono` and `tint` are then ignored
```

Nothing else changes — both the home page and the CV pick it up.

Square-ish source images work best. A wide wordmark lockup shrinks to
illegibility inside the tile, so crop the `viewBox` (or the bitmap) down to
the mark and drop the lettering.

Two things to watch with SVGs, since they are loaded through `<img>` and so
render in isolation from the page:

- `fill="currentColor"` resolves to black, not the surrounding text colour.
  Replace it with an explicit hex — the brand colour where you know it.
- Anything styled by an external class (`class="path-vs-black"` and the like)
  arrives unstyled. Same fix: set `fill` on the path.

## Updating the CV

`_resume/resume.tex` is the source of truth for both the PDF and the `/cv/`
page. Edit it, then rebuild both:

```sh
cd _resume && latexmk -pdf resume.tex        # the PDF
cd .. && python3 _scripts/build_cv.py        # _data/cv.yml, which /cv/ renders
```

To publish a new PDF, copy it into `assets/` and point `links.cv.url` in
`_data/profile.yml` at the new filename:

```sh
cp _resume/resume.pdf assets/cv-rebecca-li-<yyyy-mm>.pdf
```

`python3 _scripts/build_cv.py --check` exits non-zero when `_data/cv.yml` is
out of date, which is the thing to run before pushing if you have edited the
resume.

### How the parser sees the resume

The script reads the semantic macros defined in the resume preamble, grouped
by the `\section` they sit under:

| macro | arguments |
| --- | --- |
| `\resumeEducation` | degree, location, dates |
| `\resumeJob` | organisation, role, location, dates, description |
| `\resumePublication` | authors, title, url (may be empty), venue, year |
| `\resumeSkill` | group, items |
| `\resumeLeadership` | one line of text |

Everything else in the file is invisible to the website, including anything
below `\end{document}`, which is where retired sections are parked.

Two tables in `_scripts/build_cv.py` connect the resume to the site:

- `SECTIONS` — one row per `\section`, giving its anchor id, its nav label and
  which macro to read. A section that is not listed is an error, so a new one
  cannot quietly go missing from the site.
- `ORG_KEYS` — which logo in `_data/orgs.yml` belongs to an entry, matched as a
  substring of the organisation or degree. An entry that matches nothing is an
  error rather than a silently logo-less row.

Inline LaTeX is converted as you would expect: `\href` becomes a link,
`\textbf` and `\textit` become `<strong>` and `<em>`, `--` becomes an en
dash, `\CC` becomes C++, and unknown macros are dropped.

### Editing the resume without breaking the PDF

The layout is whitespace-sensitive in two places, both marked with comments:

- A blank line inside a list environment is a paragraph break and changes the
  spacing. Use a comment-only `%` line to separate entries in the source.
- `\resumeSubheadingCleanLong` ends with two deliberate blank lines. They set
  the gap between employment entries.

## Deploying

GitHub Pages builds from `master`. Merge and push.


## Inspirations
- https://zekehausfather.com/
- https://amymakesstuff.com/
- https://isopack.blogspot.com/
