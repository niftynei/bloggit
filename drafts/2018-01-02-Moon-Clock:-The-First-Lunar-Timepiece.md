timestamp: 1514935581
date: 2 Jan 2018
time: 15:26
title: Introducing the Moon Clock, The World's First Wall-Mounted Lunar Timepiece
tags: moon-clock, projects, lunar-timepiece, astronomy

---
## The Moon Clock Project

![MoonClock](/img/moon_desk.jpg)

I spent the last half of 2017 working on a project that I'm calling a Moon Clock, a physical lunar timepiece that displays what the moon looks like for your current location.  Apparently the moon is a trendy thing these days.[0]

I got the idea when decorating a new bedroom; the walls needed something that went with my celestial themed room and I already had a 'normal' clock.  Why not make a lunar clock?


## Making a Moon Clock

The moon clock is a simple, backlit screen print of the moon, illuminated to show what the moon looks like at your location.  It's mounted in a frame and when hung looks like a backlit moon portrait.

I went through a few ideas of using mechanical  moving screens to get the moon shadow, but ultimately settled on using an LED display that lights up a printed moon screen.  

The prototype I've built uses an LED matrix, a RaspberryPi and the corresponding Adafruit HAT (for driving the LED).  You can see how to set up an LED project for yourself via this [Adafruit tutorial](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi).  Note that the underlying Gihub project that Adafruit uses as a driver is super out of date; the updated version of the original project now includes instructions for how to use it with the Adafruit HAT. I recommend using the updated driver [version](https://github.com/hzeller/rpi-rgb-led-matrix).

The moon clocks is simply this Adafruit LED project mounted in a shadowbox, with a screen mounted at the front.



### Lunar Tracking

Getting the LED set up was fairly trivial; however the astronomical algorithms required to calculate the moon phase given a latitude, longitude and time turned out to be non-trivial. The book [Astronomical Algorithms](http://www.willbell.com/math/mc1.htm) by astronomer Jean Meeus is generally considered to be the gold standard in computational astronomy, but as a layman I found the astronomical jargon to be largely unintelligible.

I spent a good amount of time figuring out exactly what the information was called, and more time yet figuring out how to use the collection of algorithms presented in Meeus' book to compute the values I was looking for.

The problem lay mostly in that the exact information I need (percent illimination and position angle of the bright limb, or in other words, rotation of the moon) is derived from the combination of about 15 or so different computations.  Figuring out which equations proved difficult without a solid understanding of astronomical geometry.  For this, I found W.M. Smart's [Textbook on Spherical Astronomy](https://books.google.com/books/about/Textbook_on_Spherical_Astronomy.html?id=HVJhQgAACAAJ&hl=en) 
to be a literal project saver. 

Briefly, the phase and angle of rotation of the moon is derived from the position and distance of the sun and moon, in relation to your current position on the Earth.  The percent of the moon that is illuminated is a direct result of the angle between these three bodies.[1]

There's a few other things involved with calculating a heavenly body's exact current position: the difference between the "mean" sun time and actual sun time, taking into account the elliptical shape of planet Earth, and adjusting  the coordinates from geocentric to your location on the Earth's surface.  I'm doing a real disservice by not fully explaining how it works, but it feels outside the scope of this blog post.  I'll have to do a follow up post on the basics of spherical astronomy.

Luckily, Meeus' book provides algorithms for all of these things. Meeus doesn't give good test data for the calculation I was doing, so I used CalSky's excellent [Moon calculator](http://www.willbell.com/math/mc1.htm) to verify that my implementation was returning accurate values. You can use it yourself to see what the moon looks like at your location, on your computer screen.


### Display

Adafruit's LED samples included an example using Python's Image Library, or PIL. PIL allows you to compose image arrays, which the LED library would then render to the screen.  PIL's API allows you to compose your own image; with a few more equations you can get an image of the moon with just two overlapping circle arcs.

I ran into two problems getting the moon rendered correctly.

First, Meeu's algorithms return the percentage of the moon currently illuminated.  In order to draw this, I'd need to translate that percentage into a circle arc that could be drawn with PIL.  Drawing a moon at 50% illuminated is quite straightforward: you just need a semi-circle. Any illumination above or below this requires knowing the arc and radius of the intersecting circle that draws the shadow across the moon's face.

Using the percent illuminated returned by our astronomy calculations and the radius of the moon (with a 32x32 square, your radius is 16), we can find the area of the illuminated portion with some math[2]. This ended up being less than straightforward to solve for directly, so we approximate within a few decimal places.  Since this is a non-trivial computation and since the values are static, I ended up generating a lookup table for these values.

It turns out that rendering arcs at  32x32 pixels is incredibly grainy, or aliased. The resolution was so bad that the moon animation wasn't smooth -- instead of waning steadily the moon clock would appear to jumpily get bigger and smaller.  However, reference images I was generating at higher resolutions transitioned smoothly.  Since the LED matrix supports a wide gamut of colors, a friend suggested resizing the correct, larger images down to the LED matrix size using a bilinear filter, which smooths out the curves using color interpolation. SciPy provides this functionality for images; the resulting output is what you see on the Moon Clock today.

That about sums up the 'science' behind the Moon Clock, the last bit involved mounting the whole contraption into an Ikea Ribba frame.

![LED matrix backing](/img/moon_led.jpg)


## Nota Bene

### There are a few things the Moon Clock doesn't account for:

- Elevation. Meeus' algorithms ask you to consider the elevation of an observer when calculating the parallax between your position on the Earth's crust and the center of the Earth (where almost all the planet location equations assume you are).  In my tests, the difference between sea level and the top of Mount Everest (8,850m) had a negligible impact on the moon's appearance, at least in terms of percent illuminated and rotation; instead it's been pegged to a reference elevation of a few meters above sea level.
- Whether the Moon is above or below the horizon.  The Moon Clock shows what the moon looks like from your position on Earth, more or less assuming a transparent Earth.  When the moon is below the horizon, the illumination shown will be accurate; the rotation however is an estimate.
- Moon libations.  Briefly, 'libations' refers to the oscillations the moon experiences as it rotates around the Earth. This oscillation slightly changes what part of the Moon face is illuminated and visible. Since the Moon Clock's moon image is screen printed, it doesn't accurately reflect the markings you'll see on the actual moon. You can read more on moon libations on [Wikipedia](https://en.wikipedia.org/wiki/Libration)

### Upcoming work:

- I'd love to get the Moon Clock to be battery powered, but I'm not sure this is possible with the current LED matrix set up I have.
- I still need to update the matrix driver to the newer mainline version
- I'd love to figure out how to run the Moon Clock on simpler PCB; the Raspberry Pi feels overfeatured for what I'm using it for. 


## So what's having a Moon Clock like?

In all honestly, I'm still discovering what it's like to have this background consciousness of the moon. I'm constantly being surprised at how the Moon has (or hasn't!) changed since I last looked. The phases seem to come and go a lot faster than I anticipated.  And it's always changing!   I'm traveling right now, and I feel a bit disconnected, not knowing what the Moon looks like today.  It's weird not knowing.

## What's next

I'm planning to Kickstart the Moon Clock some time in 2018.  I'll let you know when that happens.  Until then, I'm keeping the source code under wraps; I anticipate making it public will be part of the project launch.


## Debts

This project has a many debts. I owe a big thank you to Karthik Raveendran for his endless support and deep graphics knowledge; Bryan Newbold and Sarah Gonzalez for lending their expertise and time to this project, especially at the early stages. For their true dedication to 'non-invasive living technology', the Moon Clock project is philosophically indebted to Jake Levine, Zoe Salditch and the rest of the Electric Objects team.

![Moon Glamour Shot](/img/moon_dark.jpg)

--- 

[0] Charlie Deets just launched a [moon app!](http://charliedeets.com/moon/)

[1] Every computer's ability to provide you with UTC time came in handy for astronomical calculations. Before computers, figuring out the real time of your location involved taking the wall clock time, translating that to UTC time, and then recalculating the "actual" sun time for your specific longitude. The reason for this is that wall clock time isn't the actual time at your location -- it's set to a reference longitude which may be off by a few minutes.  For our purposes, using your 'timezone time' rather than your actual time probably wouldn't make a noticeable difference, since the resolution of the moon available on a 32x32 LED matrix is fairly low, but for accuracy's sake, using the 'actual' time is preferable. 

[2] See [Circular Segment](https://en.wikipedia.org/wiki/Circular_segment#Area). In our case, we know the area and need to solve for the radius R and angle theta.
