timestamp: 1561128635
date: 21 Jun 2019
time: 09:50
title: A Quick Post on this One Tool c-lightning Uses
tags: c-lightning, tooling, waoh, linkers

---

tl;dr: I found (another) cool tool hidden in the c-lightning codebase

c-lightning has a bunch of really cool little utilities and conventions baked into it. I recently discovered how the auto-generator for mocks work, and thought it was novel enough to write about, so here's a quick exploration of it.

I've been working on implementing a new open channel pathway for allowing dual funded channels to become a reality. It's definitely the biggest project I've worked on in c-lightning so far, so it's giving me the opportunity to run up against all of the little problems that you might hit when developing on a large C project.

## Building a C program

When building a C program, there's actually two steps. One is the compilation round, where your .c files are written as bytecode, in .o files. Next, there's the linker step, where references to functions in other .o files are linked together so that program execution knows where in memory an externally referenced (i.e. in a different file) method's code can be found.[1]

Typically, a C program's buildscript is composed of Makefiles. These Makefiles are responsible for indicating to the linker which .o files need to be included when building a binary for a C program. (The c-lightning project builds a number of binaries -- one for each of the daemons.)

I ran into a problem when moving code between openingd and lightningd. I wanted to include some failure handling code. So I added the appropriate `#include <common/status.h>` to the .c file that I was working in. The code I wanted to reuse already exists in common, so in theory it should be fine right?

It compiles fine, but I ran into linker problems, which look like


[1] For a more in depth discussion of how gcc and C program generation work, I highly recommend checking out Brian J. Gough and Richard Stallman's book, An Introduction to GCC. Here's a [link](https://www.amazon.com/Introduction-GCC-GNU-Compilers/dp/0954161793) to the book on Amazon.
