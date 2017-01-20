timestamp: 1484071777
date: 10 Jan 2017
time: 13:09
title: Death by Thirst
tags: foresight, grand-canyon, dehydration

---
## tl;dr: Drink water before you feel thirsty

A while back, I had the chance to hike the Grand Canyon with some intrepid friends.  On our way home, we stopped by the park gift shop where I picked up Over the Edge: Death in the Grand Canyon. Written by Michael Ghiglieri, Over the Edge is a re-telling of all recorded deaths in the canyon.  There's falls from the rim vs falls within the canyon, environmental deaths, murder, drowning, plane crashes, animal attacks -- to name a few.  It's a pretty gruesome book.  However, one detail, taken from the accounts of the deaths from dehydration, really stuck with me.

Death by dehydration or its close cousin, heat exhaustion, is common, especially during the summer months when temperatures within the canyon can surpass 120F. Hikers are advised to carry and consume 2 gallons of water for each day they're on the trail. With few access points to the river, steep walls that take hours to hike out of, and limited resupply points, it's easy to run dry.

However, in some cases, hikers were found dead or near death with water still in their canteens.

You read that right.  People died of heat exhaustion with water undrunk.  

Why?

The theory is that 1) hikers didn't realize they were dying of heat exhaustion so they were 2) saving their water for when they 'needed' it.

Would drinking the water have saved them?  Probably not.  But at least they wouldn't have died with water in their canteen.  To state the obvious, water in your bottle is useless, as the best time to drink is before you get dehydrated.  Plus undrunk water is extra weight to carry.  

## Thirsty Software

I'll be the first to admit that 'drink the water before you need it' isn't the clearest guideline as far as software maxims go, but I do find it a fun analogy to pull out for making the case for doing preventative work in the codebase, even, if not in spite of, deadlines.

Generally, 'drinking the water' or doing your due diligence and maintenance on your codebase before you need it helps prevent problems later.  Due diligence could be updating a library[1], or extracting out an interface, or adding tests to an untested part of the codebase.  I've found that by doing this 'preventative work', when a new feature comes down I've got the test coverage or the necessary nuts & bolts available to make the work of adding the new requirement quite trivial.

Unrelatedly, it has been shown that drinking more water while writing software improves the quality of your code. Or at least it's been proven to get you away from your keyboard more often during the day, which one could argue improves the quality of the codebase.

Your mileage may vary.



[1] This isn't an exact analogy.  I often wait for library updates to 'mature' a bit before updating. This gives more adventurous members of the community the chance to find bugs before I add it to my production apps.
