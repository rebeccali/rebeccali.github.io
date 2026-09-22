# rebecca.li

Single-page personal site. Jekyll on GitHub Pages, served from `master` at the apex
domain `rebecca.li` (see `CNAME`).

## Structure

```
index.html            Home: bio, where I've worked, contact.
cv.html               Full CV at /cv/ — experience, education, publications,
                      projects, skills.
_data/orgs.yml        Logo registry: one entry per company or org.
_includes/logo.html   Renders an org's logo, or a lettermark if it has no file.
assets/img/logos/     Square logo files, 128x128.
_layouts/default.html Bare HTML shell.
_includes/head.html   Meta tags, OG/Twitter cards, stylesheet link.
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

The CV is authored in LaTeX in a separate repo (`rmli_resume_letters/resume/`).
After rebuilding the PDF there, copy it in and point `cv:` in `_config.yml` at
the new filename:

```sh
cp ../rmli_resume_letters/resume/<new>.pdf assets/cv-rebecca-li-<yyyy-mm>.pdf
```

`cv.html` is a fleshed-out superset of the PDF and is maintained by hand.

## Deploying

GitHub Pages builds from `master`. Merge and push.
