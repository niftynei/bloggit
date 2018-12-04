timestamp: 1543434961
date: 28 Nov 2018
time: 13:56
title: Getting AMPed Up or Reflections on Lightning post Adelaide
tags: lightning, bitcoin, oss, edges

---

I've recently been thrust head first into my first open source software ecosystem. I love it; I also feel like I'm struggling to contribute anything worthwhile because I've been spending so much time just getting up to speed -- the particular subsystem of software that I've landed in is incredibly complex and has a bit of scattershot documentation, spread across a couple of mailing lists and two enormous projects.

I want to give some meta commentary on the mechanics of getting involved in a new, active space, and then give a more nuts and bolts overview of the considerations that are shaping the edge of Lightning at the moment. I'm sure I've left things out, so know that my list is just a subset of all the things.

## Finding Active Edges
There's a difference between getting up to speed and active in a currently evolving field versus learning a topic or subfield that's pretty much static. By way of example, I'd largely consider calculus and functional programming, as fields, to be pretty static, i.e. there's interesting stuff happening at the margins, probably, but there's not a lot of paradigm shifting research going into how to describe functionalism or what a second derivative is. As a field and practice, the borders of *meaning* and *scope* have largely been well defined.

'Active' spaces are different. They have action, or people actively working on new approaches or building out software and new ideas. The presence of people and the messiness of definition and conversation are beacons to what the interesting and new things the future will hold.

Arriving at an edge or beehive of activity where there are people working is like descending into a bit of chaos.  In an active field, there's usually a lot of independent research and motivations and interests that keep the actors on this edge a bit spread out. Figuring out where the edges lie is difficult because the definition of the edge is its lack of a roadmap. Sometimes you can find artifacts that strictly define at least a subset of those edges -- the wiki tracking decisions made at the Lightning Summit in Adelaide two weeks ago is one such example.

I was lucky with Lightning, in a lot of ways. The biggest one is that due to the team I joined, I have a lot of direct access to people that have been working on the edge of the space basically since the beginning (h/t to cdecker). The other is that I joined just in time to attend the latest spec update meeting. These meetings are rare -- the last one happened over two years ago in Milan for the first lightning spec.

I'm not going to talk directly about what happened at the meeting; if you're interested check out the lightning mailing list, where we're currently in the process of hashing out the decisions made at the summit (which you can see [here](https://github.com/lightningnetwork/lightning-rfc/wiki/Lightning-Specification-1.1-Proposal-States)), or take a look at the PRs currently in progress on the [lighting-rfc Github project](https://github.com/lightningnetwork/lightning-rfc/pulls).

Rather, I'd like to give some really meta impressions of what kind of thinking it takes to get involved in a project like Lightning -- hopefully this metaness will give you a portrait of what kind of conversations you need to be having or questions you should be looking to get answered when getting involved in a new field.

First off, it's hard to contribute to a field if you don't really understand the underlying system that it's operating on top of. Sure, this is easy enough to say, but just figuring out the contours of the system that define the problem space can be tricky. A lot of the stickiest problems that Lightning developers deal with, especially when looking to expand the protocol or improve the experience, are either limitations in the underlying Bitcoin protocol or a self-imposed mandate for privacy.  If you don't have a good grasp on the goals of Lightning with regard to privacy (keep it, as much as possible), or a pretty deep knowledge of how Bitcoin itself works, you're not going to be able to contribute much to the conversation around Lightning -- mainly because you're going to struggle to even understand, let alone communicate with, people who are already working in the space.

I'm an incredibly quick study, but still relatively new to the Bitcoin and Lightning space. My largest contributions to date can mostly be summed up as asking clarifying questions.  This may seem trivial, but I've come to see that it's an important contribution nonetheless -- comprehensibility is an incredibly important aspect of a system that needs and wants newcomers to both feel welcome to the space and able to contribute. And Lightning definitely could be more comprehensible!

##Into the Deep
With an eye to making the Lightning space a bit less opaque, I'd like to run through a few of the higher level considerations that seemed to come up with some frequency during the weeks leading up to and at the summit itself. I think it's safe to say that these themes will be continuing problems and on-going discussions in the Lightning ecosystem.

### Bitcoin
Bitcoin protocol limitations come in a variety of flavors. Here's a quick, condensed (and definitely contains omissions) rundown of things in Bitcoin that hold up or complicate Lightning feature development:

 - Fees. Lightning is a 'second layer' protocol, sure, but at some point it has to publish transactions on the Bitcoin blockchain. Lightning's security mechanisms (ie your ability to successfully pull your money out of a channel) rely on the ability to get a transaction into a block within a reasonable amount of time. Lately, this hasn't been a problem, but if and when fees spike, there's a lot of potential to run into trouble if your transactions aren't able to get confirmed.  Fees are complicated by the fact that 1) there's two parties involved in creating and spending all the transactions, 2) commitment transactions are usually composed, signed and stored long before you might actually need them, 3) economic incentives mean that you're probably looking to pay the smallest fee possible to accomplish what you want, but this means that you're probably in a bad position in terms of being able to get your transactions on chain in a fee spike event.  Lightning as a protocol would like to move away from the business of needing to know what the fees should be, but that means we're going to run into another corner case of the Bitcoin transaction ecosystem...  

 - RBF and CPFP. If you're not deep in the Bitcoin wallet management weeds, there's a good chance you've never heard these acronyms before. Briefly speaking, these are two mechanisms that the Bitcoin protocol provides for getting a transaction through that has largely been pushed to the back of the queue for being included in a block (mines/confirmed etc) because of a fee spike. RBF stands for Replace By Fee, whereby you basically re-issue a new copy of a transaction, but one with more fees per sipa[1]. CPFP means Child Pays For Parent. It takes advantage of the chained nature of Bitcoin transactions, and attempts to 'sweeten the deal' for miners such that they'll mine your first, low fee transaction in order to also be able to mine a high fee child transaction. The parent plus child chain is typically termed a 'package'.
 -  Schnorr. What is Schnorr?  Schnorr is a proposed change to multiparty signature composition. Including it in Bitcoin will require a revision of the signature verification mechanisms.In addition to more compact and easier to verify signatures, Schnorr unlocks a certain amount of obfuscation and script burying. Schnorr can make Lightning channel openings invisible on chain (right now they're a bit easy to spot[2]). There's a few other nice things that Schnorr signatures enable, that I don't exactly remember the details of, but they'll Lightning to send payments in parts more easily and securely[3]
 - Script Sighash Flags. Christian Decker's been spearheading an effort to update the way that Lightning balances are enforceable on chain. (The updated protocol is called Eltoo, you can read more about it in this high level [article](https://basicbitch.software/posts/2018-10-29-Explaining-Eltoo.html) I wrote, or the [paper itself](https://blockstream.com/eltoo.pdf), if you want something a bit more in depth.) This requires a change to Bitcoin script, specifically the addition of a new sighash flag called SIGHASH_NOINPUT[4][5]. Work on the new, improved state management protocol is basically stalled until this gets merged into the Bitcoin reference implementation. On another note, there's some other boutique, existing sighash flags that will probably start being utilized by Lightning transactions as part of the attempts to dodge the fee problem. Watch this space.
 - Transaction malleability. This is an ancient problem now in Lightning land, as it was resolved when SegWit landed. If you're going to be doing Lightning, you should know how SegWit works, as that's the only type of transaction protocol that Lightning wallets speak.  As a historical note, transaction malleability basically refers to how fixed the transaction hash is. Lightning, in its current form, *requires* the guarantee that the hash of a signed transaction can't be changed (by a miner or the other party etc).  SegWit fixed this -- it's practically never mentioned now. In other words, this problem has moved off the edge, largely because it's settled.

### Privacy
This feels like one that's taken for granted more than most things, but it largely informs a lot of architectural decisions that get made. Maintaining privacy is important, and it manifests itself in a bunch of ways. Here's a short list of things that privacy considerations impact.

- Error handling. How do you know who bungled your payment?   
- Payment correlation / decorrelation. Can an observer figure out if payments being sent over different channels or the same payment over different time periods, routes, are the same?  
- Getting a clear picture of current network health. It's hard to a payment success rate if the payments themselves are localized and unreadable  
- Autopilots. How much information should nodes reveal, to help other nodes figure out who to connect to?  
- Anything that might leak private or proprietary information including but not limited to: channel balances, node wallet UTXOs, payment origination, payment destination  

### Other assorted things
- Liveness. Payments can get stuck if nodes along the route aren't responding. This is particularly bad if a payment has to 'go to chain', ie be finalized via the blockchain. 
- Liquidity. Lightning payment capacity is a constantly mutating DAG. Channels' total value is known, but the balance of funds within that channel is often kept secret (see Privacy, above). This makes it hard to predict which routes will fail until you try it -- the advertised channel capacity may be pointing in the wrong direction. This is exacerbated by the fact that channel funding is one-sided at the moment. Splicing and dual-funding will help this problem.  
- How important *are* receipts? This deserves a much longer post and honestly I need to do more research around it; I won't get into it here.  

## In Exitus
I'm having a great time. 


[1] A sipa is another term for a kiloweight, which is a Bitcoinic way of weighting bytes in a transaction to calculate the fee rate of a transaction. As a general rule, miners prefer transactions with the highest fee rate per byte. If a fee rate spike is happening, you're going to want to up your transaction's effective rate.  
[2]  As an aside, we green lighted work on a different signature scheme (some 2 party single ECDSA sig algorithm) that can let private channels remain invisible on chain. Nice because it doesn't rely on Schnorr.  
[3] There's been a lot of discussion around AMP (base AMP, OG AMP, low versus high AMP). This deserves a longer discussion, but know that Schnorr sigs will provide a way to do split-payments with fewer drawbacks than any of the current proposals. In fact the coming of Schnorr is a background vibe underpinning a lot of the discussion, as it makes the timeline question more important.  
[4] I believe the final name is settling somewhere near SIGHASH\_NOINPUT\_UNSAFE for #reasons.   
[5] What's a sighash flag you ask? Briefly, it's a bit that's added to a transaction signature that tells the verifier what fields in the transaction that the signature signed. You can read more about them [here](https://bitcoin.org/en/developer-guide#signature-hash-types).  
