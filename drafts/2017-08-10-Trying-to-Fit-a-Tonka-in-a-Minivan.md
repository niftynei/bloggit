timestamp: 1502398215
date: 10 Aug 2017
time: 13:50
title: Trying to Fit a Tonka in a Minivan
tags: refactoring, architecture

---

One of my biggest weaknesses in software for a long time was the absolute belief in my ability to shoehorn a Tonka truck into a Minivan object.

In other words, I believed that I could take something that looks nothing like a Minivan, and fudge the data structure just enough to fit a Tonka truck in it. 

This causes problems. Always. Usually those problems radiate outwards from the data storage place to all the places that have to come in contact with the data. Suddenly you need functions to know how to tell the difference between a Tonka and a Minivan, since what you're handing them could very easily be either.

You need the ability to tell the difference between a Minivan and a Tonka truck everywhere that that data object ends up.  The chance for forgetting to check for Tonka vs Minivan-ism becomes higher the longer it's been since you stuck a Tonka truck in the Minivan parking spot.  It also becomes higher the more code that you write that has to deal with that parking spot (so to speak).

I find that this is a problem that tends to crop up in non-typed codebases most of all.  Because there's no type checking system to make sure that you've kept the Tonka out of the Minivan object, you just shoehorn it in.

It is possible to shoehorn Tonka trucks into Minivans in typed languages; sometimes they give this ability a special name like 'generics'.  In generic land, you're only in marginally better territory than non-typed language territory -- the consequences of having to check the label on the object you get remains valid.

I wouldn't care about this so much if I wasn't currently attempting to get the Tonka truck out of the Minivan parking spot at the moment.

If only everyone learned lessons at the same time that I do.
