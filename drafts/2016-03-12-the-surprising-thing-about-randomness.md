timestamp: 1457782588
date: 12 Mar 2016
time: 09:11
title: The Surprising Thing About Randomness
tags: AlphaGo, AI, human-reactions, wonderment

---

## tl;dr AlphaGo's triumph beating Lee Sudol is a huge milestone.  But perhaps less surprising than we'd thought.

A few hours ago, a human built machine by the name AlphaGo defeated the world champion Go player for a third time, officially winning the first public human/AI Go tournament.  This is a remarkable feat for the field of Artificial Intelligence, and a huge validation for one of the current emergent strategies of AI, colloquially termed "neural networks".[1]

This blog post is meant to be a commentary not on the technology that we're using to 'solve' problems like Go but on the general human reaction to the strategies that AlphaGo has developed.  In other words, why are people so surprised that AlphaGo is using strategies that no human has used?

Two things about AlphaGo are remarkable. First, the number of potential moves in Go is astronomically large. So large that researchers couldn't use the same strategy they used for chess AI.  Historically, for chess AI, beating a human at a game involved computing all potential moves that could occur in a game, like a tree of branching possibilities. Some of these branches lead to a win for you and some, to a loss. As your opponent makes moves, the AI whittles down the remaining choices, picking the branch (ie move) that is most likely to lead to a win for the AI.  This isn't possible in Go -- the tree of choices is too big for existing computers to practically compute.  An alternate strategy had to be developed, one that can dynamically make choices.  The second remarkable thing: AlphaGo did some *very* intense training before it was leashed upon the world.

If you read Google's blog post on building AlphaGo, you'll find that in order to prepare for its match against a human, first it studied "30 million moves from games played by human experts".  Then, AlphaGo played "thousands of games [...] adjusting the connections using a trial-and-error process"[2].  

What's striking about this approach isn't its novelty; it's the similarity to how a human masters a craft.  As an example, let's say that we wanted to learn a new craft of which you have no prior experience or understanding: knitting.  What would be the fastest path to becoming a master knitter?  First you study what existing knowledge there is on knitting: the basic techniques for starting a knitting project, how to finish a knitting project, how to make a single knit stitch, how to make a perl stitch.  Then you'd build learn more complicated patterns, perhaps committing to memory the entirety of Vogue's stitch anthology, building upon the skills you've learned.  You'd talk to knitting experts, watch YouTube videos, go to master classes, learning from a bunch of other expert knitters.  The realm of knitted goods is large, so you decide to specialize in making socks. You'd probably start by knitting a few socks the traditional way, from the top down.  Then you might hear of someone who's written a book on a novel technique for knitting socks from the toe up[3], and study that.  All the while that you're learning new techniques, you're making socks, no two socks that you make the same.  

Do you expect that the 10,000th sock that you made will resemble the socks of anyone particular style or strategy that you studied? Chances are that by the 10,000 sock, you've added your own inventions, weaving together the lessons that you learned from a wide range of masters and techniques into a style that is all your own.  You've become a master sock knitter, built upon trial-and-error and studying other knitters.

Given that the software programmers writing AI have developed a program that can a) remember moves its experienced and b) draw conclusions based on the outcome of those moves (ie calculate probabilities for success), it seems that this program has the same raw capabilities as a human learner does for becoming an expert.

So let's focus on the differences.  First, AlphaGo has the benefit of a huge bank of studied moves.  30 million moves by the best human players in the world is probably an order of magnitude more than the most expert human Go player has experienced, let alone remember.[4]  Secondly, an AI has the benefit of time.  It can run simulations and play thousands of games against other simulations in a fraction of the time that a human possibly can. Thirdly, an AI has the benefit of randomness.  Here, I'm making an assumption about how the simulated games were composed: that they were seeded by a random number.  

This is a fundamental difference.  Human Go players play other humans, who have developed their strategies over thousands of years by playing other humans.  The type of game play that humans have as material for study is bound by the set of rules and experiences of their human opponents.  AlphaGo, on the other hand, played against randomness. Perhaps it was a randomness informed and instructed by the 30 million odd moves that had been pre-loaded into the system, but without the bounds of prior human experience limiting the moves that it could develop. Lee Sedol is facing an opponent of the likes of which no human has ever faced.  One whose moves are learned from thousands of _random_ trials.[5]

Ostensibly, the set of moves that human intelligence uses for play also was seeded randomly; ie consider that the entirety of strategies for Go that humans have developed are the product of a single random seed.  Given that the space of potential moves for Go is so vastly large, it should be unsurprising that a system operating on the same learning principles as humans but starting with a *different* seed might develop strategies that we've never seen before.  If anything, the emergence of novel strategies is a sign of the correctness of the hypothesis of evolution, and a validation of our understanding of the underlying precepts for intelligence.

What really baffles me though, and in a large part what spurred this blog post, is all the post game 3 commentary that registered surprise at the emergence of novel moves. If you're a subscriber to the theory of evolution, what is surprising?  Are you surprised that human software researchers successfully built a learning system?  Are you surprised that there exist other successful strategies for Go, outside the set that humans have developed?  Is it that the outcome of a random process didn't equal the previous outcome? Are you surprised that learning systems learn?

If it's the latter, perhaps we should consider out own biases towards learning[6] -- who knows, with a little hard work[7] and some studied randomness, maybe *you* are the Go player that will outlearn AlphaGo.


[1] My understanding of AI strategies is very basic, largely based on some run-ins with Twitter Markov chain bots, a few conversations with friends that have played around with Google's open sourced neural net code, and a lot of reading on the topic. I haven't watched the Lee Sudol x AlphaGo games; frankly I'm not sure that I would glean much from them -- I'm not familiar enough with the game to recognize 'novel' versus 'traditional' moves.

[2] Google's blog post can be found at [https://googleblog.blogspot.com/2016/01/alphago-machine-learning-game-go.html](https://googleblog.blogspot.com/2016/01/alphago-machine-learning-game-go.html)

[3] Socks From the Toe Up [http://www.amazon.com/Socks-Toe-Up-Essential-Techniques/dp/0307449440](http://www.amazon.com/Socks-Toe-Up-Essential-Techniques/dp/0307449440)

[4] It is a remarkable achievement of human intelligence that we *don't* need to study 30 million moves in order to be expert players.

[5] This lends itself nicely to one possible definition of 'alien intelligence': a decision making entity that is operating from outside the collective wisdom of human experience.

[6] Allison Kaptur's post on growth vs fixed mindsets is A+ reading for thinking about learning [http://akaptur.com/blog/2015/10/10/effective-learning-strategies-for-programmers/](http://akaptur.com/blog/2015/10/10/effective-learning-strategies-for-programmers/)

[7] If an average Go game takes 2 hours to play, and a move is played every 10 seconds, a human Go player would need to observe over 41,000 games before they had encountered 30 million moves. This is 9.3 years of uninterrupted game observation.
