timestamp: 1549742688
date: 9 Feb 2019
time: 12:04
title: A Taxonomy of Lightning Nodes
tags: lightning, markets, liquidity, taxonomy

---
It never ceases to amaze me how little the general crypto population knows about how the lightning network works, so I thought I'd write down something that's been quite obvious to me for a while, with the hopes of influencing others to see it my way.

Lightning is a network of node operators. Each node has a wallet with funds, that are then apportioned amongst a set of channels to other nodes. Each channel that is opened has a balance, and each node in the channel has the right to spend a certain amount in that channel. This "right to spend" gives every channel a directionality to it. In other words, which direction the funds can move at any given moment depends on which side has the right to spend them. For this reason, the Lightning network is a directed graph. 

Every payment that moves through the system changes the balance of payments in every channel that it flows through. As payment volume grows, managing the 'flows' and ability to send payments from one node to another will become an important and non-trivial management task.

## Drawing Lines Between Nodes
A key to understanding how these flows will affect ability to make payments is to understnad that not every Lightning node has the same 'goal'.

In fact, you can classify these nodes into three distinct groups. Each of these groups represents a different policy on liquidity in their channel balances. As such, the actions they will each regularly perform on their channel balances will be distinct. A channel balance is only useful if it allows you to do what you need to on the network, and each of these three actors will have different goals.

Theses three node groups are:  
- consumers  
- vendors  
- liquidity providers  

## Consumers
This is probably the most intuitive group to understand, since it's every one of us. A consumer is a net supplier of funds to the Lightning network. On a whole, they spend more money over Lightning than they receive. There is a certain amount of exchange that happens among nodes of this type, but this amount is dominated by their outflow to Vendor nodes. Typically, their payments will be to a relatively closed set of repeated contacts. 

Generally, the actions a consumer takes will be one of:   
- Adding more money to their wallet/outgoing channel balances  
- Sending payments to vendors  
- Creating new channels to pay new vendors  

The apps that these users use are typically mobile wallets and web browser extensions. They're generally interested in centralized/custodial services. Probably not running their own node unless it is their mobile client or they've invested in a small home node.

## Vendors
This is the Amazons and Blockstream stores of the network. A vendor is a net drain of funds on the Lightning Network -- they receive more payments in than they send out. They are typically receiving inflows in exchange for a good or service, which means that they'll be withdrawing funds from their channels to cover their costs.

Generally, the actions a vendor takes will be one of:  
- Withdrawing money from their channels  
- Opening channels with liquidity providers, to get inbound capacity  
- Originating invoices  

The apps and infrastructure that these vendors use will generally be a bit more intensive and always on than consumers. Their ability to transact will be closely tied to their ability to reliably source inbound capacity. Backups and watchtowers are of a bigger concern to these users than to consumers.

## Liquidity Providers
This is the HODLers, people who have a chunk of crypto that they want to put to work but aren't interested in spending it and don't really have much of anything to sell. They've got the time, know-how, and resources to set up a more 'industrial strength' node than the general 'consumer' population. They're interested in writing custom algorithms that can help them figure out how to price their liquidity and are willing to spend the time and energy (generally speaking) to figure out what configuration of channel balances and flows will bring them the best return on their node setup, in terms of routing fees. They earn money by providing liquidity between consumers and vendors.

Generally, actions a liquidity provider will take are:  
- Opening new channels to vendors, to provide inbound capacity  
- Advertising liquidity  
- Rebalancing their channels between vendor + consumer accounts  
- Network analysis to discover lucrative avenues to open/create new channels  


### In Exitus
It's my understanding that the Lightning Network needs all of these types of nodes to function. Providing a visible market for liquidity will make these roles even more apparent. I'm incredibly excited about the inclusion of liquidity advertising in the 1.1 spec, as it will give another lever for liquidity providers and vendors to  make decisions about how to most effectively allocate channel balances across the network, in a decentralized and transparent manner.
