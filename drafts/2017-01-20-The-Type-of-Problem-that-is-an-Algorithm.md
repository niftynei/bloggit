timestamp: 1484891132
date: 20 Jan 2017
time: 00:45
title: The Type of Problem that is an Algorithm
tags: algorithms, architecture, types-of-developers, skillsets

---

## WHerein I Rant About Being Interviewed

I struggle with recruiting because solving algorithm problems is not my strongest skillset.  I've taken a single online class on them, solved a number of exercises, watched tens of other engineers solve algorithms problems, and am generally familiar with the classes of problems that algorithms fall into.  That being said, I have not, personally, solved a large number of algorithms problems on my own.  In fact, my achilles heel seems to be dynammic programming problems that I don't recognize as such until it's too late. Much, much too late.

I had an in-person interview recently where the day was split up by 'type' of skill that, I, as a 'generic' softwawre engineer (typically this means web) am expected to have acquired by this point: front-end knowledge (JS & CSS), architecture, databases, algorithms, 'culture', a tour of the code-base, and lunch with a few other engineers. I, without question, bombed the algorithm portion, fumbled quite a bit on the front-end bit (it's 5 years since I last made a web UI), and gave a weird, high-level explanation of how database sharding works.[1]

Having the skills that 'it takes' to be a web engineer so concretely delineated, and feeling like I wasn't really particularly good at any one of them, made me question what skills I had developed as an engineer.  It certainly wasn't domainspecific knowledge of large databases or JavaScript or how to solve algorithms.  Yet I have been writing and shipping software for half a decade.  Surely there is some part of software development that I've mastered by this point.

I very much enjoy -- and spend a good amount of time thinking about -- system architecture.  This can be a small as the, as I like to call it "API UIs", or how another library or part of your application interacts, and code encapsulation techniques.  I'm not really into 'patterns', per se, but I very much enjoy building modular, decoupled, composable software.  I've most recently spent time going deep on how to build concurrent, fault-tolerant systems, elegantly.  I really loved talking through a web-worker, off-line work problem.

As far of types of problems that I've spent a lot of time thinking about, these tend to be application state[2], manual testing, and  code architecture problems.  I tend to be strongly interested in the way code fits together.[3]  

Doing all these different 'types' of interviews made me realize exactly how *much* there is to know in the world of software.  I had never really thought about what 'types' of problems I had been focused on solving before.  What exactly does it mean to be 'good' at solving algorithm problems, vs architecture, etc?


## The Nature of an Algorithm

An algorithm is the precise set of steps that you must take in order to accomplish a task.  A solution to an algorithmic problem can be judged on the number of steps that it takes to complete the task and the amount of computer memory that is occupied during the process.  Solving an algorithm, then, is a matter of divining the necessary steps.

An algorithm can fail if the defined steps do not return a correct answer for a valid starting condition.  Part of the process of finding a solution is identifying potential places that the steps, blindly followed, will arrive at incorrect results.


## The Nature of a T-Bar

Architecture is the theater of abstraction. As a topic, it is a wider, and more nebulous category of problem, but generally speaking it is a class of problems that concerns the definition of spheres of responsibility between the various functions of your application.  Usually this involves some amount of data flow.  When you 'architect' a system you are naming things, assigning work, and defining relationships.


## Wrapping Up

The companies that appreciate the skills that I have are the companies that I've done the best at.  I didn't end up getting the job at the company who put me through a litany of web-centric problems.[1]  It's frustrating to be judged on what you don't know, rather than what you do, but it was illuminating to see what different engineering organizations value in new hires.



[1] I didn't get the job, for reasons cited as "looking for someone with more web experience", at which point I went apoplyectic because you could have figured that out from my resume in about five seconds.  Based on their interview process, they seem to be seeking candidates with a skillset that generally matches that of their existing team.

[2] Android developers tend to be very well versed in state-management by nature of the job.

[3] As much as I hate them, take-home coding exercises seem to be the best place to showcase this particular talent.
