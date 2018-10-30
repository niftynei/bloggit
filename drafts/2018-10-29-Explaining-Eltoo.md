timestamp: 1540866052
date: 29 Oct 2018
time: 19:20
title: Understanding Eltoo
tags: bitcoin, lightning, eltoo, explainer

---

## Simplified Channels, Simply

This article assumes base knowledge of the existing Lightning Network contracts and Bitcoin transaction composition. This is a lot of base understanding to have, and in fact, I'd argue that it's probably the biggest challenge to fully understanding what eltoo is really getting at.

That being said, I'll do what I can to explain it such that it's understandable.

Let's start by first understanding how the existing Lightning network contract invalidation system works.

The original Lightning protocol relies on a series of half-signed transactions. When the channel balance needs to be updated, you exchange a new set of half-signed transactions that update your balance. In order to keep your channel partner from broadcasting an old, invalid transaction that you've signed, every time that you exchange a new, updated transaction that reflects the current state of the payment balances, you also exchange a 'penalty' transaction, of sorts, that allows you to claim all of the Bitcoin in the channel, if the other person in the channel accidentally or intentionally publishes an old transaction state.

Each of these exchanged transactions spends the same output -- the one created by the Funding transaction.

It'd probably be useful to spend a bit of time here talking about how Bitcoin transactions work, as it'll be handy when we get into eltoo.  Every Bitcoin transaction is a global state update. It takes existing, unspent output objects, spends them by providing a signature that proves you can spend them, and creates new unspent output objects. The set of previous outputs that your Bitcoin transaction "uses up" are called inputs. Every input is another, previous transaction's outputs.

Let's bring this back to the Funding transaction then. A funding transaction has a single output. This output can only be spent by providing two signatures, one from each party in the channel. This is called a 2-of-2 multisig transaction. The funding transaction is committed to the Bitcoin blockchain, which then makes this Funding output eligible to be spent by the channel parties. The only way these funds can be spent is if both parties sign a transaction. The channel balance is updated, then, by creating new, ephemeral transactions that spend this output, re-apportioning the total value in the channel to each party as a reflection of their current balance. 

As a concrete example, let's say you and I wanted to create a Lightning channel between ourselves. I'm going to offer up 2 Bitcoin, you're putting in 1 Bitcoin. We'd make a funding transaction that takes two inputs: my 2 bitcoin and your 1 bitcoin, and creates one output of 3 Bitcoin. This 3 Bitcoin can only be spent by a transaction that has both of our signatures on it.

To record what the original balance is, we'd create a transaction then that has, as an input, the 3 Bitcoin funding transaction result, and that pays out two outputs: one to me for 2 Bitcoin and one to you for 1 Bitcoin. It's a lot more complicated than this, but for the sake of understanding how eltoo works, this simplification will suffice. The whole point of Lightning is that you and I can now Do Business between each other. I buy you lunch, worth 0.25 BTC. Rather than paying me back with Square Cash or Venmo, we could just create a new transaction that spends the funding transaction, throwing away or invalidating the first one that we exchanged. The new, updated transaction would reflect the new balance of accounts between us: it'd pay me out 2.25 BTC and you'd get .75 BTC.

The problem is that the first transaction we exchanged, with the original balance values, still exists. In it, I get just 2 BTC and you still get your original 1 BTC. Let's say that you decide you'd like to stiff me the lunch I bought you (jerk), so you publish the original transaction onto the blockchain. I wouldn't be able to publish the later transaction that actually reflects the balance between us, because I'd also be trying to spend the same output from the Funding transaction. You can't do this -- only one Bitcoin transaction can spend a single output. So I'd be shit out of luck.

The original Lightning proposal solves this problem of past state transactions getting published by introducing a concept of penalties. Without going into too much detail, it effectively gives me the ability to penalize you for reneging on our lunch deal, by spending a special output from the stale state transaction that you published. The penalty for your actions is built into the outputs of the state transaction, and basically gives me the ability to take all of the Bitcoin in the channel for myself. So the punishment for trying to take back your .25BTC is a total loss of all of your channel Bitcoin. 

Crime doesn't pay, at least not with lightning.

Every time we want to update the balance of accounts in the channel though, we need to exchange new penalty transactions, that invalidate the previous state. Or not really invalidate it, but provide a huge disincentive for you, if you decide to publish it anyway. Half of the security of the system, then, relies on you and me saving all of the penalty transactions that we exchange, because they map 1 to 1 to expired or invalid transactions. If you lose the penalty transaction for a particular old, invalidated state, and for some reason the other party finds out that you've lost it, they can publish that old transaction and you wouldn't be able to do anything other than accept your loss. 

In in that way, Lightning, as it exists today, largely resembles a practical implementation of the theory of guaranteed mutual destruction. If you lose or reveal your nuclear arsenal (in this case, a set of transactions that invoke penalties for unfair actions on behalf of your adversary aka channel partner), you're shit out of luck.

As any Soviet-era super power knows, nuclear arsenals are costly to maintain. Here's where eltoo comes in. eltoo is an elegant proposal to do away with private-arsenals of penalty transactions. In fact, eltoo does away with penalties entirely. Rather, it provides an elegant mechanism for allowing any later agreed upon state to override any previously agreed upon state. As long as you have a copy of the most recently agreed upon transaction, you can publish it any time and it's guaranteed to be spendable.

The key to this is being able to decouple a transaction from any specific output. The original Lightning transaction scheme relied on all transactions spending from the Funding transaction. Instead of pegging a signed transaction explicitly to a prior one, signed transactions can spend any transaction for which it has a valid spend script. These types of transactions are called floating transactions.

This is huge, because it gives you the ability to 'fix' the channel balance. Previously, if your channel partner published a stale balance transaction, you couldn't do anything to 'fix' it because all of the existing state transactions that you have spend the same output: the funding transaction output. With a floating transaction, however, you have the flexibility to spend either from the funding transaction, or from any previous state transaction. 

Let's go back to the previous example. I've bought you lunch, the most current transaction that we share between us says that I get 2.25 Bitcoin, you get .75 Bitcoin. You decide to publish the older transaction, where you get 1 Bitcoin and I get 2.  The transaction spends the funding transaction output. In the original Lightning scheme, I can't fix this because I all of the transactions that I have must spend from the funding transaction, and the funding transaction's single output has now been spent, by you. With an eltoo floating transaction, I can broadcast the most up-to-date transaction, spending from not from the funding transaction output, but from the old state transaction that you've just published. This flexibility as to which transaction you're spending is what makes eltoo so elegant. There's no need for punishment, because old state updates are fixable, you just spend them again, with the most up-to-date balance, ideally.

How does eltoo do this? By removing the concrete identifier of an input to a transaction. To do this, you'd construct a transaction using a the flat SIGN_NOINPUT, which means that the signature doesn't include the unique identifier of the input it's spending. Currently, this isn't a part of the Bitcoin spec; there's a [proposal out](https://github.com/bitcoin/bips/blob/master/bip-0118.mediawiki) for it's inclusion.

Once a transaction can spend any other transaction in a channel though, what's to keep your cheating partner from just over-writing the correct channel balance with another, older transaction?  eltoo solves this in a hackishly elegant manner, by repurposing the nLocktime field that already exists as a part of the transaction format. The locktime field already serves a dual purpose: it either limits the spending of this transaction by a required blockheight, or by a timestamp. If the locktime is beneath 500k, it assumes that it's a block height lock. Anything above this is a timestamp lock. Any number above 500k but beneath the current time, then, can safely be used as a series number for a set of eltoo channel transactions, as they will be immediately spendable. Eltoo transactions can be ordered by locktime. Update transactions are configured such that they can only be spent by a transaction that has a higher locktime than their own, thus preventing an earlier transaction from overriding a later, committed transaction.[1]

eltoo is incredibly elegant in its simplicity. Floating, ordered update transactions obviate the need for arsenals of penalty transactions. They also do away with the need for secrecy -- any update transaction is valid and publishable. This greatly reduces the memory overhead needed for each channel that a lightning server maintains, as old state update transactions can be safely discarded.

There's a bit more nuance to update and spending transactions that I've largely glossed over. You can read more in the [eltoo paper itself](https://blockstream.com/eltoo.pdf). There's a lot of other really nice features that eltoo adds, like making multi-party channels feasible, and a better mechanism for dealing with fee spikes.

As it stands currently, eltoo won't be possible until the SIGHASH_NOINPUT flag has been added to the spec, but I'd be surprised if it isn't included within the next few months to a year.

For further reading, on the original Lightning spec, see Poon and Dryja's paper, [The Bitcoin Network, Scalable Off-Chain Instant Payments](https://lightning.network/lightning-network-paper.pdf).

[1] The key to understanding how this works is to know that the CHECKLOCKTIMEVERIFY doesn't compare with the actual time, but rather to the nLocktime specified in the transaction. [See BIP65](https://github.com/bitcoin/bips/blob/master/bip-0065.mediawiki#credits).
