# Holo Alfa Jekyll theme [![Build Status](https://travis-ci.org/steinvc/holo-alfa.svg?branch=master)](https://travis-ci.org/steinvc/holo-alfa) #

TO SELF:

# How to serve and deploy #

Things you need to install are ruby, bundler, and jekyll.

To work locally, go to the holo-alfa folder and run "bundle exec jekyll serve" which will serve to localhost:4000. In _config.yml, url must be ""

To deploy, deploy to the rebeccali.github.io repository by first changing url in _config.yml to http://rebecca.li/. Then run "bundle exec jekyll build --destination ../rebeccali.github.io" then push to the internet. 

![Screenshot](http://i.imgur.com/Gi46aag.jpg)

Holo Alfa is a minimalist, mobile first Jekyll theme with focus on readability and content. Created for free and fun by Stijn.

See it in action: http://steinvc.github.io/holo-alfa/.

## Feature highlights ##

* Mobile first design
* Extensive content styling
* Responsive video's (using [FitVids.JS](http://fitvidsjs.com/))
* Support for authors and guest authors
* Read time on articles
* Disqus comments
* Automatic [og metadata](http://ogp.me/)
* Automatic archive page (without plugins)
* Automatic sitemap en RSS feed
* Contact page (with working email form)
* A lot of (optional) customization options (all in `_config.yml`)

And much more.

## Getting started ##

If you're new to Jekyll, check out http://jekyllrb.com/ and read up on Jekyll. It's worth it.

* [Another great resource to learn about Jekyll](http://www.smashingmagazine.com/2014/08/build-blog-jekyll-github-pages/)
* [Github's guide to using Jekyll with Pages](https://help.github.com/articles/using-jekyll-with-pages/)

If you run one of the latest versions of Jekyll, this theme will work with no* problems.

### Installing ##

As simple as forking the repository, and then clone it so you can edit the files locally.

### Configuration ###

Edit `_config.yml`!

You can find `_config.yml` in your site's root directory. This configuration file contains some necessary settings and some optional customization settings. **All settings are explained in `_config.yml` itself.**

There are some customizations that can't be done in `_config.yml`. These include:

* Editing the About, Contact and Archive page.
* Adding or removing pages from the navigation. This can be done in `\_includes\navigation.html`.
* The "thanks" page after a message has been send through the contact page: `thanks.md`
* The gradient on cover images: `\_includes\gradient.css` (this is explained in `_config.yml`).

Also make sure to replace the placeholder favicons and the `\img\og-image.jpg` with your own.

### Start the Jekyll server ###

Run this command at the root of your site:

```
$ jekyll serve
```

> To run Jekyll in a way that matches the GitHub Pages build server, run Jekyll with Bundler. Use the command `bundle exec jekyll serve`.

When everything is OK, your site should now be available at `http://localhost:4000`.

That's it.

---

[MIT license](http://opensource.org/licenses/MIT)