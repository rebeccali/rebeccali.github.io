---
title: OpenSCAD GEB-Inspired Block
date: 2015-12-11 00:00:00 Z
tags:
- projects
- art
layout: post
img: lovehaterender.png
---

This is a block that I made with [OpenSCAD, a code-based 3D solid modeler][openscad]. The block is two words - love and hate - on different sides of the block such that you can only read one from any given side. The first version I made was in Rhino and promptly lost to a spontaneous system wipe. The new version is all parametric, woo~

![ABC XYZ block]({{ site.baseurl }}/img/lovehatecompiulation.png) <small>Block with dual words</small>

[OpenSCAD][openscad] uses a set of primitive shapes (cubes, spheres) and boolean operations (union, difference, intersection) in order to make a complex shape. For this model, [OpenSCAD][openscad] has an additional font primitive which this model takes advantage of. It is the intersection of "LOVE" and "HATE" rotated about the same axes. The basic code is below:

	font = "Consolas:style=Bold";

	intersection() {
	    rotate(90, [1, 0, 0])   linear_extrude(height=1) text("LOVE", font = font, size = 1, spacing=.7);
	    translate ([0,-1, 0])   linear_extrude(height=1) text("HATE", font = font, size = 1, spacing=.7);
	}


It was inspired by the Godel Escher Bach book cover, which is a book written a little too much in a Malcolm Gladwell-esque style for me to read past the first few pages. Maybe one day I will go read it and not have this opinion.

![Godel Escher Bach]({{ site.baseurl}}/img/geb.jpg)<small>Godel Escher Bach Cover ([Source][geb])</small>

You can find all my strange OpenSCAD projects on my [Github repo][openscadrepo].


[jekyll]:      http://jekyllrb.com
[jekyll-gh]:   https://github.com/jekyll/jekyll
[jekyll-help]: https://github.com/jekyll/jekyll-help
[githubpages]: https://pages.github.com/
[mywebsite]:   https://github.com/rebeccali/holo-alfa/
[holoalfa]:    https://github.com/steinvc/holo-alfa
[ppprs]:       http://www.powerracingseries.org/
[dvr]:    	   http://www.ti.com/product/drv8302
[chainsawfet]: http://www.nxp.com/documents/data_sheet/PSMN7R0-100PS.pdf
[bayley]:      http://isopack.blogspot.com
[ninephase]:   https://github.com/rebeccali/ninephase
[openscad]:    http://www.openscad.org/
[geb]:         https://books.google.com/books/about/G%C3%B6del_Escher_Bach_Anniversary_Edition.html?id=aFcsnUEewLkC&source=kp_cover
[openscadrepo]:https://github.com/rebeccali/openscad
