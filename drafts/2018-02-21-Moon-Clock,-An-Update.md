timestamp: 1519277198
date: 21 Feb 2018
time: 21:26
title: Moon Clock, An Update
tags: moon-clock, api, aws, lambda

---

## Wherein we announce the launch of [moon.supply](https://moon.supply)

I've been working slowly, but steadily on getting the Moon Clock project ready for Kickstarter primetime.  It still feels a long way off, but we're getting there.

Since I last wrote in early January, I've built a two more moon clocks and ordered the parts for another few, found an informal circuitry advisor (hi Yuanyu), realized I know a lot more about hardware hacking than I thought, ordered (and am extremely excited about receiving) my first benchtop power supply[0], bought the wrong parts[1] on Digikey, found a friend with a 3D printer and some CAD exp (thanks Eric), talked my partner (<3) into dusting off his electronics 101 skills, found a designer for the KickStarter (hi Paul), and made some LEDs blink.

Oh, and I've ported the moon clock code over from some Golang/Python hybrid to pure Go and put an [API](https://moon.supply/api.html) where you can get the current moon image for any lat/lon[2].

Ya'll, I'm making a thing!

Here's some notes and impressions on the work I've been doing.

## Wherein you realize you're almost but not quite in over your head

I could build a bunch of Moon Clocks using the same hardware I used for the prototypes, but there's a lot of problems with the current set up.  First off, the parts for a Moon Clock, just off the shelf, are really expensive.  The full version of a Raspberry Pi costs $30, plus the Adafruit HAT piece I'm using to wire the LED to the Pi is another $20. That's $50 right there just for the brains of it.

Secondly, the chips don't really fit in the frames I'm using. I might be able to find something a bit deeper, but designing my own board will let me get something that fits nicely into the existing frame. Further, the boards require a decent amount of soldering and setup.  Having a customized chip with all the parts already soldered on will make assembly a lot faster.

On the face of it, designing a PCB from scratch is pretty daunting but, I'll let you in on a little secret.  All that a PCB does is connect the differrent parts together. Most of which pins connect to what is specified by the datasheets (or open source library you're using to drive the display). You literally just connect the pluses to the pluses and the grounds to ground. Ok, maybe it's not that simple for every circuit, but the Moon Clock wiring really isn't that complicated! Winning!

The most electronics I've done is getting some Raspberry Pis to work, and hacking together a pretty complicated light switch a few years back.[3] 

Suffice it to say, I know just enough about how circuits work to be extremely dangerous.

## First steps towards a PCB

The first step toward making your own circuit is to figure out what you need. I'm at this stage right now, more or less.

Figuring out what you need is a lot harder than it sounds.

For starters, I know I needed a 'microcontroller' of some sort, the word 'microcontroller' being about the extent of what I knew about them.  Luckily, [The Prepared](https://theprepared.org/) had sent out this really [wonderful guide](https://jaycarlson.net/microcontrollers/) to sub-$1 microcontrollers.  I passed the article to a friend of mine, who in return sent me back the [page for the STM 32](https://jaycarlson.net/pf/st-stm32f0/).

There's a lot of options for microcontrollers, mostly because there's a lot of different things that you can use a microcontroller for. Solar panel rigs, car interiors, low-power sensors, networked devices, outdoor LED panel displays, etc. Different applications need different things in a chip, hence a plethora of options.

I ended up buying a couple of devboards to try out; here's the criteria I used to help me figure out what to get:

- Clock speed. Adafruit claims you need 16Mhz+ to run the LED panel without too much flickering. The slowest chip I got runs at 48Mhz (the F0 series), the fastest is up to 72Mhz (F3). Raspberry Pi's, for comparison, run at about 1Ghz.
- RAM. This is how much you can hold in memory at once. For the LED display, we theoretically need to be able to hold a 32 x 32 x 8 x 3 byte image, which is about 24K. That's not counting the program that's running. I accidentally got one dev board that only has 20k of RAM; the beefiest board I've got has 128k (?).
- Flash Memory. This is where the program we write will get stored. I'm not too worried about how big this needs to be but bigger is probably better.

There were a few things that I have come to realize might be important, but at the moment don't have any real way of evaluating boards for this:

- Floating point hardware. The Moon Clock calculations do a lot of floating point math. Supposedly some chips have addons that make this a lot faster. Luckily, the clock face doesn't update that often, so we'll probably be fine.
- Energy efficiency. Good thing the clock plugs into an outlet.
- Number and type of pinouts. There's still a few circuitry parts to figure out[4] but I'm pretty lucky that the LED panel I'm driving doesn't have any complicated connector requirements. The STM32 dev boards I ordered ended up having Arduino compatible pin configuartions, which made finding documentation on them pretty straightforward.
- Dev environments. The nice thing about the STM boards is how straightforward the dev environment is. There's a graphical image of the board! With pinouts that you can configure with a GUI! It generates C code for you!  The STM family is known for having a good dev environment though, so I definitely lucked out.

So far, we've wired up one dev board and gotten it to flash an LED. Which feels like a huge success!  There's still a lot of work to go in terms of wiring up the LED matrix, but it feels within reach!

After the LED driving bits are sorted out, I'll probably need to port the Moon calculating code over to C. That, or figure out if Go will run on a tiny chip. I'm stoked.

## Putting up an API

On the software front, I thought it'd be fun to put up an API to let other people use the Moon engine I wrote to get Moon pictures. It's super simple because I was too lazy to add more functionality, but if you give it your latitude and longitude, it'll give you back a base64 encoded 320x320 image of the moon right now at that location.

You can try it for yourself with curl, or by hitting this endpoint in a browser:


```
curl "https://api.moon.supply/img?lat=37.7272&lon=-77.2918"
```


I got really lucky because AWS *just* launched Golang support in Lambda back in January. There's a lot of hacky projects that will let you run Go with a nodejs or python wrapper; but luckily I didn't have to deal with any of that. The moon engine is a really great example of a good use case for Lambdas -- the calculation engine is completely contained and you really only need it when you call it!

I couldn't find an example of how to send back the 'raw' png bytes using the AWS API Gateway event object so I encoded it to base64 to send back. If you know how to make it return an image, I'd be very curious to hear how to do it!

Getting the Moon engine Lambda ready meant re-writing the drawing code from a Python PIL library to using Go's image library. It was a bit easier to do, but required pulling out some trigonometry to get the circle distances correct.

To draw a circle in PIL, the API requires you to provide a bounding box for the circle and an angle which to fill in.  Here's an example that returns a semi-circle.


    img = Image.new('RGB', (320,320), 'black')  
    draw =  ImageDraw.Draw(img)  
    draw.pieslice((start,start,diameter+start,diameter+start),-180,0, 'white')  


The Go image library is a lot lower level. The example that I based my draw-er off of instead requires that you return the color value for a given pixel coordinate. Basically, writing a function that returns either black or white for a given pixel.  It ended up being easier to write than the PIL code, once I figured out how the trig worked.

Here's an example 'draw' function that will get you a white circle; it returns 0 (black) if the pixel point is outside the circle, and 255 (white) if it's inside.


    func (c *Circle) Brightness(x, y float64) uint8 {  
        var dx, dy float64 = c.X - x, c.Y - y  
        d := math.Sqrt(dx*dx + dy*dy) / c.R  
        if d > 1 {  
            return 0  
        }  
        return 255  
    }  

Unfortunately, as soon as I put the website ([moon.supply](https://moon.supply)) up, I realized how nice it would be to have the API return an SVG formatted moon instead of image pixels, so that I could use it on the site without there being any rastering. I'll add it to the 'to-do' list.


## Wrapping Up & Kickstarter Dates

So, things are slowly marching toward a Kickstarter! There's still a lot of work to do, but I'm pretty happy with where we're at right now. I'll keep you posted, but for now look for a launch sometime in mid- to late March! We'll have a few early bird specials, like original Moon Clock prototypes and a bit of a discount for our first handful of backers!

In the meantime, give the Moon API a try and let me know what you think!  Or just visit the [moon.supply](https://moon.supply) site to see what the moon looks like for where you are now.


---

[0] A benchtop power supply lets you try out a bunch of different voltages and currents. If you're working with electronic components and aren't sure what the power requirements are yet, a power supply will let you easily fiddle around with different settings. I got this [one](https://www.amazon.com/gp/product/B06VXGLFWK/ref=oh_aui_detailpage_o02_s00?ie=UTF8&psc=1) from Amazon.

[1] [https://twitter.com/niftynei/status/961469328297148416](https://twitter.com/niftynei/status/961469328297148416)

[2] I think the images for the moon at the poles is broken. Sorry.

[3] I built a wireless circuit and Android app to control a power outlet a few years back (which I then wired up to a string of lights). I [wrote it up](http://www.draftcopy.co/2014/02/first-milestone-xbee-project.html) in story form; I wish I had done more of a technical write up -- I learned a lot about wireless routers (specifically XBees) and pinouts with it. God I had _no idea_ what I was doing.

[4] It'd be nice to have a dial to set the latitude and longitude with.
