timestamp: 1459437434
date: 31 Mar 2016
time: 11:17
title: Efficiency as False Prophet
tags: efficiency, software-architecture

---
##tl;dr: There are cases where redundancy and repetition provide a greater benefit to the system than the sacrifices required to eliminate it.

Jeff Magnusson of Stitch Fix, a SF-based clothing concierge service, recently posted a thoughtful blog post about their novel approach to structuring a data team. The article[1] is worth a read. A particular sentence in the blog post got me thinking about efficiency and writing code (emphasis mine).

>"We are sacrificing technical efficiency for velocity and autonomy. ... There is, however, a *set of less obvious efficiencies* that are gained with end-to-end ownership."

It bears repeating: "A set of less obvious efficiencies". What I believe Jeff is pointing out here is something a bit novel.  Writing efficient code, or setting up systems of engineers and data scientist such that each of them can specialize on a particular problem domain is nothing new. Classical optimization problems have hard boundaries set at the machine level, classical work efficiency is understood as deriving work to its smallest, most specialized task and then assigning responsibility for them to different individuals, making them solely responsible for a single, repeatable task.  At a pencil factory, for example, this means that one person makes the erasers, and another person splices the graphite; no one person builds a pencil from start to finish.

### Repetition in Orgs
What's radical about Jeff's post is that the work hierarchy he's proposing for the data team goes against this factory style of work efficiency.  Rather than breaking down work into its separate, repeatable parts, each data-st (analy-st/scienti-st) is responsible for building the whole pencil.  The software engineers' job, instead of implementing the data-st's ideas, is to build tools that make it easier to build pencils, or in this case data outputs.  They're no longer the pencil _cutting_ group, they’re the pencil _tooling_ group.

If you're thinking that having a bunch of data-st each building their own pencils isn't as efficient as it could be, you'd be right.  But that's precisely the point -- the efficiency of work product, or 'time-saving' in units of engineer/data-st minutes isn't something worth optimizing for.  Instead, Jeff recognized that what was more important than his engineers' time was their agency (ability to get things done).

### Repetition in Code
This question of 'less obvious efficiencies' reminded me of an anecdote a friend told me while at Etsy.  My friend had worked with another software engineer whose approach to product code (building user facing things) could best be described as a "copy-paste" approach. My friend was a bit shocked by this; blatant copy-pasting flies in the face of a core tenet of responsible software engineering -- the DRY principle: Don't Repeat Yourself. 

The offending engineer had an explanation for it: in a product driven software project, the code they wrote, especially user-facing product code, was going to last a few months, at most, before the design changed, or the product priorities shifted.  Why put effort into carefully re-using code and re-architecting solutions to fit this new change, when it was going to change or be discarded momentarily.  All product code has a shelf life -- they were betting it would be a short shelf life.[2]  This is especially true if your group is running a bunch of  AB tests; it is guaranteed that at the end of an experiment one version of the code you wrote will be obsolete.

If you've ever worked in product engineering, you might recognize some truthfulness to this. 

In fact, one could argue that copy-pasting, if done mindfully, actually is designing for a different tenant of software architecture: encapsulation.  By copying all the code that you need from other parts of the project, you can build product feature silos into your app, silos that have minimal shared code with parts of your app external to them.  Precisely because of their relative isolation, they can be torn out easily without worrying about side-effects. Silos like this allow designers and 'product professionals' to make last minute changes to the design without much risk to the larger project.  In fact, this concept has been applied to server side code -- it's colloquially termed "microservices".[3]


### Do Repeat Yourself
So what does copy-pasting and Stitch Fix's data team have in common?  Both are case studies against the century old adage of "work efficiency", or the need to drive out 'repetition' from a process or system.  As I've highlighted above, there are times where efficiency for the sake of efficiency obscures larger goals; in the case of code it's the flexibility to change and try out new things without introducing a burden of rearchitecture and coupling.  In the case of human work, it's structuring your team to provide the most autonomy and agency for everyone.

I've said it before, but it bears repeating: there are cases where redundancy and repetition provide a greater benefit to the system than the sacrifices required to eliminate it.[4]  May we all be wise enough to recognize them.[5]


[1] [http://multithreaded.stitchfix.com/blog/2016/03/16/engineers-shouldnt-write-etl/](http://multithreaded.stitchfix.com/blog/2016/03/16/engineers-shouldnt-write-etl/)

[2] This is a bit of a fuzzy hearsay recollection. I apologize to the characters in this story for any unintended misrepresentation.

[3] There is a flaw with this. True as it is that the code you're writing *will* all be thrown away at some point in the not so distant future, the trouble is that you have no way of knowing what parts of it or when.  It takes some careful crafting to build things that are flexible enough to withstand last minute design changes, but robust enough to be easily refactored.

[4]  This idea of living with repetition because of other, less quantifiable benefits has been explored in other places outside of software, ie in Jane Jacobs' books on city economy, she theorizes about how having a proliferation of small, competing businesses in cities is directly related to the continuing robustness of a city's economy.

[5] Thanks to Sophie Haskins for her feedback on this post.
