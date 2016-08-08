timestamp: 1470679322
date: 8 Aug 2016
time: 14:02
title: Ring Benchmark in Erlang and Go
tags: erlang, go, benchmark, concurrency

---

### tl;dr In a head to head test, Go is a better language for writing concurrent code than Erlang

## Problem Statement

I'm currently working my way through Joe Armstrong's Programming Erlang.[1]  One of the exercises from the chapter on concurrent programming is as follows:

> Write a ring benchmark. Create `N` processes in a ring. Send a message round the ring `M` times so that a total of `N` * `M` messages get sent. Time how long this takes for different values of `N` and `M`.

>Write a similar program in some other programming language you are familiar with. Compare the results. Write a blog, and publish the results on the Internet

I started off in Erlang.  In my tests, I sent one message around a ring of 10,000 processes 10,000 times in 88s.[2]  That's a single message that's being passed sequentially, for a total of 100 million message passes.

I chose Google's Go to run a comparison in, partially because Golang and Erlang look alike on paper (jk). And because their concurrency models share common roots in Hoare's 1978 paper on "Communicating sequential processes".[3]  

There are differences, however. From a pure API perspective, Erlang allows processes to pass messages to each other directly, whereas in Golang channels are used to abstract away which process you're passing to.[4] Practically speaking, this means that in Erlang you're creating a ring where each node knows the Pid (Process IDs) of the next node; in Go each node has a channel that is connected to the next node.

After re-writing the program in Go, I found a similar ring (10k nodes by 10k trips around) to finish in about 76s.  That's 12s faster than the Erlang version.

I found Go's concurrency models to be easier to work with. The channel paradigm made it easier to reason about passing pieces one to another.  Go is moderately object-oriented and procedural, I found that this made it easier to organize the implementation details into structs.  In Erlang, I wrote two looping functions -- one for 'child' nodes and one for the 'head' node (that had to keep track of when to exit).  In Go, I found it possible to store the data about who was the first node in a node struct, ergo I only wrote one loop. (Though it's probably possible to do the same Erlang, much more elegantly than my attempt.) 

One drawback I encountered with Erlang's model of directly passing messages between processes is that I needed to initialize the process before creating the next node.  This led to some wonky initialization code -- the loops actually contain two sets of logic: one for initializing the loop and the other for the actual message passing.  I found this to be quite messy and harder to reason about than the pattern I wrote up for Go.  It's possible that I'd be able to clean up the Erlang code, now that I've got a better handle on concurrency models.

I ran into issues with implementing this in both languages, which I think are worthwhile to point out. 

## Erlang Problems

In Erlang, I had a lot of trouble putting the 'head' node into a second process.  Early versions of my code had the head node loop running in the same process that I was running the program from.  I kept getting deadlocks in my main program thread and wasn't sure why.  The problem was that I was starting the `head_loop` in the same process as the terminal -- it was deadlocking waiting to hear back.  Spawning a separate process for the `head_loop` mostly fixed this problem. 

This bug led me to discovering this nifty one-liner that checks for messages that the console process has received:

    F = fun() -> receive X -> X after 0 -> no_message end end.

Goroutines nicely encapsulate all of the spawn_link and Pid gymnastics that Erlang puts you through.

## Go Problems

In Go, I ran into trouble when I tried copying Erlang's switch statement loop syntax.  Go gives you the option to construct `switch` statements for channels, a la:

    for {
        select {
          case event := <-ui:
            // process user interface event
          case msg := <-server:
            // process server message
          case t := <-tick:
            // time has elapsed
        }
    }

via Go, for Distributed Systems [5]

Here's what my original code for the `Loop` function looked like:

    func (p *Process) Loop() {
        for {
            switch {
                case msg := <-p.RcvMsg:
                    // ...
                    p.SendMsg <- msg
                default:
                    // do nothing        
            }
          }
    }


As written, this code runs unreasonably slowly.  Passing the message around a single ring of 10,000 nodes takes longer than a minute.  The problem is with the default block.  As far as I can tell, this makes the loop run constantly.  10,000 `for` loops running nonstop creates some contention on the CPU, which leads to slowness.  

There's a few ways to fix this. One is to add a sleep to the default block.  

    default:
        // do nothing  for some time
        time.Sleep(5)
    }

Even adding as little as 1 ms sleep fixed the problem considerably.  To really fix the problem, you can remove the `switch` statement.  The goroutine will block until it receives a message on its receive channel.  

This bug highlighted a cool feature of Go: channels block until they receive input (unless they're used in a switch statement with a default).  In the right conditions, enough waiting channels in the right configuration will create a deadlock.

## Wrapping Up

Given a choice between Erlang or Go for writing a concurrent project, Go would be my go-to.  It's measurably faster than Erlang, and it has slightly nicer abstractions for spawning new 'processes'.  

The complete solution for these problems can be found on Github: [Go](https://github.com/niftynei/go_sketches/blob/master/ring.go) & [Erlang](https://github.com/niftynei/erlang_sketches/blob/master/prog_erlang/ring.erl).

[1] [https://pragprog.com/book/jaerlang2/programming-erlang](https://pragprog.com/book/jaerlang2/programming-erlang)

[2] My laptop is a mid-2011 Macbook Air, with a 1.7 GHz i5 processor and 4GB of RAM.

[3] T. Hoare's CSP paper: [http://spinroot.com/courses/summer/Papers/hoare_1978.pdf](http://spinroot.com/courses/summer/Papers/hoare_1978.pdf)

[4] This re-implementation of Hoare's paper in Golang has a decent discussion at the beginning [https://godoc.org/github.com/thomas11/csp](https://godoc.org/github.com/thomas11/csp)

[5] [https://talks.golang.org/2013/distsys.slide#43](https://talks.golang.org/2013/distsys.slide#43)
