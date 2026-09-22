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
