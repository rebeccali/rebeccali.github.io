# rebecca.li

Single-page personal site. Jekyll on GitHub Pages, served from `master` at the apex
domain `rebecca.li` (see `CNAME`).

## Structure

```
index.html            The entire site. Content lives here, inline.
_layouts/default.html Bare HTML shell.
_includes/head.html   Meta tags, OG/Twitter cards, stylesheet link.
assets/css/site.css   The stylesheet. Hand-written, no build step.
assets/resume-*.pdf   Resume, copied in from the resume repo (see below).
_archive/             Retired blog posts. Not built, not published.
photography/          Pre-generated gallery HTML from the old site. Still live at
                      /photography/<gallery>/, deliberately unlinked from the site.
img/                  Images for the archived posts.
assets/css/main.css   Legacy stylesheets. The photography galleries load these.
assets/css/gallery.css  Do not delete.
assets/fonts/font-awesome/  Ditto — the galleries reference it.
```

## Local development

Needs Ruby (3.x) and Bundler.

```sh
bundle install
bundle exec jekyll serve
```

Then open <http://localhost:4000>.

There is no CSS build step — `assets/css/site.css` is edited directly.

## Updating the resume

The resume is authored in LaTeX in a separate repo
(`rmli_resume_letters/resume/`). After rebuilding the PDF there, copy it in and
point `resume:` in `_config.yml` at the new filename:

```sh
cp ../rmli_resume_letters/resume/<new>.pdf assets/resume-rebecca-li-<yyyy-mm>.pdf
```

The on-page Experience section is a fleshed-out superset of the PDF and is
maintained by hand in `index.html`.

## Deploying

GitHub Pages builds from `master`. Merge and push.
