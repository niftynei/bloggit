timestamp: 1462373186
date: 4 May 2016
time: 10:46
title: Go in Peace, Use the (White)Board
tags: whiteboarding, interviews, engineering-orgs

---

## tl;dr: Whiteboarding is a great tool for evaluating a candidate's problem solving skills; well done, it can be a competitive advantage for your engineering org.

There's plenty of public discourse about how terrible whiteboarding interviews are.  Typical criticism often concludes that they're not representative of a candidate's coding ability; that they disadvantage certain candidates; that they're hard to do correctly; that they're unrepresentative of the role you're attempting to fill.  As an alternative, companies have been asking candidates to perform other tasks at interviews: assigning take-home projects, doing a pair-programming exercise, giving the candidate time and space to build out a project during the on-site interview, etc. 

Despite all of this criticism and the move away from them at some companies, whiteboarding is still something that you can reasonably expect to be asked when you interview for a role as a software developer.  You will be evaluated based on their ability to draw out answers on a whiteboard.

### Why is this?

While at Etsy, I had the luck to attend a great interviewing workshop given by [Moishe Lettvin](https://twitter.com/moishel) and [Tim Falzone](https://twitter.com/cardamaro).  The main take-away from the workshop was that as an interviewer, your goal isn't to see if a candidate can answer a question correctly. Rather, your goal is to see if you can find out how much that person does or doesn't know.  

Tim put it in terms of a "potato".  Potatoes are lumpy, odd shaped things.  So is the map of a person's knowledge.  During an interview, our goal is to determine how big or lumpy a person's knowledge potato is, with the stretch goal of seeing how a candidate reacts when you hit up against the edge of their knowledge potato: how do they solve a problem that they haven't seen before?  What resources do they draw upon?  Do they get frustrated?  Do they blame you the interviewer, or challenge the question?  Are they easy to work with and give suggestions to?

The truth of the matter is that white-boarding, properly done, can give you enormous signal about a candidate's problem solving approach and the shape of their "knowledge potato".  Does it tell me if they can write compilable code?  No, not really.  But that's not what whiteboarding is a good tool for discovering[1].  What whiteboarding excels at is getting the candidate problem solving and communicating; it's a great forum for trying out collaborating, to see if you can put a candidate into a position where they can teach you something.

White-boarding is a skill, however, and it takes some careful set-up and calibration on the part of the interviewer to get the most valuable information about a candidate.  I'd bet that the reason whiteboarding is so hated is because not many companies set themselves up for this correctly.  What follows are some pointers on how to get the best signal from a whiteboarding interview.


### What makes a good whiteboarding question?

There's nothing wrong with asking questions that are orthogonal to the job they'll be doing.  Yes, I am telling you it is OK to ask those god-damn linked list problems.  They're valid.  Especially if it's a problem the candidate has never seen before.  

In my experience, the best whiteboarding problems are ones that are short enough to be solved by an experienced dev in a few minutes, and will take a less experienced candidate thirty to forty minutes.  If a candidate aces your question, ask them another, harder one.  Make the problem more challenging, maybe ask something impossible.  Your goal is to get to something that they don't know, so you can watch them problem solve.

Having given a good number of interviews, I've found that the best white-boarding questions are one that you, the interviewer, are familiar with but don't know the exact answer to.  You must be familiar enough with the problem domain to be able to answer any clarifying questions that the candidate has, but not so familiar that you find yourself impatiently watching the candidate stumble through the problem.  Not knowing the answer puts you both on more common footing - I'm far more engaged with the candidate's problem solving process and curious about where they're going when I don't have a preconceived idea of how to get to an answer.  Although it's subtle, you're now positioned as a collaborator with the interviewee, not a judge.  Ideally, collaboration is the kind of working relationship that you're aiming to build with this person - and during the interview is a great time to try out how you like working with this person.


### What if they get the wrong answer?

The right answer is nice to get to, but ultimately not the point.  The point is to observe how a candidate solves a problem.  Do they ask the right questions?  When they get stuck, what do they do?  How are edge cases considered?  Are they able to successfully walk through their pseudo code and find bugs?  Do they try to come up with examples that will break their solution?  Do they ask for help when they get stuck?  Do they explain the problem and their thinking to you, so that you can follow along?  

Remember, you haven't necessarily solved the problem before either.  This puts you in the best position where you can ask genuine questions for clarification.  Asking them to step thru and do the work of explaining their solution such that you can understand it is more authentic when you're genuinely learning along with them.


Finding great candidates is a hard problem.  You want to hire people that are sharp, that are good at solving problems, and communicating about them.  Being a good whiteboarding interviewer will help you determine if a candidate is great, but that's only part of the equation.  You still have to find them, and then convince them that they want to work for you.  Solving problems can be fun; who knows, maybe a great whiteboarding interview is the thing that sets your company apart.


[1] If this is what you're trying to use whiteboarding for, stop.  Go get yourself a laptop.  Sit down with the candidate, open up a REPL.  Now ask the question again.

[2] Thanks to James Porter for his early review and feedback on this post. James and I are facilitating at the [Recurse Center](https://www.recurse.com/) for the next few months, a self-directed educational retreat for people who want to get better at programming.  Applications are now open for Summer and Fall 2016 batches.  Most of the insight for this piece comes from helping Recursers get better at whiteboarding.
