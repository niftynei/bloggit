timestamp: 1545980715
date: 27 Dec 2018
time: 23:05
title: Explaining Replace By Fee
tags: rbf, bitcoin, explainers

---

I apologize in advance to those readers of mine that have zero interest in Bitcoin. I'm personally quite absorbed with the project, and am hoping that by writing about it incessantly, I might be able to convince you to at least appreciate the project for its vast complexity, if not for the riches it might make you, if only you invest at the right time.

I'd like to spend some time today writing out everything I know about a small corner piece of the Bitcoin puzzle, a transaction replacement protocol colloquially termed "Replace By Fee", or RBF for short.

## A short description of the problem space

In order for a Bitcoin transaction to be considered valid, you must first have it included in a block by a miner. Normally, the way that would happen is as follows:

1. You compose and sign a valid Bitcoin transaction. I'm leaving the details out here, but think of it like a HTTP packet that is ready to be sent out across the network, if that's helpful.  
2. You broadcast your transaction out from your wallet, onto the Bitcoin network.
3. Other Bitcoin nodes on the network see your transaction and add it to their 'mempool'. This is the set of all Bitcoin transactions that have not yet been included in a block. They are candidates for inclusion.
4. A miner receives your block. The miner finds a winning hash that makes its block a block. Your block is now mined.
5. The newly mined block is transmit from the miner's computer to all the other computers on the Bitcoin network. 
6. Upon receiving this block, the Bitcoin node evicts all of the now-mined transactions from its mempool.
7. Rejoice. Your Bitcoin is Spent!

You may remember that the topic we're discussing today is known as 'Replace By Fee'. When, you might ask, in this sequence of events might you want to replace your Bitcoin transaction?

The answer is sometime between steps 3 and 4 above. After you've broadcast your transaction, there is a chance that it will be seen and mined by a miner. Once your transaction has been mined, you can no longer broadcast a new version of that transaction, as the inputs to it have now been marked as spent.

There are a few cases, however, where your transaction might get trapped or evicted from the mempool without being included in a block. One common case for when this might happen is when the number of transactions that are looking to be included in a block (ie the mempool size) is larger than the available blocksize. In this case, transactions tend to be processed or mined based on the feerate per kilobyte that they offer to pay the miner for their inclusion. 

If you've broadcast a transaction with a low feerate, and suddenly the mempool fills up with a lot of transactions that are looking to be included in a block, you may want to update your transaction to provide a higher feerate, so that your transaction will be confirmed in the next available block.

There's currently two mechanisms that people use to try to get their transaction included. The first is what we'll be talking about more in depth here, Replace By Fee. The basic gist of Replace by Fee is that you're rebroadcasting a previously broadcast transaction, but with a greater fee paid than the prior transaction.

The other strategy that wallets use to get transactions included in full blocks is called Child Pays For Parent, or CPFP for short. It involves issuing a new transaction, one that *spends* the earlier, still unconfirmed transaction. This second, child transaction will pay a larger feerate than it might on its own, with the hope that the now pair of transactions' total feerate will be high enough to merit inclusion in the next block. CPFP only works if the transaction you broadcast has an output that you can spend.

## RBF: The Existing Algorithm

Replacing By Fee replaces the earlier transaction that you broadcast in other node's mempools. That's where the replacing happens. There is a set of rules governing whether or not a transaction is eligible for being evicted from the mempool and replaced by a new one.  Here's a few things that the 'accept into mempool' code checks...

- The transaction that you're attempting to replace has flagged itself as eligible for replacement. This is flagged at a transaction level, but is retroactive for any as yet unmined inputs that you're spending. If any of a transaction's inputs, or it's input's inputs, are flagged as replaceable, then this current transaction is also considered eligible for replacement. If a transaction or any of its parent inputs are not marked as replaceable, any transaction with an input conflict (that is they'd be spending the same inputs) is rejected with the error "txn-mempool-conflict".  

- Requires that all inputs already exist in the UTXO set. No currently unmined inputs are allowed in a replacement transaction. This is a tighter rule than the desired one, which is to check that the replacement doesn't require 'low fee junk' to be mined first. You can avoid this by rejecting any replacements that aren't using already mined inputs.  

- A replacement candidate must pay more in fees than all the transactions it replaces. The rationale for this is that sending transactions across the network consumes bandwidth. The higher feereate of the new transaction, in theory, pays for its increased usage of bandwidth: once for the original broadcast and then again for every subsequent replacement. Note that the nodes keeping and broadcasting this transaction don't get paid -- only miners do. In that sense the fee is more of a social justice than a net payment to every node that sees the transaction. 

Note that this is in _total_ fees, not fee rate. Any replacement transaction must pay more in total fees than the entirety of any and all transactions that the replacement would displace from the mempool. There's the potential that you'll be replacing an entire "package" of umined transactions, a parent-child chain of transactions that are looking to be mined. If you're a small transaction and you're trying to replace another who has an extremely large sized child also in the mempool, your effective fee rate (roughly calculated as the fee paid per byte of transaction that is included in the block) will be much higher than the original as you need to cover a larger amount of fees with a smaller number of bytes.

- Finally, if the 'package' of transactions that you're looking to replace numbers greater than 100, your transaction replacement won't be added to the mempool. In other words, if someone has attached 99 transactions onto the transaction you'd like to RBF, you're shit out of luck. You'll have to wait until there's enough room in a block for your original to be mined.

## Proposed Changes

Russell O'Connor published a proposal to change how the RBF rules work, at least two of them. The proposal would update the total fees rule. Instead of a replacement needing to beat the absolute fee amount of all transactions that it would be replacing (aka the "package" of transactions), it'd only need to be beat the effective feerate of the original. Additionally, the proposal would amend the 4th rule, such that the fee on your replacement is at least as much as the `minrelayfee` on the total package you're looking to displace from the mempool.[1]

Why is `minrelayfee` used as a minimum? A transaction that's replacing a larger set of transactions removes already transmitted bytes from the mempool. This rule change makes sure that the replacement transaction 'pays' for the cost of relaying those removed bytes.

Ok this is all pretty tedious. Let's take a look at some examples.

## Miner Incentives, A Consideration

There's two cases that we should consider: a larger transaction wants to replace a smaller transaction (small txn -> larger txn) and that of a smaller transaction replacing a larger set of transactions, or package (large package -> small txn).

### Current Rules
*small txn -> large txn*: Rule 3 stipulates that the total fees must be greater, with no regard to fee rate. In practice, no replacement is accepted if it lowers the total feerate of the mempool. ([source](https://github.com/bitcoin/bitcoin/blob/bccb4d29a8080bf1ecda1fc235415a11d903a680/src/validation.cpp#L789)). In practice, this shouldn't happen anyway. The motivation for RBF'ing a transaction is that the block inclusion feerate cutoff has spiked -- replacing one transaction with another larger one with a lower fee rate makes it less, not more, likely that your transaction will get mined in the next block.

*large package -> small txn*: The smaller transaction must pay more total fees than the existing package. The miner doubly wins: they're making the fees of a large transaction in a smaller byte footprint.

### Proposed Rules

*small txn -> large txn*: Miner's choice strictly improves. The fee rate per byte that they're including has increased and the net fee of the new, larger replacement transaction is greater. This is no change from the current scheme.

*large package -> small txn*: Miner's choice also improves. Although the total fee that they will make for mining the smaller replacement transaction is net-net smaller than the fees the entire large package would have earned them, given a competitive environment for blockspace (ostensibly why the RBF was triggered in the first place), the smaller transaction with the higher per byte fee rate is more likely to be mined than the larger, lower fee per byte package it's replacing. The incentives of the miner (highest fee per block byte) and the RBF'er (having the transaction confirmed for the lowest reasonable fee) align.

## Wherein We Contemplate a Word Problem

Let's take a closer look at the *large package -> small txn* case, as that's clearly the one where the proposed rule change has the greates impact.

A 1ksipa size transaction with a 10ksipa sized child transaction is in the mempool. The current feerate on the block is 2 satoshis / sipa[2]. The total fees that these two transactions, or package, pay is 2ksat + 20ksats = 22ksats.

Under the current scheme, a replacement transaction of size 1ksipa would need to pay at least 23k satohis, a feerate of 23 satoshis / sipa. This is an 11.5x increase in feerate from the original package's rate of 2 satoshis / sipa.

Under the proposed scheme, a replacement transaction of size 1ksipa would need to pay 12k satoshi in fees in order to replace a set of transactions of size 11ksipa. The effective feerate on the replacement transaction is 12 satoshis / sipa, a 6x increase in feerate above the package it's replacing.

The proposed ruleset strictly improves the feerate of the mempool, while lowering the fee ceiling for replacing a large or weighty transaction.

## Notus Commentarius

RBF mechanics closely resemble that of an auction, where the rules for replacement are actually the next price that the auctioneer will accept a bid at. The current rules set the floor for the next bid to be extortionately high if the number of bytes you're looking to replace is quite large. Russell's proposed rule change lowers the bid floor to a more reasonable metric.

One of the largest arguments against changing the replacement fee rules, as far as I can tell, hinges on the argument that without a fee hike, anyone could spam the network with RBF requests, creating mempool churn and eating up network bandwidth. I'd argue that *any* RBF mechanism leaves an opening for this style of DoS attack on a node. The difference between these two proposals is not the mechanism, but merely the floor cost for waging such an attack -- at some point your transaction will be mined and the fees you've offered up will be paid. Further, the only case where this attack would be truly expensive is in the case where they're looking to replace a large number of bytes in the mempool -- perhaps that truly is the most likely DoS attack vector, however.

Thanks for sticking with me! Hope you enjoyed learning more about how mempool transaction replacement works! I left a few things off, but the main gist of how RBF works is all here. 


[1] Russell O'Connor's [proposed RBF rule changes](https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2018-February/015717.html) (source Bitcoin ML) vs [BIP125](https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki), the current RBF rules.  
[2] A sipa is a byte/weight measurement. For simplicity's sake you can consider a sipa to be a byte.

