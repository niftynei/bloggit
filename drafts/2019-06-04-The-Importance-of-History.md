timestamp: 1564880468
date: 3 Aug 2019
time: 20:01
title: The Importance of History
tags: git, history, bisect

---

I work on [c-lightning](https://github.com/ElementsProject/lightning) and one thing that I spend a lot of time doing, as a new c-lightning contributor, is making my git commit history as perfect as possible. What is a perfect git commit history? There are two things that our team uses to judge whether a Pull Request's commits are good for committing: how bisectable it is and how readable it is. Bisectability is a concern for the machines, or keeping your commit history interoperable with a useful tool, `git bisect`. Readability has to do with documentation, keeping your commit history interoperable with other humans that are maintaining the codebase.

## Bisect

Tooling. It's important. It's especially important that you keep it in a state where you can continue to use it effectively. `git bisect` is one of those tools that is incredibly powerful, but only if you keep an incredibly high bar of 'cleanliness' in your commit history. Basically what this boils down to is that every commit must, at a bare minimum, build. At its core, this has to do with how `git bisect` works.

For the uninitiated, `git bisect` is a built-in git utility that helps to identify the patch that introduced a bug. In order for it to work effectively, however, you need to be able to build (and hopefully run the tests) on every commit.

To start a git bisect session, you run `git bisect start`. Next, it expects you to mark a good and a bad commit. If the current HEAD is bad, you'd say

    $ git bisect bad

Assuming you know at least one commit that was good, you then tell git bisect what the 'good' commit is. As an example, here's how you'd mark a commit hash good.

    $ git biset good 9a7b7a8e


From there, `git bisect` will binary search through the commits between the known good and known bad points until you've identified the commit where the error takes place. It automatically checks out commits, and then you run your tests. If the test fails, you mark the commit is bad (with `git bisect bad`); if the test passes, you mark it as good (`git bisect good`). When you're finished, return to head with `git bisect reset`. 

Since `git bisect` picks 'random' (actually they're halfway between the last marked good + bad) commits, if any commit in your project doesn't build and you land on it with `git bisect`, you're not going to be able to figure out if it's actually a good or a bad commit. Same for breaking tests as well.

To summarize: non-buildable commits break your abilty to 'easily' git bisect through a codebase, and build at any given commit.

## Readability

The other thing that c-lightning reviewers ask for is readability in commit messages. This means that each commit should only contain a single 'logical' change, and that the commit message should accurately describe it. Further, if you submit a set of commits in a pull request, the ordering of the commits should be such that they organize a 'narrative' around what you're changing. If you need to make changes to helper functions, or pull something out so that you can use it elsewhere, that would go before the commit where you use it in the new thing. Same for renaming of things!

Ideally a reviewer will be able to step through the commit set on a PR and be able to understand how, step by step, you got to the final goal that the PR represents.


## In Practice
I find all of these things hard to do in practice, but I've been working on it. One reason for this is that I tend to change a bunch of things at once. Another is that often times when you start in on a project you don't have a good idea of the scope of the change that's necessary to accomplish what you're looking to do. So you start in one place, only to discover that there's a number of other things that need to change in order to move forward. I tend to end up with a huge heap of unrelated changes staged in git.

###  git add -p
There's a couple of ways to get around this. One is to commit more frequently. You make a small change, or rename something, or pull up a method. Then you stop and check it in. Another good tool is to use git add's `-p` flag. This lets you 'pick' what changes you'd like to add.

    $ git add -p

This starts an interactive program that presents you with every edited 'hunk'. You can add it to the staging area (y), leave it out (n), or if it's too big (you want to add a few lines but not the whole hunk) you can edit it, with 'e'. There's a lot more options, you'll see them if you try this. Try them out!

I find myself using 'edit' more than I probably should. I like how fine-grained a control it gives you for adding things to a commit.

If you accidentally stage a 'hunk', you can similarly unstage hunks with the same tool using `git reset HEAD -p`.

###  git rebase -i
Once you've made your commits, you can reorder them, merge commits together, or execute a commands against them using `git rebase`. I use this all the time to add more things to other commits with fixup, to re-arrange the order that commits come in, or to re-write a commit message.  A word of caution about re-ordering commits: this is a really great way to end up with conflicts if you're not careful. If you end up with a mess in the middle of a rebase, you can always abort with `git rebase --abort`.

Typically when I start on a thing, I'll have 20+ commits that will get whittled down to 2/3rds or half of that number for the PR.

I've never done this, but you can confirm that `git bisect` works by running `git rebase -i` with the -exec flag. Kamal[1] has a great blog post on how this works [here](http://kamalmarhubi.com/blog/2016/03/08/git-rebase-exec-make-sure-your-tests-pass-at-each-commit-and-other-rebase-goodies/). Typically what you'd exec is the build and check make commands, and also your linter. For c-lightning this would probably be something along the lines of `make check check-source`.

`git rebase` is great. Score one for neater commit history and preserving bisectability!

# In Exitus
Yes, I spend a lot of time these days massaging commits.


[1] Hi Kamal!
