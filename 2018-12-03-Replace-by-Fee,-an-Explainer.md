timestamp: 1543893495
date: 3 Dec 2018
time: 21:18
title: Replace by Fee, an Explainer
tags: bitcoin, rbf, explainer

---

Replace by fee is one of the mechanisms that can be used to bump the fees on an existing transaction in the mempool, to improve its chances of being mined in a block.

## Existing algorithm
Things that the 'accept into mempool' code checks...

The transaction must be flagged to be replaceable. If any of its inputs, or any of its inputs inputs are flagged as replaceable and unmined, this transaction will be considered eligible for replacement. Otherwise, a transaction that has a conflict will be rejected with error "txn-mempool-conflict".

Requires that all inputs already exist in the UTXO set. No currently unmined inputs allowed in a replacement transaction. This is a tighter rule than the desired one, which is to check that the replacement doesn't require 'low fee junk' to be mined first; you can avoid this by rejecting any replacements that aren't using already mined inputs.

A replacement candidate must pay more in fees than the transactions it replaces. The rationale for this is that sending transactions takes up bandwidth -- without this restriction you could publish replacement transactions without paying for the additional cost of relaying the replacement also.

Note that this is total fees, not fee rate. Any replacement transaction must pay more in fees than the entirety of the 'package' of descendants. If you're a small sized transaction trying to replace another that’s got a much larger transaction that spends one of its outputs, your effective fee rate will be much higher than the original as you need to cover a larger amount in fees with a smaller number of bytes.  This is an incentive to push larger transactions as your replacement candidate, since they easily will pass the 'more fees' rule.

Finally if the 'package' of transactions that you're looking to replace numbers greater than 100, your replacement transaction won't be added to the mempool. In other words, if someone has attached 99 transactions onto the transaction you'd like to RBF, you're shit out of luck.

## Proposed changes
Russell O'Connor [published a proposal](https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2018-February/015717.html) to change how the RBF rules work, at least two of them. 
The proposal would update the total fees rule (3). Instead of a replacement needing to beat the absolute fee amount of the total 'package' of transactions, it'd only need to be better than the effective fee rate of the original. Additionally, the proposal would amend the 4th rule, such that the fee on your replacement is at least as much as the minrelayfee on the total package that you’re replacing.[1]

Why is minrelayfee used as a minimum? A transaction that’s replacing a larger ‘package’ of transactions removes transmitted bytes from the mempool. This rule change makes sure that the replacement transaction pays for the cost of relaying those removed bytes.

How do these rules play out? Let's see.

## Miner incentives, a consideration
There's two cases that we should consider: a larger transaction replaces a smaller transaction (small txn -> large txn) and that of a smaller transaction replacing a larger package (large package -> small txn).

### Current Rules
small  txn-> large txn: rule 3 stipulates that the total fees must be greater, with no regards to fee rate, however in practice no replacement is accepted if it lowers the total feerate of the mempool. 
https://github.com/bitcoin/bitcoin/blob/bccb4d29a8080bf1ecda1fc235415a11d903a680/src/validation.cpp#L789  Worth noting that practically this shouldn't happen anyway. The motivation for RBF'ing a transaction is that the block inclusion fee rate cutoff has spiked -- replacing one transaction with another larger one who's got a lower fee rate makes it less, not more, likely that you'd be included.

large package -> small txn: the smaller transaction must pay more fees than the existing package. The miner doubly wins: they're making the fees of a large transaction in a smaller byte footprint. 


### Proposed Rules
small txn -> large txn: Miner's choice strictly improves. The fee rate has increased and the net fee of this transaction is greater. This is no change from the current scheme.

large package -> small txn: Miner's choice also improves. Although the total fee is lower, given a competitive environment for blockspace (ostensibly why the RBF was attempted), the smaller transaction creates space for other, more valuable transactions than the existing package it's replacing. The incentives of the miner (highest fee rate per vw) and the RBF'er (having transaction confirmed) align.

## Analysis
Let's consider the large package -> small txn case, as that's the biggest change between the two proposals.

A 1ksipa txn with a 10ksipa child txn is in the mempool.  The current feerate on the blocks is 2sat / sipa. The minrelayfee is 1sat / sipa. The total fees for the package are 2ksat + 20ksats = 22ksat.

Under the current scheme, a replacement transaction of 1ksipa would need to pay at least 23ksats, or 23sats / sipa, a 11.5x increase in fee rate. (22ksat for the repla

Under the proposed scheme, a replacement transaction of 1ksipa would need to pay 12ksipa. The effective feerate is 12sats/sipa, a 6x increase in fee rate.

Effectively, this lowers the ceiling for getting out from under a large, low fee, pinning transaction.

## Commentary
RBF mechanics closely resemble that of an auction. The current rules set the floor for the second bid to be extortionately high if someone has attached a large transaction to one of your outputs. The proposed rule change will lower this floor.

Any RBF proposal leaves an opening for a DoS style of attack on a node. The difference between these two proposals is merely the floor of a bid to reset the attack.

In a high fee environment, the proposed rule change makes it more economical for motivated parties to evict non-fee competitive, bloated transactions from the mempool.


Resources:
The original BIP125, specifying RBF rules: https://github.com/bitcoin/bips/blob/master/bip-0125.mediawiki

Russell O’Connor’s proposed RBF rule changes, bitcoin ML  https://lists.linuxfoundation.org/pipermail/bitcoin-dev/2018-February/015717.html

