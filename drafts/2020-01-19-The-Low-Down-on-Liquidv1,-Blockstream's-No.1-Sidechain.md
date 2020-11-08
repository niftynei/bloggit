timestamp: 1579469540
date: 19 Jan 2020
time: 15:32
title: The Low Down on Liquidv1, Blockstream's No.1 Sidechain
tags: liquid, blockchains, bitcoin, sidechains

---

Let's talk about Liquid, Blockstream's semi-proprietary sidechain[1], lightning and how they interop with bitcoin. If you're anything like I was a year and a half ago, you may be fairly comfortable with bitcoin at a high level, but not quite understand where and how Liquid and Lightning fit inside of that. This brief article is for you, past self.

From a super high level, Liquid and Lightning are software projects that operate on top of pooled bitcoin.

Both of these projects have very similar underlying principles, but different ways for accounting for the money in the 'bitcoin pools' that they create.

I consider lightning to be the simpler case of this, since lightning 'channels' only concern two parties. The basic idea is that two people who hold bitcoin decide to put that bitcoin into a contract, or bitcoin transaction, such that a shared pool is created. The money in the shared pool can only be spent if both parties agree to spend it. A parties' agreement is demonstrated by signing a transaction that spends the jointly pooled funds. The transaction that creates the 'pool'[2] is published to the bitcoin blockchain. Any transaction that spends from that shared or pooled transaction will require both parties' signatures. If you're a party to this contract, you don't sign any transaction spending the pooled money unless you agree to how much that transaction pays you. Ideally, you've been keeping track of how much of the money in the shared pool belongs to you, so you can check that when someone asks you to sign a transaction that pays out from the pool that you're getting the appropriate share.

## Lightning Fast Lunchbox Poker
Ok, so lightning is two people with some bitcoin who want to pool it together. What do these people do with this pool? Well, they basically create a 'napkin ledger' that records how much of that pool belongs to each person. Let's use a card game with a buy-in as an example. At a casino, you give your money to a cashier and they hand you a bunch of chips. You then take those chips to a poker table, and play poker. At the end of each round of play, the chips get redistributed to each party at the table depending on how they did that round. 

Lightning is like a round of poker between two friends, but instead of chips you put the money into a lunch box that your friend Joe keeps track of. Joe will only distribute the money from the lunchbox when he gets a napkin with both of your signatures on it, saying who gets paid what amount from the money in the box. So the two of you play a very boring two player game of Texas Hold'em. At the end of each round, you get a new napkin, write down the updated balance, sign it, and then tear up the last napkin (so that neither of you can take an old napkin to Joe and get more than is currently fair).

Lightning channels work like this, except instead of Joe's lunchbox we use the bitcoin blockchain, and instead of napkins we use unpublished bitcoin transactions, and instead of tearing the napkins up there's something called a revocation token that makes it such that if anyone publishes an 'old napkin', the other party can go and take all of the lunchbox money for themselves, as penalty for you cheating.

## Welcome to the Liquid Casino
Liquid is more like the casino where there are chips and instead of there being Joe with a lunchbox, there's a whole office with a cashiers window and multiple tellers that will change your hard money into red and green and black chips. In this case the cashiers are the members of the Liquid federation. They run special hardware boxes with special keys that make them part of a hardcoded signature set. Anyone can pay money into liquid, but you have to put it into a contract where the only people that can spend it again is by going to a cashier's window to cash out[3].

Instead of using napkins to keep track of who owns what and what their balance is, in this casino of pooled money, Liquid uses its own blockchain. Every movement of chips between players at the casino[4] is recorded in a transaction on this secondary chain. Just like at a casino, none of the chip movements really matter to the larger pool of cash outside of the Liquid casino, except that everyone in the casino knows that you can go to a cashier and get money for them (bitcoins in this case), so it really is as good as cash. Unless you try to buy a sandwich with them, in which case, well good luck.[5]

Since Liquid is a blockchain, and it's *not bitcoin* there's a few differences in how exactly the chain gets built or made. In bitcoin, you need a bunch of people running proof of work algorithms to figure out what the next block will be. In Liquid, since there's only a few cashiers at the windows, each of the cashiers takes a turn deciding what the new block will be. If you're a cashier and it's your turn to make a block, you get to pick what transactions go into it. You just bundle them up and then sign it, and send it out to the other cashiers who look at who's turn it is to make a block, check that the signature belongs to that person and that it builds upon the last block in the chain, and add it to their copy of the liquid chain. Then the next cashier does the same, etc. Blocks in liquid are issued every minute; this is a convention rather than a probability function like it is for the bitcoin chain.

In Liquid vocabulary, "putting money into the casino and getting chips" is known as "pegging-in". Taking your casino chips to a cashier and getting paid bitcoin back is known as "pegging out". When you understand that the liquid money pool is the set of transactions in the bitcoin blockchain that have all paid to a smart contract that can only be unlocked with a certain threshold of the cashier's (federation member's) signatures, suddenly it makes sense why [anyone can peg-in](https://twitter.com/jb55/status/1217997942209990657?s=20) but you have to talk to a cashier to peg out. 

(In case it's not obvious, you peg in by creating a bitcoin transaction to a special address. Anyone who owns bitcoin can do this, thus anyone can peg in to liquid.)


### Other Liquid Features
Liquid also does other fancy things like confidential transactions and allows you to issue new assets[6]. Assets on Liquid aren't pegged-in in the same way that bitcoin is, so who has them and how you get more of them and how many there are of them might just be a Liquid network thing, but it also might be a bigger wider thing, like the Tethers on Liquid that are part of a larger ecosystem. I'm not really going to talk about these here because they're not really part of the pooled bitcoin stuff. If you want to learn more about how liquid actually works, I'd recommend Blockstream's [technical overview](https://docs.blockstream.com/liquid/technical_overview.html). If you want to run a liquid node, the Elements project [tutorials](https://elementsproject.org/elements-code-tutorial/installing-elements) are where you'll want to end up. The open-source software that can run a liquid sidechain is called "Elements" for reasons[7]. In theory, anyone can run their own federated chain using the Elements project, Liquid is just one of the existing options. I'd recommend this [simple config file](https://gist.github.com/niftynei/455223f720bb70f49cae2b7fd3a5d94f) for an elements node if you decide to run on the liquid chain.


## In Exitus
That's it bitches. We've pretty much covered lightning and liquid's relationships to the bitcoin blockchain.  Seem simple? This is one of those things that I'd call very 'simplex', because it's simply complex.



[1] Disclaimer: Blockstream pays me salary.    
[2] The way you do this is simple: you create a 2 of 2 multisig outputs. The only way to spend a 2 of 2 output is by first getting both party's signatures.    
[3] There are plans to make it so you anyone can cash out at will, but right now you have to go through a cashier. This is for security purposes, and makes sense when you think about it.    
[4] I imagine, if there were a Liquid Casino, their tagline would be "let's get liquid!" but who knows. Hard to say, really.    
[5] BTCPay server just added Liquid to its set of things that it will accept, so the casino is expanding quite rapidly. [Reddit discussion](https://www.reddit.com/r/Bitcoin/comments/ep9dha/announcing_liquid_network_support_for_btcpay/)    
[6] Watch this space for BitchCoin. #BitchCoin2020    
[7] I seem to remember someone telling me it's because the Elements Project is a collection of building blocks, or elements, for a coin ecosystem. This is unverified.    
