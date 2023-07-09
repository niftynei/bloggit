timestamp: 1661380194
date: 24 Aug 2022
time: 18:29
title: niftynei's Unscientific Liquidity Sales Guide
tags: lightning, liquidity, channel-sales

---
This is a quick guide for things to consider when you're looking to sell inbound channel capacity on the Lightning Network.

## Skip Tor
Tor is unreliable for long-running connections, like the type that lightning channels depend on. This unreliability can lead to force closes. I personally dont buy any liquidity from nodes that I can't connect to over clearnet (IPv4 or IPv6).

## Be Mindful of Your Closing Costs
A little known fact about lightning channels is that the peer that *opens* the channel is responsible for the onchain fees for the closing transaction, no matter which party closes it.

This means that if you sell someone liquidity and then are the one who *opens* the channel to the buyer, you're on the hook for the cost of closing that channel. This is hard to account for ahead of time as the feerate in the future is unpredictable.

Anything you pay to close the channel will cut into your "profit" from the sale of liquidity. Magma and I believe Pool(citation needed) have the seller of the liquidity initiate the channel open; the liquidity ad protocol is the only one that I know of where the channel *buyer* initiates the open (and thus bears the channel closing costs). Might be worth keeping in mind if you're looking to profit from selling deployment of capital to the network.

## Routing Fees vs Liquidity Sales
There's two opportunities for earning "return" from capital deployed to the lightning network: being paid to allocate capital to a channel and being paid to route a payment.

The best of both worlds would be getting paid to put money into a channel and then also collecting fees to route that capital (preferrably a few times, back and forth).

Some channel operators charge zero for routing but will sell you inbound liquidity. These operators are basically getting pre-paid for the routing of that money to you. This is probably a better deal than not getting paid for that capital at all. Note that this strategy means that you'd probably prefer to have your capital available to be re-purchased rather than in a channel for a long duration, given that you're not going to get paid for capital in channels with "expired" leases. In fact, it's probably a good deal for you if you're not responsible for opening this channel, and thus don't have to pay any closing costs for it.

Buyer beware here, eh.

## On-Chain vs In-Channel Liquidity
Zmn raised a point recently that when considering how to implement liquidity ads into CLBoss (Core-Lightning's auto-channel manager "AI" bot plugin) that there's an *opportunity cost* associated with leaving funds on-chain with the hope that someone might buy them.

The logic goes a little something like this: money in a channel might be routed. This will earn you routing fees.

Money on-chain (not in  a channel) might be purchased as in-bound for a new channel. But it can't be routed through while it's waiting to be purchased.

How do you balance the opportunity to sell liquidity into a channel with the opportunity to be paid to route a payment? This is a tricky question which probably is different for every node, depending on your connectivity and the routes you've got liquidity on.

Note here that [splicing](https://github.com/lightning/bolts/pull/863) should make a big difference in terms of figuring out how to balance this -- it should allow you to dynamically move capital out of a channel into a new one whenever someone asks to buy liquidity from you. Of course, the algorithm which decides which capital is worth re-deploying is still an open problem, but at least you don't have to decide how much liquidity to keep *out* of channels now, rather you just have to decide *which* channels to resize (if any).  This will hopefully be out on CLN soon, so get your best capital opportunity estimation equations ready.
