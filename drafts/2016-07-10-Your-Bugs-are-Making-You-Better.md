timestamp: 1468158650
date: 10 Jul 2016
time: 09:50
title: Your Bugs are Making You Better
tags: 

---

## tl;dr Bugs are powerful indicators of where your knowledge gaps are.

I work at the [Recurse Center](https://www.recurse.com) (henceforth RC) as a Facilitator.  As a facilitator I help people pick projects, organize and run interview prep, keep things in the space moving smoothly, and serve as a semi-permanent, always available pairing or debugging partner.

 In this capacity I've had the opportunity to help more than a few people with their bugs, and am pretty familiar with the routine of winding your way down through both the problem space and the source code, in an attempt to figure out what's going on.  

 As an active software developer, I also encounter my own bugs or problems from time to time.  In solving these problems, I learn things, most of which could be succinctly summed up as "How my idea of the world is not what actually exists".

 This past weekend, I had the pleasure to ride along on a meet & greet with a prospective resident for RC (let's call her Jane).  Jane had been the CTO at a financial trading firm in NYC and taught classes sometimes at NYU.  Her advice for RC was that we should build out a common environment, as her financial firm had done, that was built on top of a linux distribution and could be downloaded and easy to set up for any person in RC.  They'd be able to develop their software in it and then easily push it out to a variety of places.  Her rationale behind this was that a skill her firm looked for in developers was their ability to deploy. By providing pre-made packages for Recursers, we would help them learn the entire deployment stack, as opposed to how we do help people deploy things currently, which is pushing things out to Heroku.

 First,  I have to say that I was opposed to this idea mostly because of the amount of work it would add to my list of responsibilities.  Keeping a linux package up to date for anyone to download is work, and I'd rather not do any more work than I have to. 

 Secondly, and more ideologically, providing students with a 'clean-room' version of Python (for example) that *just works* sounds nice in theory, but in practice runs counter to the very idea that Jane had been proposing in the first place -- that providing a box that goes "all the way down" would be more 'learning-rich' than just 'pushing to Heroku'. 

 In my experience, the biggest learning comes in two ways: 1) doing a thing for yourself or 2) encountering bugs.  Providing a working dev environment to all participants at RC effectively removes both of these opportunities for learning.  Do Recursers encounter problems installing Python?  Yes, sometimes.  Do Recursers sometimes waste lots of time getting the right dependencies installed for OpenCV or Pandas, or some other technology?  Yes, definitely, all the time.[1]  Do Recursers get frustrated by the inability to make actual 'progress' on a project because they're mired in dependency or install hell?  Without question.

 However.  Inability to resolve problems, be it in code or in package downloading, is indicative of not fully understanding what and how something works.  I agree with Jane: programmers *should* know how their package managers work, as far down as they need to in order to successfully troubleshoot problems when they encounter them.  If you don't understand what a PATH[2] variable is, then having an environment where that is already setup for you perfectly won't help you to figure out how to add new environments to it.  Further, it keeps you from understanding how to modify and change your computer such that you can add new programs (maybe ones that you wrote) to the PATH, to be used anywhere.

 This is a key point of the power of knowledge -- knowing how things work enables you to change and modify them as you see fit.  Bugs are a gateway to that knowledge, and removing bugs and problems from people's path is really taking away a great learning opportunity.  Which as a facilitator, runs counter to my job.

So the next time you can't get a package to install, instead of getting frustrated, think of all the marvelous things you're learning! Either about how computers work, or the architecture decisions of the package maintainer, or maybe even the politics that went into whatever it is that is causing you grief at the moment.

Maybe it's not the most marvelous thing to waste your time with, but the silver lining's not so bad.

 [1] To a large extent, I am ignoring the other, larger problem that the nature of the Recurse Center presents: that Recursers work on a variety of diverse projects, and the requirements for what a 'common' machine would need in order to be useful to even half of the participants at any given time is daunting, both from a maintenance perspective and a requirements gathering project.

 [2] A PATH variable is a Unix-shell[2.a] construct that allows you to run programs from any directory, regardless of where that actual program lives on your computer.  This is like being able to start the Chrome app while you're digging thru the Trash Bin.

 [2.a] If you are a Mac user, your Unix-shell is Terminal.
