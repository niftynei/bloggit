timestamp: 1493296949
date: 27 Apr 2017
time: 05:42
title: Roadblocks on the Way to Refactoring
tags: refactoring, maps, wtf

---

## tl;dr how good is your mental map of the territory?

My three month 'anniversary' at Pluot Communications is quickly approaching.  In the time since I've started, I've worked on a dizzying number of projects, most of which has been getting up to speed on how WebRTC and React/Redux works.  Recently, a lot of our software contractors rolled off the project (and hopefully onto something else equally squishy).  Anyway, with their rolling, I've since more or less acquired responsibility for a large React / Redux project.  Part of the work we've been doing at Pluot lately is a big re-skinning job, getting ready for some soon to come feature that I'm not allowed to tell you about yet.

Reskinning is like refactoring the view parts of a website.  It seems logical to me then that refactoring the code parts would rightly follow.  And they usually do, depending on what, exactly has changed about the spec.

Refactoring a project that is A) large, B) mostly unfamiliar, C) untested, D) written in a dynamic, non-self documenting language (JavaScript) is not one of those things that anyone would largely recommend that you do.  I'm here to tell you that you can and you should do it.  Here's why.

## What should Refactoring accomplish?

I'm going to be honest, I don't know why other people re-write things.  A lot of times when I've observed teammates embark on refactorings (which honestly never seems to be as often as I feel like I'm hauling off on them, but I digress) sometimes the code comes out cleaner. Most times it comes out far more confusing and complicated and they claim that they've just saved ... something.

I don't buy white knight refactoring.  When I refactor shit I'm usually multiplying code.  I refactor things so that I can read them, so that the chance of me breaking something in the future in considerably lessened, so that it's easier to make changes to one part of the code without having to necessarily consider other parts.  When I 'refactor' I pull out components, try and keep all of the logic for a thing into a single, canonical, topically or functionally organized place.

I try as hard as possible to decouple view code.  View code is notorious for being an arena for subtle bugs.  You change a padding in one place and it looks good everywhere except the checkout page where it completely hides the Buy button for certain languages.  Of course you checked everywhere, except there, and it took an analyst three days of pondering why the sales numbers in Turkey had taken a plunge in order for someone to figure out what had happened.  

As far as I know, I've never done anything like this. But that just shows what I know.

## You mentioned earlier that refacotring large, unknown, untested, untyped projects is a good idea. Can you expand on this more?

Sure. When you're faced with changing a codebase that you don't understand, the probability for changes you make introducing bugs is very high.  There's a whole taxonomy of where bugs originate from that I won't get into right now, but a large, a very large class of them, fall under the category of problems introduced because you did not understand how the code worked.  The root of these bugs then is Your incomplete mental model of the codebase.

So how do you pre-emptively fix this class of bugs, bugs caused because there are incorrect assumptions that you have drawn about how the code works?  It may seem obvious, but the easiest way to not make bugs based on bad assumptions is to not hold bad assumptions.  How do you know what quality of assumptions you hold?  Like any good scientist does, by testing them.

How do you test assumptions about code?  There are two ways. One is by closely reading the source document. This is a bit of a pro-level move. The other is by changing things and seeing what breaks and how.


Sometimes I rename variables just so I can see where all it's used.  That way I have to touch every single last place that that particular variable appears.  It also makes grep a viable tool to help you check when you're finished with a particular task -- when all mentions of the old variable are gone you're done.  Grep is a particularly important tool for non-static or non-compiled languages.  Back in the day when I did Java codes, IntelliJ or Eclipse would automatically reneame a variable with a few strums of the keyboard.  Without that compiler guarantee, it's basically up to you to manually check that every instance of a variable has been updated or changed or whatever.  Grep's a good tool for this.  If you're new to the grep game, check out `git grep` -- it only parses files that are checked into git.  The only flag I really use for grep is the occasional `-n` which shows the line number that a particular match was found at.  Between grep and vim, I can crank through a number of renamings pretty quickly.

What's the use of knowing every place that a variable is used? It gives you an idea of the scope of that object. If you know every place that a variable is used, your assumptions about that variable are probably more accurate, which reduces the chance of introducing bugs.  More than anything, you'll find out really quickly how good your naming scheme is.  If you're having trouble figuring out which 'versions' of a variable name are related to each other, maybe you should use more explicit or unique names for things. Asking someone to use a project unique name for every variable is a bit of a tall order, but hey no harm in considering it.  After all, you are programming in a language with a shitty toolset -- hacks are expected.

## When to Refactor?

You should refactor any time that you encounter code that you do not understand and the person who wrote the code is no longer available to explain it to you. The goal of the refactoring should be simple -- to make it such that you do understand the code.

## What if you break the code and can't get it work the way that it originally did?  

Let's go back to assumptions. If you're unable to re-write code such that A) you understand it and B) it functions as it previously did, then clearly you don't understand what that code is doing.

In this situation, my advice is to either A) start over or B) give up.  If you give up, you better not change anything else related to how that code works as you've just irrevocably proven that you have no idea how it works.  Clearly the person who wrote it is a madman who sucks at programming and you should celebrate your defeat by posting the offending code-bit to the code shaming website of your choice. I recommend StackOverflow.

## What if you need to make a change to that code but you don't understand how it works? 

I'm sorry to say it, but your odds don't look very good here.  Making changes to code you don't understand is not something I'd put money on.  You really shouldn't either, but this all depends on what you consider an acceptable level of risk.

Have you tried asking for help? I hear StackOverflow is a good place for that.


## What does Refactoring accomplish?

Ok so you've totally refactored large swaths of your project and managed to wrangle the three-way merge hell into a single large commit.

Congratulations!  You are now the only person who, supposedly, understands how the code works.  As the only person who understands how the new code works, you have implicitly become its maintainer into perpetuity.


Isn't that exciting?
