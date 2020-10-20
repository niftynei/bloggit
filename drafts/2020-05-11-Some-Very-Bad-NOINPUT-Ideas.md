timestamp: 1589210076
date: 11 May 2020
time: 10:14
title: Some Very Bad NOINPUT Ideas
tags: bitcoin, protocol, NOINPUT, ANYPREVOUT, fanfic

---

I spent some time this weekend groking the [NOINPUT proposal](https://github.com/bitcoin/bips/blob/master/bip-0118.mediawiki). If you're new to Bitcoin, it's a fairly technical change as it happens in a pretty niche yet important part of the transaction signature system.

First, I'll try to briefly explain the part of the 'signature stack' that the NOINPUT proposal effects. Then we'll get weird and go through a few absolutely terrible (citation needed) ways that you could use this new functionality.

I'm not actually going to cover the good use case, you can read more about the eltoo proposal, which relies on the NOINPUT sighash flag, [here](https://blockstream.com/eltoo.pdf).

## Where NOINPUT fits in the signature stack

### But first, a short illustration of what a digital signature is
Generally speaking, when you 'create a signature' there's usually a document that that signature is attached to. In normal paper contracts and the like, your signature is some ink that you've personally put down onto a physical paper in a hopefully hard to replicate manner. Anyone can look at the document with the ink doodle you drew on it and say "ah, yes! This is in fact a doodle drawn by Georgina" and that makes the document valid, because it shows that Georgina has consented to what's written on the document.

In the digital world, we don't have paper and ink doodles that anyone can look at and say "ah yes! Georgina did this". But we still need a way for people, like Georgina, to express their consent about *digital* documents. This need for 'digitalized consent marks' led to the development of cryptographic signatures, which is basically the production of some extra 'metadata', let's call it, that accompanies a digital document, much like an ink signature rides on the paper of a real world contract.  This 'metadata' is really just a number, which you can put into a fancy math equation, along with another number called 'the users public key' and 'the document' the signature is for and if the math equation equals out, you know that the 'metadata' is in fact a valid signature.

So digital signatures are mathematically verifiable, instead of the ink doodle version which relies on you recognizing and comparing previous handwriting samples of the person in question.

Note that the signature verifies a document still -- the actual digital object that the 'signature metadata' accompanies.

What is in this 'digital document' matters -- if you attach a digital signature to the wrong document, the math equation will come out wrong because your inputs are wrong.

Ok, that seems ... straightforward enough. In bitcoin, there are signatures. Which means that, at some layer, there are 'messages' that those signatures are signing. The question is what is in the message that the signature signed?

Well, it's definitely going to be parts of the bitcoin transaction. But what parts, exactly? There's a bunch of fields in a bitcoin transaction. We need a standardized way to communicate which fields of a transaction were included in the message that produced the signature. 

"What fields from a transaction were included in the message that this bitcoin signature signed" is the problem that 'sighashes' solve.

## NOINPUT

Anyway, you should read up on sighashes if you're into that kind of thing. NOINPUT is a 'modifier' which adjusts which fields of a transaction are included in the signature -- specifically it makes it so that you don't commit to the previous transaction output that you're spending.

See, most signature hashes include the txid and vout of the UTXO they spend; NOINPUT specifically leaves all of this out. The only thing that you do sign about the UTXO that you're spending is the amount of bitcoin that it contains.

Ok so, just to recap. A 'normal', non NOINPUT signature, exactly specifies the UTXO that it's spending. A NOINPUT signature, on the other hand, doesn't. Instead of saying 'I must spend exactly this UTXO', it allows you to spend any UTXO that meets the following criteria:

  - it is for exactly the amount specified (a NOINPUT signature commits to the amount)
  - the public key that that UTXO is locked to matches the key that signed the NOINPUT signature


So if I give you a transaction and a signature for that transaction, but my signature includes the NOINPUT flag, that means that any UTXO that has a valid locking script and amount can be slotted into that transaction.

## Let's Get Wicked

Here's a few terrible ideas about how such a signature could be used.


### Bad Idea One: An Inifinite Subscription Service

You're a magazine vendor who'd like to allow subscribers to pay you every time a new issue comes out, once a month. You send the new subscriber an address to pay to, and they send you back a transaction with no inputs and a NOINPUT signature that covers the amount. Whenever a new magazine edition comes out, the subscriber creates a UTXO locked to the pubkey that signed the NOINPUT sig they gave the magazine company at signup. The magazine company can spend this UTXO by using the transaction and signature they've gotten. If the signature is `SIGHASH_SINGLE|SIGHASH_NOINPUT`, then the magazine company can add additional outputs and inputs to cover the transaction fees.

Once the magazine subscriber has successfully processed the payment ie spent your UTXO, they send you the latest issue.

#### The Good

- infinite subscription! As long as you keep paying, you're still subscribed.
- lightweight comms! There's no need for the subscriber to ever cancel or re-contact the magazine company. You just stop issuing payment to that pubkey.
- no prepayment! Other locktime related payouts require you to commit a lot of money upfront for such a scheme. But here you only pay the funds when there's a new issue. 
- reversibility! If the magazine subscriber goes defunct and stops claiming the UTXO's you've produced, you can simply spend them elsewhere.

#### The Bad

- privacy! You're spending to the same pubkey every month; the magazine subscriber is re-playing the same transaction every month.
- bookkeeping! since the magazine company is re-playing the transaction, unless it's modified with additional payments, the txid won't change.
- accidental loss! If you ever send the exact subscription amount to that pubkey and don't intend for the magazine service to spend it well you're shit out of luck. The amounts have to match exactly what you gave them the signature for though.
- price is fixed! There's no way for you to easily renegotiate a price change without the magazine company contacting you to get a new signature.

#### The Alternatives
- The magazine publisher gives you an HD wallet pubkey seed path that you pay to every month.
- You use the as-of-yet unfinished lightning offers proposal to set up a recurring lightning payment.
- You give the magazine publisher your credit card number and they charge you whenever they want.


### Bad Idea Two: Let's Run a Lottery!

You want to run a raffle for 100 friends. You produce 100 pub/priv key pairs and put them into a hat. Each friend then gets assigned one of these pubkeys and is issued a transaction and NOINPUT signature for that pubkey. Maybe they pay you a little bit of money in order to be in on your raffle. Who knows.

Through some totally trusted TM mechanism, you randomly pick one of the 100 pubkeys out of the set and publish a transaction that puts that UTXO out onto the chain. The winner has the transaction that can spend it, so they do! Huzzah, someone won the raffle!

#### The Good

- instant winner! Who doesn't love money suddenly appearing on the blockchain that they can win?
- 'raffle tickets' are actually tangible! It feels good to have a physical 'ticket' that you can redeem if your winning number is published
- potential for a transparent lottery selection process! I'm not exactly sure how this would work and you could make it trusted but it's an ok idea. It seems like you might even be able to setup a service where the raffle ticket payments get aggregated into the output, like an actual lottery where the ticket sales end up being the lottery pot. But I'm not 100% sure there's a trustless way to do this. Maybe blinded something is the answer? Maybe you could already have published the UTXO which is somehow verifiable from the 'lottery ticket oracle', but you have to keep hitting it until you get the winning signature. That might be fun.

#### The Bad

- no guarantee it'll pay out! You paid someone some money, who's to say they won't just run away with the pot?
- no way to verify that the winner is 'randomly' chosen. The lottery ticket producer is an 'oracle', how much do you trust it not to just send out the right signature to some guy who paid the lottery maker a kickback? I don't know man, this whole thing seems a bit fishy.

#### The Alternatives
- Buy a lottery ticket and lose your money that way
- I think I once saw a fancy lightning service idea that involved HODL-invoices to create a lottery payout, but maybe that was actually a dutch auction. Different thing.
- I hear there's some Ethereum token that randomly pays a member of a savings pool the interest payment. Maybe try that?

### Bad Idea Three: Inheritance Planning

You want to send some money to your heirs but you don't want to give them your secret keys while you're alive. You also don't want to put your secret keys into any place where anyone could possibly get to them. Instead, you get your heirs to get their own wallet and private keys set up. They create a transaction that pays out to them, and you sign it with NOINPUT, for a UTXO that doesn't yet exist.

Since NOINPUT signs the amount of the UTXO, you're going to need to know the exact amount of money that your heirs are getting, as that's a part of the signature. You could have a service set up that just emails them a new signature and updated transaction every time that your net-worth on chain changes.

You're also going to need a way for, upon death, all of your assets to get paid out to the UTXO that your heirs can claim. Maybe you do it on your death bed. Maybe you invest in a deadman switch that automatically pays out to them when you stop breathing or hitting a button every two weeks. There are options here, but you do need a way to get that final UTXO on chain, so that they can spend it.

#### The Good

- no need to share private keys! Forget about making sure that others know how to reconstruct your private keys! Since they can claim them as soon as you pay out to them, the bitcoins will live on beyond you without secret sharing.
- pretty good privacy! Since the NOINPUT transaction is completely offline, there's no way for anyone to know what your future intentions with the coins are. Unlike vaults or other schemes that require published locking scripts, cached NOINPUT sigs are private until used.

#### The Bad

- constant updates needed. Since NOINPUT signs the amount of the issued UTXO, if for some reason your net-worth of bitcoin changes but you don't issue an update, it makes the signatures that you issued completely worthless. Whoops.
- deadman switch has gotta work. If you die and the payout UTXO isn't created, then you're back to being screwed. One way to mitigate this might be to have a tx that gets created and stored with your cold storage keys that just needs to be broadcast to activate it. But if your cold storage is findable then they'll have your private keys anyway so there's no point in the NOINPUT scheme. Having someone find and publish the transaction that pays out to your relatives though seems a lot less terrible than having them find your secret keys though so maybe you just make that transaction a little easier to get to.

#### Alternatives

- Some form of [vaults](https://hackingdistributed.com/2016/02/26/how-to-implement-secure-bitcoin-vaults/)
- [Shamir Secret Sharing](https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing) and/or multisig script solution to spread your secret key seed to friends in a very horcrux like manner. You pay all your bitcoins out to these multisig scripts while living, so that if anything happens to you at any point, you heirs can reconstruct your keys and recover your vast riches.
- Bury a [cryptosteel](https://blog.lopp.net/metal-bitcoin-seed-storage-stress-test/) with your seed phrase in the backyard and leave a treasure map to it in your will.


### Bad Idea Four: The Marie Antoinette Balcony Coin Dump

This one's for all the chaos causers. You create a `SIGHASH_NONE|SIGHASH_NOINPUT` signature for a pubkey and amount, which you make public. At random intervals, you publish UTXO's to that pubkey.

Mayhem ensues as the hoi polloi compete to be the first to get their transaction mined to claim the funds you've just released for poaching. It's like that scene where the aristocrats randomly decide to throw thousands of liras off their balcony onto the impoverished masses below. You can do it at any time, and anyone who knows how to write a bitcoin transaction and attach a signature can claim it. They'd just want to make sure that it pays out to an address they control, as any such transaction becomes pretty much replayable (assuming that there's no other inputs/signatures on the transaction).

It's like groundhog day but for money raining from the sky!

#### The Good

- mayhem! chaos! Watch as a whole ecosystem of chain watchers and transaction mining fast-track industry pops up around the concept of claiming this freely tossed digital gold

#### The Bad

I can't think of a single downside to this idea.

#### Alternatives

- Use a `OP_TRUE` script and just publish money onto the blockchain that anyone can claim at will. It's a little bit of a different scanning strategy but basically the same idea.


## In Exitus

What other terrible ideas are there for NOINPUT? Surely you can do worse.
