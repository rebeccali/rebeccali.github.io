# Flexible-Jekyll is a simple and clean theme for Jekyll

Now appropriated by rebecca li

## Features

- [Google Fonts](https://fonts.google.com/)
- [Font Awesome](http://fontawesome.io/)
- [Disqus](https://disqus.com/)
- [Analytics](https://analytics.google.com/analytics/web/)
- Support Emoji

## Installation:
Run `sudo bash setup_scripts/install_all.sh`

Now, run the following:

```
bundle exec jekyll build
bundle exec jekyll serve
```

If you update the galleries, then right now it kind of sucks and you should copy over the photography folder from `_site` to the top level and commit it. You also have to update the `_config.yml`.

```
bundle exec jekyll build
cp -r _site/photography/* photography/
```

## Todo

* Add About Page
* Add Photography Page
* Fix Image widths
* Add Portfolio Page

### License

GNU General Public License v3.0
