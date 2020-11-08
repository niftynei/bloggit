timestamp: 1579215867
date: 16 Jan 2020
time: 17:04
title: How to Be Perfect
tags: git, rebasing, tips

---

Git is a collection of commits, a story about a history of changes that you made to a codebase. I've written [before](/posts/2019-06-04-The-Importance-of-History.html) about the importance of this history, but I realized I didn't really put much time or effort into talking about how to manipulate your history. If you can re-write history, why not re-write it to make you look perfect?

Being perfect is expensive. It's not easy. Going back and attempting to make yourself look perfect after the fact is even more tedious and difficult. My understanding is that most people get into programming because they love automating rote things; what I'm about to show you is the opposite of automated -- it's a bit of painstaking work. 

Why would you do this tedious thing? Because it makes you look fucking perfect.

Before we get too far into this, I should offer up a small caveat that editing your git history is pretty dangerous/risky. The absolute best thing to do before trying a rebase like this is to make a new branch that you can attempt to rebase from. That way, if something goes absolutely haywire, you'll have the original branch hanging around still, and you can start over from there, if you want. Or call it quits like the imperfect human that you are and roll forward from there.

Another final note, I consider myself a pretty basic git user as the number of commands that I use on the regular are fairly small, but as you'll see shortly, this technique does require a certain level of understanding of how git's model of commit history and rebasing work. If you don't really grok how git plays and then replays commits during a rebase, maybe reading through my weird way of mangling history will make it clearer. One can hope, at any rate.

Ok, so preliminaries out of the way, what am I even talking about by making a git commit history look perfect? Well, if you're anything like me, you might have a bad habit of checking in slightly broken code, discovering how it's broken later, and then writing a small update to fix the brokenness. One good example of this in c-lightning is allocating an object off of the wrong thing -- I don't find out about it until I've gotten some good test coverage with valgrind running. 

## Fixing Commits, The Easy Way
The easiest way to fix an imperfect commit is immediately after you've committed the imperfect code; when the commit you want to correct is the first commit in your history.

You can easily update the last commit using the `--amend` flag. Basically, how this works is that you update the code and stage the changes, as you would normally. When you go to commit it, you merely add the `amend` flag. This applies the staged changes to the last commit.

	$ git commit --amend

It will re-open the text editor with the commit notes in it, so you can make any edits you'd like before saving and closing. Once you close the commit message document, git will amend the last commit to include the new changes.

## Fixing up Commits, The Hard Way

Ok, let's say that you've made some commits, realized those commits had errors much much later, made some fixes, checked those fixes in and now are at the end of your project and want to go back make everything look incredibly neat. 

Who does this? Me, I do this. It's fixable, but it's also painful. I'll walk you through an example of me fixing up some commits I made to the dual-funding branch on c-lightning, before pushing it up for review. In this particular case, I've committed two fixups into the same commit, however the original errors were made in two separate commits. I need to go back and split the fixup commit into two, before I can then squash each of the fixup up commits into their respective originating commit.

Note that just by giving you this information ("the fixup commit's errors belong in two separate commits"), I'm cheating a bit. Normally, you'd have to go back and figure out that this is what happened yourself. We'll still walk through how to find the originating line change, however, which is basically the same process.

Ok. Let's make some perfectionism happen!

## Example of an over-eager fixup 

Alright, here's the fixup commit. I've pulled it up by running `git show 8280a3a`.


	commit 8280a3a54efa1dcbb767f5f499e2ad86fde460d3
	Author: lisa neigut <niftynei@gmail.com>
	Date:   Mon Dec 2 13:13:03 2019 -0600
	
	fixup: pass correct `am_funder` value
	
	diff --git a/openingd/openingd.c b/openingd/openingd.c
	index 5b37dd7d4..d848cbac6 100644
	--- a/openingd/openingd.c
	+++ b/openingd/openingd.c
	@@ -1170,9 +1170,9 @@ static bool send_receive_funding_tx_info(struct state *state,
 			u16 num_ins, num_outs;
 			int type;
 
	-		msg = opening_negotiate_msg(tmpctx, state, false);
	+		msg = opening_negotiate_msg(tmpctx, state, role == OPENER);
 		if (!msg)
	-			return NULL;
	+			return false;
 
 			type = fromwire_peektype(msg);
 			switch (type) {
	@@ -1434,7 +1434,7 @@ static u8 *funder_finalize_channel_setup2(struct state *state,
 					       &our_sig.s, NULL);
	
		sync_crypto_write(state->pps, take(msg));
	-	msg = opening_negotiate_msg(tmpctx, state, false);
	+	msg = opening_negotiate_msg(tmpctx, state, true);
 		if (!msg)
 			return NULL;
 

Notice that this commit contains two separate line changes: one at line 1170, the other at line 1434. 

It's easy to see why these were checked in together -- they're fixing a problem of the same class, namely the wrong value being passed in to `opening_negotiate_msg`'s final parameter.

In most cases, as a one-off commit, this is a perfectly acceptable way to do things. But we want to make it look like we never even messed this up in the first place. We're *erasing* our mistakes. We can do this because this is still in a branch -- the commit where the original mistake took place hasn't been committed to `master` yet. 

This is distinction is import. We're going to re-write history using rebase to make it look like this little whoopsie never happened. You can't (shouldn't rather) rewrite the history that's on `master`, but branches that you're about to push up as a PR are fair game.

To do this, we need to first find the original commit where the line we're changing got added to the codebase. Then we'll use rebase's `fixup` to merge this commit in with the original, no one will be the wiser to our original mistake. This will reduce your commit count, but that also reduces the number of commits that a reviewer needs to look at and makes the change more 'atomic'. Atomic commits are easier to revert or port elsewhere if need be, and make your history easier to understand because every commit has decent context for the change.

So I already cheated and told you the answer to this, but we need to confirm that they both originated in the same commit. If not, we'll need to break them into two smaller commits, and then `fixup` those patches individually into their respective originating commit. Spoiler: these definitely belong to different commits.

Let's start by finding the commit where the first line was added, the one that we modified. We need to find the originating commit for the line we're changing. Usually, I use `git blame` to look for clues as to where it might have been originally added. This can be kind of tricky, and is probably the hardest part of this whole endeavor. If you already know what commit the change originated in, you can skip this part and go down to where we split it up into parts.

Looking just at the first change in the commit, you'll notice that it's in a method called `send_receive_funding_tx_info`. I'm going to search in git blame for this method.

	@@ -1170,9 +1170,9 @@ static bool send_receive_funding_tx_info(struct state *state,
 			u16 num_ins, num_outs;
 			int type;
	 
	-		msg = opening_negotiate_msg(tmpctx, state, false);
	+		msg = opening_negotiate_msg(tmpctx, state, role == OPENER);
 			if (!msg)
	-			return NULL;
	+			return false;


Now we run git blame on the file that the change is contained within. I've used vim's find utlity to locate the method.


	$ git blame openingd/openingd.c
	
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1091)
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1092) static bool send_receive_funding_tx_info(struct state *state,
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1093)                                        enum role role,
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1094)                                        struct input_info ***local_inputs,
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1095)                                        struct output_info ***local_outputs,
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1096)                                        struct input_info ***remote_inputs,
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1097)                                        struct output_info ***remote_outputs)
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1098)
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1099) {
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1100)       struct channel_id id_in;
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1101)       bool complete;
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1102)       size_t i;
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1103)       u8 *msg;
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1104)
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1105)       /*
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1106)        *  BOLT-3f9f65d3ad5a21835994f9d9226ed9e0e4066662 #2
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1107)        *
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1108)        * - if is the `opener`:
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1109)        *   - MUST send at least one `funding_add_input` message
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1110)        *   ...
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1111)        * - if is the `accepter`:
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1112)        *   - MAY omit this message
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1113)        */
	...


This is a long method, so I'll then search for `opening_negotiate_msg`, which leads me to this code block.


	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1168)               struct input_info **inputs;
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1169)               struct output_info **outputs;
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1170)               u16 num_ins, num_outs;
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1171)               int type;
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1172)
	12953b897b openingd/openingd.c          (lisa neigut      2020-01-16 20:03:39 -0600 1173)               msg = opening_negotiate_msg(tmpctx, state, role == OPENER);
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1174)               if (!msg)
	12953b897b openingd/openingd.c          (lisa neigut      2020-01-16 20:03:39 -0600 1175)                       return false;
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1176)
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1177)               type = fromwire_peektype(msg);
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1178)               switch (type) {
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1179)                       case WIRE_FUNDING_ADD_INPUT:
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1180)                               if (!fromwire_funding_add_input(state, msg, &id_in, &inputs))
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1181)                                       peer_failed(state->pps, &state->channel_id,
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1182)                                                   "Parsing received funding_add_input %s",
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1183)                                                   tal_hex(msg, msg));
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1184)                               check_channel_id(state, &id_in, &state->channel_id);
	7cd71d3128 openingd/openingd.c          (lisa neigut      2019-11-21 17:48:36 -0600 1185)


In `git blame`, the first column is the commit hash where that line was last changed. You'll notice that most of these lines were introduced/touched in commit `7cd71d3128`, but two of them have been updated in `12953b897b`. `12953b897b` is the commit we want to fold into the other one. I'm going to guess that the commit we want to fold into is `7cd71d3128`. I'll confirm this by running `git show 7cd71d3128`, and looking for the originating lines.

	$ git show 7cd71d3128
	commit 7cd71d31281fc23ba7d63d057c631c95591ee4d3
	Author: lisa neigut <niftynei@gmail.com>
	Date:   Thu Nov 21 17:48:36 2019 -0600
	
	    df: port to new input/output dance
	    
	    updates to use the newer funding_add messages.
	
	diff --git a/channeld/channeld.c b/channeld/channeld.c
	index 172660c6a..b0085ebc2 100644
	--- a/channeld/channeld.c
	...

For the updated commits, we'll need the first commit message for this, `df: port to new input/output dance`. I'm not going to walk through it, but I'll do the same for the other commit now. (It originates in a commit who's tagline is ``).

Once I know where these changes belong and that they're not in the same commit, we'll split the single fixup into two commits, which we can then apply to the two places where the problem originated.

We're going to want to `edit` this commit in the rebase history. Typically I do a `rebase -i`, mark the offending commit as an `edit`.

	$ git rebase -i 8adbd4d31eac37449d40a6a3ee207d4a4de3e188

This opens up a list of commits from HEAD to the passed in commit hash. My git editor is set as vim, so it'll open in vim. This a worksheet where you can interactively edit your commit history. Be careful here -- any lines that you delete will be lost from your branch, and will be pretty hard to get back if you lose/don't remember the commit hash.

Here's the relevant section of my rebase list.

	pick 8bfcd941e fixup: missing bracket
	pick 3be3df51d df: convert accepter_sigs to new pattern, add input check
	pick 8280a3a54 fixup: pass correct `am_funder` value
	pick f5d7f1d0b fixup! send_receive_funding_tx_info, use pointer
	pick ba715505e df: save incoming peer messages until we return
	pick 3dfeafa9d df: fixup, need to pass a not null in to to/from wire
	pick 1001fa1da Revert "lightningd/bitcoind: remove unused 'get_output' function"
	pick 29fb84ec0 bitcoind: Add typesafe version of gettxout
	pick e665d91f0 dual-funding: confirm scriptpubkey matches what's onchain
	pick 9ba12df8f fixup! patch up feature addition of v2 fundchannel


The commit we want to update is the the third one, `fixup: pass correct 'am_funder' value`. The bottom of the interactive rebase screen lists our options for how to change up this commit.

	# Commands:
	# p, pick = use commit
	# r, reword = use commit, but edit the commit message
	# e, edit = use commit, but stop for amending
	# s, squash = use commit, but meld into previous commit
	# f, fixup = like "squash", but discard this commit's log message
	# x, exec = run command (the rest of the line) using shell
	# d, drop = remove commit

We'll use `fixup` later. For now, we want to stop to `edit` this commit. All we need to do is update `pick` to `edit`. Like this.

	pick 8bfcd941e fixup: missing bracket
	pick 3be3df51d df: convert accepter_sigs to new pattern, add input check
	edit 8280a3a54 fixup: pass correct `am_funder` value
	pick f5d7f1d0b fixup! send_receive_funding_tx_info, use pointer
	pick ba715505e df: save incoming peer messages until we return
	pick 3dfeafa9d df: fixup, need to pass a not null in to to/from wire
	pick 1001fa1da Revert "lightningd/bitcoind: remove unused 'get_output' function"
	pick 29fb84ec0 bitcoind: Add typesafe version of gettxout
	pick e665d91f0 dual-funding: confirm scriptpubkey matches what's onchain
	pick 9ba12df8f fixup! patch up feature addition of v2 fundchannel


This will stop on this commit and allow us to make any changes we want to. Save and exit the interactive rebase document, and it'll execute the commands you've given it. When it reaches the `edit` command, you'll end up with a prompt like this one: 

	niftynei@granito:lightning$ git rebase -i 8adbd4d31eac37449d40a6a3ee207d4a4de3e188
	Stopped at 8280a3a54...  fixup: pass correct `am_funder` value
	You can amend the commit now, with
	
	  git commit --amend '-S'
	
	Once you are satisfied with your changes, run
	
	  git rebase --continue
	

When we run `log` we'll see that `HEAD` has stopped just after the commit that we wanted to update. We've basically gone back in time to that commit and can make any changes we want to the history. Once we play `git rebase --continue`, git will continue applying the rest of the patches listed in the logs until we reach back to where we started, at the branch tip.

Here's what my `git log` looks like.

	commit 8280a3a54efa1dcbb767f5f499e2ad86fde460d3 (HEAD)
	Author: lisa neigut <niftynei@gmail.com>
	Date:   Mon Dec 2 13:13:03 2019 -0600
	
	    fixup: pass correct `am_funder` value
	
	commit 3be3df51d80351b14120b2e6534bdd88d7d21e20
	Author: lisa neigut <niftynei@gmail.com>
	Date:   Mon Dec 2 13:11:42 2019 -0600
	
	    df: convert accepter_sigs to new pattern, add input check
	    
	    we're now using funding_signed2 and a commitment_signed instead
	    of the accepter_sigs method
	
	commit 8bfcd941ed988ca15e64068ce78bb45125f51119
	Author: lisa neigut <niftynei@gmail.com>
	Date:   Mon Dec 2 13:09:29 2019 -0600
	
	    fixup: missing bracket
	
	commit a5a14cb76a59a38110c854a96610e9065ea30756
	Author: lisa neigut <niftynei@gmail.com>
	Date:   Mon Dec 2 13:09:05 2019 -0600

Ok. We want to split the top commit into two different commits. To do this, I'm going to reset to the commit before it. That'll roll the project back to the previous commit, and move any changes in that commit back to unstaged. 

	$ git reset 3be3df51d80351b14120b2e6534bdd88d7d21e20
	Unstaged changes after reset:
	M       openingd/openingd.c


Alright, let's add the first change back. I'll use `git add -p` for this, as it'll let me precisely select the patch I want to stage for commit.

	niftynei@granito:lightning$ git add -p
	diff --git a/openingd/openingd.c b/openingd/openingd.c
	index 5b37dd7d4..d848cbac6 100644
	--- a/openingd/openingd.c
	+++ b/openingd/openingd.c
	@@ -1170,9 +1170,9 @@ static bool send_receive_funding_tx_info(struct state *state,
	                u16 num_ins, num_outs;
	                int type;
	 
	-               msg = opening_negotiate_msg(tmpctx, state, false);
	+               msg = opening_negotiate_msg(tmpctx, state, role == OPENER);
	                if (!msg)
	-                       return NULL;
	+                       return false;
	 
	                type = fromwire_peektype(msg);
	                switch (type) {
	Stage this hunk [y,n,q,a,d,j,J,g,/,s,e,?]? 

The answer is Yes, I want to stage this, so I hit Y. Then we quit, with `q`. We only want to check this first change in. Now when we run `git status`, you can see that some changes have been staged, but that there's still more to add. This is great and exactly where we want to be.

	Changes to be committed:
	  (use "git reset HEAD <file>..." to unstage)
	
	        modified:   openingd/openingd.c
	
	Changes not staged for commit:
	  (use "git add <file>..." to update what will be committed)
	  (use "git checkout -- <file>..." to discard changes in working directory)
	
	        modified:   openingd/openingd.c
	

I'm going to commit these now, with the info about which commit it belongs to.

	$ git commit -m "fixup! df: port to new input/output dance"

Now I add the other commit.

	$ git add -p 
	$ git commit -m "fixup! dual-funding: wire up opener side of dual funding"

Ok. We're done breaking that commit into two. Now let's finish off this rebase, so we can run a second rebase to apply the commits to the correct fixup. If we add the `autosquash` flag, it'll automatically place these commits in the correct place, and change the rebase action from `pick` to `fixup`.

	$ git rebase --continue
	$ git rebase -i 8adbd4d31eac37449d40a6a3ee207d4a4de3e188 --autosquash

Here they are moved to the correct part of the file, with their action updated.

	pick 83efa2bc8 dual-funding: wire up opener side of dual funding
	fixup 9f5c3acc2 fixup! dual-funding: wire up opener side of dual funding
	pick 30f6a536c fundchannel_complete: return 'txid' and 'remote signed' tx
	pick 70d61f8db df: verify that funding output not included
	pick 7cd71d312 df: port to new input/output dance
	fixup 4f1e3d908 fixup! df: port to new input/output dance
	pick 2183a2b42 df: include input info on witness data
	pick 6f829ad20 df: add remote's witnesses to unreleased tx object

All we need to do is save and close so the rebase can run. Viola! Mistakes successfully disappeared! Here's what the commit log looks like:

	83efa2bc8 dual-funding: wire up opener side of dual funding
	30f6a536c fundchannel_complete: return 'txid' and 'remote signed' tx
	70d61f8db df: verify that funding output not included
	7cd71d312 df: port to new input/output dance
	2183a2b42 df: include input info on witness data
	6f829ad20 df: add remote's witnesses to unreleased tx object

## As I stated before, don't fuck this up

I'd rate this as fairly advanced Git abuse. It's normal and expected that you might run into conflicts when doing this. If you're extremely surgical and tactical, you'll probably do pretty well (i.e. one line change per `fixup` commit), but from time to time you'll run into situations where moving commits around incurs conflicts with later patches.

The easiest thing to do in this case is to abort. Fucking up your git history during a rebase isn't impossible to come back from, but there's a good chance you'll lose some work or create a bigger mess to clean up than when you started. If it's really important not to lose something, `git rebase --abort` will end a rebase and reset your history back to before you started. As I stated at the beginning, the absolute safest way to do this is to checkout a new branch to do the rebasing and fixups in. You can compare the two branches at the end to guarantee that you haven't lost any changes.

If for some reason these warnings didn't save you and you do royally fuck your rebase up, get to know `git reflog`, the savior of git quagmires.


## In Exitus

Pefection is attainable. Don't fuck it up.
