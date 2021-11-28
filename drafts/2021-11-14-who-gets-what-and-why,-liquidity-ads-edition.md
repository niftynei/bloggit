timestamp: 1636916216
date: 14 Nov 2021
time: 12:56
title: who gets what and why, liquidity ads edition
tags: lightning, liquidity-ads, market design

---
Alvin Toth's book on market design, "Who Gets What.. and Why", outlines a few aspects of market-making that I thought it would be interesting to apply to the liquidity market on lightning.

Toth outlines a five things that every market design should take into consideration:
- Market Thickness. Is everyone who wants to participate online at the same time? In the same venue?
- Congestion: Do participants have ample opportunity to evaluate the available matches?
- Evaluation: Of what's available, what has value *to me*?
- Game Theory/Strategy: Do I need to 'game the system' to get what I want or can I express it directly?
- Safe Participation: Am I going to be taken advantage of?

To apply these to the liqudity ads market, it's probably useful to have an understanding of how liquidity ads work.

## Liquidity Advertisements
In lightning, liquidity ads are posted by a node who wants to *offer* liquidity. The ad contains the rate that they're charging for it, how much they expect to be reimbursed for on-chain fees, and their commitment to a cap on channel fees on the liquidity they do provide.

The ads are placed on a network-wide bulletin board system, effectively. Every node gets a copy of the ad that every other node is handing out.

To take up a node on their advertised offer, any node may attempt to open a channel with them, telling the node the advertised rates they expect to lease liquidity for and the number of sats that they'd like put into a channel on their behalf.

If the node that advertised has the funds available, they'll accept the offer and the channel will open. The funds are locked into the channel for 4032 blocks, or about 1 month. The fees for leasing the channel are placed on the advertiser's side of the channel, effectively transferring the balance from the opener to the other side. This is cool though, because the fee you pay is more inbound liquidity!

(You can read more about inbound liquidity and its importance on this other post I wrote ...)

Now that you've got a bit of an overview of how liquidity ads work, let's see how liquidity ads do compared to Alvin Toth's five marketplace designs.

## Market Thickness
Toth uses the example of a farmer's market to explain thickness. Vendors are often not allowed to begin selling until the market opens. This is to prevent buyers from arriving earlier and earlier in an attempt to get the best head of lettuce or the last carton of yogurt.

Instead, the market establishes start and end times. If you want to participate, you need to be there when it's open.

Of course, the earliest arrivals will most likely get the best head of lettuce that day. But everyone who wants to participate knows exactly what the start time is.

Liquidity ads aren't an amazing design for guaranteeing that everyone who wants to buy liquidity shows up at the same time. They do, however, provide (relatively) equal access to information about available liquidity, and any lightning node that comes online and is set up to receive gossip will receive the same information -- the marketplace itself is the lightning network. Which is to say you don't have to register with a separate service or download any extra software in order to see and take advantage of the available liquidity marketplace.

On the other hand, the information is sent out by the gossip network, which means that the first nodes to find out about new liquidity are the ones that are directly connected to the node that's advertising it. The next nodes to get the new info, are the ones that are connected to them, etc. So timing of the arrival of new offers of liquidity is a bit dependent on who's making the advertisement and where they are in the network relative to you.

## Congestion
Congestion is a problem when the marketplace is too thick, or when there's too many people trying to make deals all at the same time. The issue is that, depending on how the market is designed, you may not have time to evaluate all of the available 'matches' before they've had to pair off with another. He makes a distinction between two different 'types' of good markets: commodity and matching.

In a *commodity* market, you offer a good for a price, and all buyers can see the offered prices. Liquidity ads works this way, as the contracts for how long of a liquidity lease you're buying has been standardized -- every lease is exactly 4032 blocks long. Sellers list their prices and channel fee caps in their advertisements -- any buyer has a rigid set of criteria they can apply to all of the provided offers.

In a *matching* market, you need to consider applicants for fit before making an offer. Dating for a partner or placing medical students at residency programs is a good example of a matching market. There's a time period for evaluation that's necessary before figuring out exactly which available offers is a good one to take.

Liquidity ads have a slight matching component to them as well -- as a buyer you may need to evaluate the node that's providing the liqudity ad before you can determine it's value to you. For example, you might want to figure out how much existing inbound capacity it currently has, or its connection to other nodes in the graph via channels. It might take some time to figure this out -- hopefully in the future there will be 3rd party services that can help with quickly identifying good and valuable matches.

## Evaluation of Options
This *matching* component of liqudity ads gets at exactly the third criteria, evaluating your options. Since it's a bulletin board system, it's fairly straightforward to look through all the available ads and then use whatever evaluation criteria you're using for inbound liquidity that day to decide what's usable for you.

This evaluation criteria however is ad hoc currently. Every buyer of liquidity needs to have a general idea of what they're looking for in a liquidity seller -- maybe you care about uptime? Or their channel liveness of existing channels? Or how long they've been around? It can be difficult to get this information right now, but there's a few third party services that have popped up to help fill the gap. I'm excited about more of them coming up.

Liquidity ads have a small disadvantage to an auction mechanic as well in option evaluation. A seller of liquidity doesn't have much signal for the value of their current liquidity -- there's no public orderbook that they can inspect to see prior liquidity buys from other nodes. They do have access to the current bulletin board prices, however.

This lack of an orderbook has further implications. Sellers don't have much good signal for the thickness of the market for their liquidity. In the current implementation, sellers receive offers to buy whenever the buyer makes them. They have no way of knowing if selling 1M sats to the current buyer will prevent them from having enough liquidity to sell out 5M sats to the next buyer. Design truly decentralized marketplaces is hard for this reason -- there's no centralized sharing of previous order history which can help inform decisions about pricing and demand.

Finally, it's hard for buyers to know which sellers still have funds available -- it's possible for an ad to be posted for a node that has no currently available liquidity, or whos available liquidity would satisfy a buyer's inbound needs. In the current market, you'd have to take up a seller on their offer to find out if they're able to meet your amount required.

## Game Theory/Strategy
The fourth aspect of market design is how 'safe' it is for a node to directly express its preferences and expect to have them be met. In his book, Toth uses the example of some public school matching systems where certain rules about grandfathering and siblings made it difficult to just list what schools you wanted and expect to get a preferred choice -- instead parents needed to know the intricacies of who else was picking certain schools to have an idea of how likely they'd be able to get into a school before listing it. This required parents to do informal polls -- whoever had the best information usually was the most successful at getting their children into the right school.

Liquidity ads are pretty straight forward.  A buyer of an ad merely needs to query a seller as to whether or not they have funds available. Given that some sellers may have limited funds, there's probably an advantage (depending on how high of demand that liquidity is then) to being directly connected to a node that's sending out a liquidity ad for the first time. However, it's impossible to predict which nodes will be emitting them first and most lightning nodes will only exchange gossip with a limited number of peers.

Still, this is definitely a downside to using the gossip network for relaying information about new offers. 

One way this could be improved is for a centralized service to accept and publish liquidity ad information -- this would give nodes at far reaches or who aren't up to date on their gossip downloads an opportunity to see new advertisements as they were published.

## Safe Participation
Finally, are liquidity ads a safe place to buy and sell funds? If you offer up liqudity, are you going to be taken advantage of by the opening node? If you buy liquidity from a node, how do you know that they will leave the channel open so that you have an opportunity to use the inbound liquidity?

At the protocol level, we've tried to make leasing liquidity as safe as possible by aligning a liquidity seller's incentives with the buyers. We do this by locking the output of the funds to the seller for the duration of the contract -- if the channel closes before the lease has expired they won't be able to re-use those funds until the lease has ended. This gives them an incentive to keep the channel open since as long as it's open they'll be able to earn more routing fees through the channel.

When opening a channel to *any* new node, whether as a buyer of liquidity or just a normal lightning node, it's always advisable to do some due diligence on your channel partner before committing funds to the channel. While the funds are locked into bitcoin contracts that you have the ability to withdraw at any time, there are certain classes of attacks where your channel peer can manipulate fees etc cetera to send your funds to miners. Liquidity ads expands the opportunities for deploying capital, and for nodes to request capital deployment from you (for the right price). 

If you're selling or buying liquidity, it's probably a good idea to use smaller amounts for first time leases with new nodes, and to scale up your capital commitment over time as you learn more about your peer. There's some third party services that allow you to see node uptime and ratings. Liquidity ads provide you with the information you need, however, to know exactly with who you're transacting before committing to the new channel.

## In Exitus
Liquidity ads create a *decentralized* liquidity marketplace for lightning. They provide a cheap and anonymous way to find and source inbound liquidity for your node, and provide an accessible venue for any seller to list their liquidity for sale.

There's definitely room for some improvement, however. It'd be great if there was a method for sellers to post executed sales to a centralized dashboard or data provider who could then provide better pricing and demand data to all market participants. There's also room for better analytics around nodes offering liquidity and maybe a nicer way for them to prove their total available liquidity via the advertisement or as part of the node connection handshake, so that prospective buyers have a more granular way to sort available ads by amount.
