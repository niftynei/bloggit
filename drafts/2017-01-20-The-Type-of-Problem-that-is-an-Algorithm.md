timestamp: 1484891132
date: 20 Jan 2017
time: 00:45
title: The Type of Problem that is an Algorithm
tags: algorithms, architecture, types-of-developers, skillsets

---

## Wherein I Rant About Being Interviewed

I had an in-person interview recently where the day was split up by 'type' of skill that, I, as a 'generic' softwawre engineer (typically this means web) am expected to have acquired by this point: front-end knowledge (JS & CSS), architecture, databases, algorithms, 'culture', a tour of the code-base, and lunch with a few other engineers. Without question, I bombed the algorithm portion, fumbled quite a bit on the front-end piece (in my defense, it has been 5 years since I last made a web UI), and revealed a large knowledge gap about how database indexing works.

Having the skills required to be a web engineer so concretely delineated and feeling like I wasn't really particularly good at any one of them, made me question what skills I had.  It certainly wasn't domain specific knowledge of large databases or JavaScript or how to solve algorithms.  Yet I have been writing and shipping software for half a decade.  What exactly have I been doing, if it wasn't any of these things?

As a mobile dev of the Android variety, I'd say that the types of problems that I've spent a lot of time thinking about are application state[2], manual testing, code architecture, network availability, and view drawing code.  I enjoy thinking about the way code fits together.[3]  

I've found interviewing to be a struggle because solving algorithm problems is not something I'm good at.  I've taken a single online class on them, solved a number of exercises, watched tens of other engineers solve algorithms problems, and am generally familiar with the classes of problems that algorithms fall into.  But I haven't, personally, solved a large number of algorithms problems on my own, an experience that I think greatly improves your ability to do so when timed and under pressure.

In thinking through this, I found it helpful to delineate the difference between an algorithm and an architecture question, as a way to better understand what sort of work involves needing to be good at one or the other of these skills.


## The Nature of an Algorithm

An algorithm is the precise set of steps that you must take in order to accomplish a task.  A solution to an algorithmic problem can be judged on the number of steps that it takes to complete the task and the amount of computer memory that is occupied during the process.  Solving an algorithm, then, is a matter of divining the necessary steps.

An algorithm can fail if the defined steps do not return a correct answer for a valid starting condition.  Part of the process of finding a solution is identifying potential places that the steps, blindly followed, will arrive at incorrect results.


## The Nature of Program Architecture

Architecture is the theater of abstraction. As a topic, it is a wider, and more nebulous category of problem, but generally speaking it is a class of problems that concerns the definition of spheres of responsibility between the various functions of your application.  Usually this involves some amount of data flow.  When you 'architect' a system you are naming things, assigning work, and defining relationships.


## Wrapping Up

The interviews that appreciate the skills that I currently have are the ones that I've done the best at.  I didn't end up getting the job at the company who put me through a litany of web-centric problems.[1]  It's frustrating to be judged on what you don't know, rather than what you do, but I've been enjoying the opporutnity to better understand what different engineering organizations value in new hires.


And next time, I'll definitely spend time brushing up on algorithms.



[1] I didn't get the job, for reasons cited as "looking for someone with more web experience", at which point I seriously had to question the recruiter's reading comprehnsion skills, as you could have figured that out from my resume in about five seconds.  Based on their interview process, they seem to be seeking candidates with a skillset that generally matches that of their existing team.

[2] Android developers tend to be very well versed in state-management by nature of the job.

[3] As much as I hate them, take-home coding exercises seem to be the best place to showcase this particular talent.
