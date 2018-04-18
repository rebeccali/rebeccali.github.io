---
title: Frozen Chainsaw Massacre
date: 2015-12-14 00:00:00 Z
tags:
- projects
layout: post
img: covers/landon-anvita-2015-nym.jpg
---

The summer comes with wonderful joys. Ice cream, air conditioning, free time, and go-karts. Last summer I played pit crew for [Charles Guan's Chibi Mikuvan](http://www.etotheipiplusone.net/?cat=112).

It was a super fun trip, going out to Detroit, seeing all of the Makerfaire shenanigans, and also seeing Charles' great work in turning hobby RC parts into a fearsome go-kart.

He and many other MITERSans do a great job of re-purposing batteries, power tools, junk, anything into a work of art.

![picture of chibimikuvan here]({{ site.baseurl }}/img/chibi-on-van.jpg) <small>Chibi Mikuvan: the most Adorable little van, on top of its mothership. Source: www.etotheipiplusone.net</small>

It was so adorable and so fast that it made me want to make my own. The competition, [PowerWheels Racing][ppprs] dictates a few rules:

* Go-kart must be built for under $500. Safety devices (brakes, etc.) are counted at no costs, and batteries are counted at half cost.
* Go-kart must be able to brake
* Electrical system must be within power limit (for us, 40V, 40A)

### The Mechanical Monster: Frozen Chainsaw Massacre ###
With these in mind, and a few friends, over the summer we constructed a monstrosity made out of Ryobi Chainsaws and steel tube left over in [D-Lab][dlab]. The end result was **Frozen Chainsaw Massacre (FCM)**. We ended up making the majority of the cart out of steel tube, with the front knuckles and back chainsaw mounts out of 1/4" mild steel plate. The 1/4" plate ended up being a huge problem for the go-kart. Bent steering and bent chainsaw mounts were our most dire problems when we raced at MakerFaire New York. The other major flaw of the mechanical system was using a 12-tooth 5mm HTD pulley. This pulley had only enough material on the inside to fit over the motor with 2mm to spare and set screw through. In the end, we ended up building up the pulley with weld so there would actually be enough area to set screw. A lack of idler and poor chainsaw mounting also led to de-tensioning of the belt being a frequent occurrence.

![Cad model]({{ site.baseurl }}/img/fcm-cad.JPG) <small>Barely enough CAD is still barely enough</small>

The happy part of FCM was that it had kingpin and ackerman steering correction, making the cart steer properly. It also had the added feature of being incredibly hard to turn, because of the cart's natural drift towards center. We briefly considered adding powered steering.

![Ackerman Steering]({{ site.baseurl }}/img/ackerman.gif) <small>Ackerman Steering correction</small>

In spite of mechanical problems, the cart was blazing fast, placing first every time it qualified over veteran carts. The secret sauce? *Dithering*.

## WTFudge is Dithering? ##

*Dithering*, mis amigos, is essentially "fuse cheating". The basic principle, developed and implemented by [Bayley][bayley] is to sense the fuse temperature, and "dither" the current in response. For example, if the fuse gets hot under 90A, the kart will pull back to 40A until the fuse is cold again. Likewise, it monitors the chainsaw motors, and dithers off of those as well. This allowed us to cheat the fuse, running more than 50A and getting as good acceleration as our belts would allow.

![The finished FCM]({{ site.baseurl }}/img/fcm-2015-nymf.jpg) <small>The Finished Frozen Chainsaw Massacre</small>

## Future Improvements ##

At both Detroit Makerfaire 2015 and New York Makerfaire 2015, while FCM started as the fastest part, reliability was so questionable that we never finished a race except for the New York Endurance (what). Here's how I would go about improving reliability for next year:

* Enclosed Ditherer box and better wiring solution
* Sharper turning radius and non-cheese steering linkages
* Billet Motor mounts instead of chainsaw bodies
* Belt Idler
* Remaking Pillow block mount to sit on bottom for better clearance
* Remake keyways
* More fan cooling on motors

## Technical Summary ##

* 9:1 Gear Ratio
* Tires: [Kenda Tire 9X3.50-4 with K372 Tread Pattern](http://www.scooterpartscatalog.com/kenda-k372-tire-154-90.html) with Harbor Freight 8" Hubs
* Frame: TIG welded steel tube
* Motor: 2x[Ryobi Brushless 40V Chainsaw](http://www.homedepot.com/p/Ryobi-14-in-40-Volt-Brushless-Cordless-Chainsaw-Battery-and-Charger-Not-Included-RY40502A/204839368?cm_mmc=Shopping%7cTHD%7cG%7c0%7cG-BASE-PLA%7c&gclid=Cj0KEQiA7rmzBRDezri2r6bz1qYBEiQAg-YEtvLsCF3aoW2Nehfu0gBoMI5JGVxdZVj_5s766MKmWq0aAgR28P8HAQ&gclsrc=aw.ds)
* Motor controller: Stock Chainsaw with [custom firmware](http://isopack.blogspot.com/2014/10/frozen-chainsaw-massacre-part-2-new.html)
* Batteries: LiFePO4 12S4P A123 26650 cells, 40V 9.4Ah
* Throttle: Scooter thumb throttle
* Switch: [Hella](http://www.amazon.com/HELLA-002843011-Series-Rating-Battery/dp/B0000AYAFE)
* Top Speed: 28 mile per hour


[anchorcms]:   https://anchorcms.com/
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
[dlab]:        dsdd