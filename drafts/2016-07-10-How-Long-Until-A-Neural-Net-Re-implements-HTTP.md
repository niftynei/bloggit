timestamp: 1468160659
date: 10 Jul 2016
time: 10:24
title: How Long Until A Neural Net Reimplements HTTP
tags: http, neural-nets, future-of-software

---

## tl;dr The future is already here, it's just not evenly distributed -- William Gibson

This past week at the Recurse Center[1], one of our alums, let's call her Jane, gave a brief, 5 minute presentation on a neural net she had built.  Jane was working towards building a neural net that could play pong, and had started by implementing a net that could be trained to replace the Math.round function.  Given a decimal number between 0 and 1, the net would round up or down, returning either 1 or 0.  Her demonstration was of the training program, a command line program where a trainer inputs a decimal number and the net would tell you what it would round that number to.  The trainer then provided feedback to the net, yes you got it right! Or no, that's not correct.  Over time, with feedback, the neural net 'learns' how to appropriately round numbers up and down.

On first blush, this appears like a lot of work for something that you could have coded in a few moments. Jane's neural net code was quite large, well over 100 lines.  And her net hadn't been fully trained yet -- given 0.43 it incorrectly guessed that this was 1 (most humans could easily tell you this answer: 0).

Jane has been working on neural nets, nonstop, for weeks. She spent a total of 18-weeks at RC, all of them concentrated on learning more about how neural nets work. At 19 weeks now, she has implemented a net that could barely determine whether a number was closer to 0 or closer to 1. (Ok, to be fair it just need more training)

But. Imagine with me for a moment.  

What if programming *was* the task of training a neural net?  What if all of our programs looked like Jane's, where we are no longer telling a computer how to round up or down, but rather building a tiny neural net that we train for 0 or 1.  

You need a function that can round a number?  Train a neural net.  Need a function that can verify if a credit card number is valid?  Train a neural net[2].  Need a function to validate that a user input a valid email address? Train you a neural net, my son, train you a neural net.

What would a browser look like if it was built by a huge, complicated network of neural nets? Would it understand interface design, and GPU optimization?  Would it figure out how to resolve 'http://neuralnetsforever.com' into an IP address? Would it figure out how mouse input works?  Or perhaps more importantly, how to render GIFs of cats? 

How long do you think it would take to train a neural net to communicate with other computers? What would the neural net version of HTTP look like? Would it also have headers and a body?  How would the standards be developed that all nets know how to talk to each other?  Would neural nets form their own Internet Engineering Task Force and give it a catchy name? 

The Neural Nets Conglomerate For A Common Tongue, perhaps?  

Now imagine this technology, neural nets, is available for everyone. Imagine that 95% of all Americans of age 22 know how to train and work with neural nets, as it's something they've been doing since they were 10.  In this future, who writes Math.round functions anymore? 

I'd wager the answer is no one.  

Programmers joke a lot about coding ourselves out of a job, but we haven't succeeded at doing it yet.  It's a common speculation, but in the past 50 years or so, we haven't made much progress. Either we're not very good, or we're doing it wrong. Which may explain why not many people seem to know what it would look like, exactly, to lose your job to your code.

I'm here to tell you that it looks like a thousand tiny training programs.  I am here to tell you that your replacement, programmer, is neural nets. When neural nets can communicate with each other, when they can reverse engineer HTTP, we will have successfully obsoleted software developers, at least of the 'classical' kind.  

We will have trained our way out of a job.[3]


[1] [https://www.recurse.com](https://www.recurse.com)

[2] [Luhn algorithm wikipedia page](https://en.wikipedia.org/wiki/Luhn_algorithm)

[3] Laugh all you want at those Pokemon trainers, but they've got the right idea. Maybe it's time to get good at training.
