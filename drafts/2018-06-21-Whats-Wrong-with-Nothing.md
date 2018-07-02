timestamp: 1530468973
date: 1 Jul 2018
time: 11:15
title: What's Wrong with Nothing?
tags: null, nothing, programming, syntax

---

I had this idea to do a post that was a takedown of the incessant `null` bashing that every Java community seems to fall into, much to my own personal annoyance.

I find it annoying because I enjoy thinking through the case of nothingness. In some way, I attribute `null` complaining as a signal of laziness, of a dev who wanted things to just work and was annoyed when they didn't. A world without nulls, like all utopias, is a nice thought but entirely impractical.[1]

I've come around though. You won't hear me complaining about `null`s quite yet, but, understanding that reality involves nulls and empty cases, your programming language can do a better job at forcing you to handle uncertainty than Java does. Go does a good job with this, I think, in two ways. The first is allowing a method to return more than one thing at a time, the second is by creating a convention of having one of the returned items be an error object.  That, ironically, can be `nil`. So maybe Go hasn't gotten away from `null`, per se, entirely, but they've rearranged the emptiness such that it leans heavily in the direction of surfacing and forcing you to deal with the void.

From the viewpoint of forcing you, as the programmer, to acknowledge and handle the case where an item may have returned or been null, for whatever reason but typically some failure case, Java's recent introduction of Optionals is a good step. Optionals allow you to more concretely signal the potential for a failure case, but, in a lot of ways, it still feels about as useful as bolted-on types in Python.  The language still gives you the flexibility to get around using an Optional how it should be. The compiler won't throw an error if you check if the returned Optional is null. It shouldn't be, if you're following convention, but let's be real, there's nothing stopping you from getting your Optional paradigms sunk into a wicked morass of nulls.

The other language feature that I've been hearing a lot about is the Groovy/Kotlin way of questionably handling null, with a question mark. This is nice from a syntactic viewpoint, as you can make calls without worrying about whether or not the underlying item is there or not. To be clear, I haven't used this much, but I do wonder how this kind of avoidance really gives you the opportunity to handle the `null` case. Sure, it's nice that you're not getting a null pointer exception because you tried to call a method on nothing, but you haven't really dealt with the fact that there's nothing there in the first place. Maybe my opinion will change after I've used the language for a bit.

So, while I won't be complaining about `null`s anytime soon, I am looking forward to learning more about how Kotlin handles the issue. Unintended nothing in programming isn't going away anytime soon, but there is definitely some room for improvement in the paradigm that Java settled on a few decades ago.


[1] I also tend to find `null` complaints from Java programmers couched in some kind of 'syntax' argument, as if checking for null was a pain because it required an unholy 'if' to clutter their otherwise perfect roll of business logic. Optionals seem to be exclusively dedicated to reducing the number of times that you have to call `if` for reasons that I don't entirely understand. Something about the functional programming bruhaha of the last 10 years seems to have convinced procedural programmers that if blocks are a blight on the beauty of programming. As someone who's spent time writing really ugly code to make apps pretty, I'm not really sure that eliminating the if block makes your app any better. The if is still there, you're just hiding it somewhere. Most syntax 'features' seem disingenous this way.
