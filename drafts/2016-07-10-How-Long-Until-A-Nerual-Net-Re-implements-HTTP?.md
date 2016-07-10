timestamp: 1468160659
date: 10 Jul 2016
time: 10:24
title: How Long Until A Nerual Net Re-implements HTTP?
tags: http, nerual-nets, future-of-software

---

## tl;dr The future is already here, it's just not evenly distributed -- William Gibson

This past week at the Recurse Center[1], one of our alums, let's call her Jane, gave a a brief, 5 minute presentation on a nerual net she had built.  Jane was working towards being able to build a neural net that could play pong, and had started just with implementing a net that could be trained to replace the Math.round function.  Given a number between 0 and 1, the net would either round it up to 1 or down to 0.  Her demonstration was of the training program, a command line program where you would input a decimal number and the net would tell you what it would round that number to.  You then provided feedback to the net, yes you got it right! Or no, that's not correct.  Over time, with feedback, the neural net 'learns' how to appropriately round numbers up and down.

On first blush, this appears like a lot of work for something that you could have coded in a few moments. Jane's neural net code was quite large, well-over 100 lines.  And her net hadn't been fully trained yet -- given 0.43 it incorrectly guessed that this was 1 (not 0, as we all know in an instant).

Jane is a new programmer. She spent a total of 18-weeks at RC, all of them concntrated on learning more about how nerual nets work. And at 19 weeks, she had implemented a net that could barely determine whether a number was closer to 0 or closer to 1. (Ok, to be fair it just need more training)

But.  Imagine with me for a moment.  What if programming became the task of training a neural net?  You need a function that can calculate a round function?  Train a neural net.  Need a function that can verify if a credit card number is valid?  Train a nerual net for the Luhn algorithm[2]  

How long do you think it would take to train a neural net to communicate with other computers? Or rather, what would the neural net version of HTTP look like?  And what about a brwoser; what would a browser look like if it was built by a huge, complicated network of neural nets? Would it understand interface design, and GPU optimization?  Where to go to figure out how to resolve 'http://nerualnetsforever.com' into an IP address? More importantly, how to render cat GIFs? 

Now imagine this technology, nerual nets, is available for everyone. Image that 95% of the college age population knows how to train and work with neural nets, as it's something they've been doing since they were 10.  In this future, who writes Math.round functions anymore? I'd wager the answer is no one.  We've successfully obsoleted software developers, at least of the 'classical' kind.  We've trained our way out of a job.

What looks trivial today in implementing a small feature, may in a few years be far more complex, like figuring out how to get to Mars, or who the next President will be.

For the record, I'm betting on neural nets.

[1] [http://www.recurse.com](http://www.recurse.com)

[2] [Luhn algorithm wikipedia page](https://en.wikipedia.org/wiki/Luhn_algorithm)
