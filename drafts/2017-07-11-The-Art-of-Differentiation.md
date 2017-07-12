timestamp: 1499824577
date: 11 Jul 2017
time: 18:56
title: The Art of Differentiation
tags: art, apis, skills

---

## tl;dr: one of the skills software development requires can make you into a pedantic asshole

This post fits into the category of 'allegorical comparison piece on an abstract idea about software as a concept'.  It won't make you better at writing software, but it might help you better talk about and identify certain aspects of the job that is writing software.

Now that I've done the work of setting expectations, let's talk about expertise.

### Expertise, Kinds of

Roughly speaking, there are five types of 'expertise' that a person can develop. These expertises are as follows: 

- physiological: feats of strength. Usain Bolt's speed or Simone Biles' graceful, aerial contortions
- muscular manipulation: muscle memory type things that require a certain amount of practice and movement, usually only developed through practice. Carpentry, knitting, playing a musical instruments, vocal production and acting
- memory: learning new languages, rote recitation, math
- social: I tend to think of Machievellian Frank Underwoods, but there's also your friend that likes organizing parties
- differentiation: a skill based on your ability to tell things apart; typically built through exposure over time, ie experience

These aren't 'pure' categories; learning a foreign language is part differentiation, part memory and part physical skill (muscluar manipulation). Being adept at math requires knowing what kinds of equations are good for solving a particular problem (differentiation).  It's also highly likely that I've left some categories out. If you think of any, I'd love to hear about them.[1]

## On Differentiation

Of all these skills, differentiation is the skill of erudition. 

Consider the case of a sommelier, a wine expert often hired by restaurants to field questions of wine pairings from patrons and offer suggestions to the less knowledgeable. Becoming a sommelier requires you to gain the skill of differentiation in the domain of wine tasting -- if someone asks you to recommend a wine similar to another one that they like, you'd better know of other kinds of wine that are similar to it.  Or at the very least, what won't be similar, lest you recommend the wrong thing.

Writing good software also requires a taste for differentiation.  Put another way, a software developer needs to be able to know when a thing is different *enough* from another.  Given another requirement or feature, is it a new case statement, or is it something that you can shoehorn into an existing structure?  Or once a bug has been found, what type of a change is required?  Do you need a separate class or will just an `if` statement do? Maybe the bug forces a complete rearchitecting of a given structure.

Unlike wine, however, software lines are more difficult to draw.  Wine can be categorized based on growing region, grape type, year of harvest, knowledge of the weather that the the grapes were grown in, how long the wine was casked for, what kind of casking process the wine underwent, who's selling it, etc.  You can compare the flavor of a wine just by tasting it -- the set of different categories of wine are set.  The only wines that need to be categorized are the ones that have been produced; the boundaries are with what exists, concretely.

Software is arbitrary.  The space and delineations of software classes are the made up lines that the creator has seen and defined.  Yes, the definitions and categories are sometimes derived from the problem domain in which you're working -- enterprises call this the business logic layer of an application because the domain is defined in part by the business needs.  But it's not always clear cut whether you should build a factory factory in order to best iterate through the variable typed list or if there's a better abstraction or generic solution that would more concretely capture the difference between the things.  Often times, I've found that the solution is subjective, depending largely on both the preferred tools of the developer and the differentiations that they've discerned.

## Good Software Developers, Then

Good software developers then, become excellent at the skill of differentiation.

They also become pedantic assholes who want nothing but to get to the root of how or what exactly is the essence of a thing. Because without that root, there is no way to differentiate, no way to tell, exactly, how this thing that you're talking about is different from the other.  Whether it's a new feature or something else entirely.

And that is why all of your software writing friends tend, over time, to converge into pendantic assholery.


[1] I would love to know how to classify writing
