timestamp: 1530470171
date: 1 Jul 2018
time: 11:36
title: On the Nature of Bitcoin
tags: bitcoin, monetary-systems, cryptocurrency, debt, david-graeber

---

I just finished reading David Graeber's book _Debt: the first 5,000 years_. In it, Graeber shows that how we think about money and exchange is fundamentally flawed. To do so, he digs into his experience as an anthropologist, the historical and archeological record of actual human societies, to give a more honest accounting, not of how money systems should work, but did and do.

My motivation for reading this book was fairly pointed -- I wanted a historical perspective in which to place digital currencies generally, Bitcoin specifically. I wasn't disappointed.  What I found really surprised me, and honestly, completely re-wrote the way I think about digital currency, friendship charms, and my communal economic relationships more broadly.

## The Local Value of Currency

A large focal point of Graeber's debunking in _Debt_ concerns where hard, physical currency comes from. How did humans actually come to regard coins as a store of value? Classical economists use Adam Smith as their jumping off point for how currency arose: because it's hard to imagine a trade economy without currency. But Graeber says that the common 'market' of trading that we all imagine didn't really exist, back in the beginnings of human trade. Instead, he proposes that humans merely kept local, personalized accounts of who owed who what. You always were a bit in debt to someone, and someone was always a bit in debted to you. That's how societies worked -- everyone owed everyone else. 

At some point in ancienct Mesopotamia, these debts came to be recorded on clay tablets. One person would owe another four bushels of grain, for example. So you'd write onto a clay tablet, twice maybe, that so and so owed 5 barrels of wheat. The tablet would then be broken in half, and each party to the transaction would get half. When the time came for payment to be made (Graeber wasn't entirely specific about how these tablets got redeemed), the tablet would be destroyed.  According to Graeber, at some point people started trading these promises to pay with other parties. If Bob owed me four bushels of grain, I could exchange it with you for a new toga. Then, when the debt came due, Bob would pay you, the holder of the other tablet half, four bushels in exchange for the contract that you're holding.

The first version of 'currency', as in not an actual, obviously useful good, Graeber proposes, were these temporary, two-party contracts.

If these person to person promissory notes were the first version of currency, when did the gold and silver coinage come into play? Graeber asserts that coinage is almost always and explicitly the work of a governing body. A government can pass out gold and silver to its citizens as coinage, and then, as a way to give the coins some kind of value, would make it such that official gold or silver coins were the only way to pay taxes. Or, phrased another way, the government gave coinage its value by demanding that all citizens acquire enough of it annually to pay tribute to the government. It's pretty perverted when you think about it: governments dug deep into their treasuries, melted down their treasures or spent years of human capital building mines, such that they could divide it up into small pieces, stamp their image into it, distribute it among the people, only then to turn around and ask their citizens to hand it back at the end of the year,  at least some of it anyway. It feels a bit out of scope to go into why governments would do this; let's just accept Graeber's explanation that they did it such that the government was able to afford goods and services from people, and then, eventually needed to extend that same ability onto it's army. So it gave one of the only things that a government can get control of -- treasure -- as payment to soldiers who then were able to buy what they needed using the coins the government gave them.

All of this may sound exceedingly hard to swallow without further proof, and I'm really not doing Graeber's arguments justice. But, have you ever heard of anyone successfully being able to pay taxes with anything other than the coin of the realm? It's not physically possible. In fact, it's one of the biggest reasons that early employees at non-publicly traded startups get stuck with options they can't exercise. You literally can't trade the shares for money, so you have nothing to give the government as its part of the tribute to the spoils you've won.

One thing that really stood out to me in Graeber's explanation of how even gold and bronze based currencies got their start was how the power of the government that issued the coin largely dictated the extent of that coin's value, independent of materials.  You can see this phenomena today. Copper has a price in the open market that is often completely different than the 'monetary' value of copper printed into a penny.[1] The fact that the reach of a government's power was, and still largely is, the extent of the value of its currency says a lot about the actual nature of a coined instrument. 

A currency is a locally understood store of value. It's accepted in certain territories and markets because it has a value to the people of that realm. Usually that realm is defined by the government party who's laws the state elects, or is forced, to follow. 

Hence, the government has the power to drive the value of its currency by requiring it from its populace as tribute at tax time. More people who owe a greater debt to the government, payable only in the government's own currency, makes the value of the currency go up. So the government has the ultimate manipulatory power, in that they can raise or lower taxes, inherently changing the value of the currency that's used to pay the taxes. Taxes and the value of a government's money are intimately linked.


## What's a Bitcoin Worth?

If currencies are only able to derive their value from their use of payment for governmental tribute, where does the value of a cryptocurrency like Bitcoin come from? You can't use Bitcoin to pay your taxes.[2]

Under the lens of currency as a token for state obligations, Bitcoin is not a currency. Thus as far as any national government is concerned, Bitcoin has no value.[3]

But is Bitcoin valueless? Even the coins of old empires had a monetary value based on their physical substrate -- gold and silver have plenty of applications in manufacturing and jewelry making, if nothing else. 

Let's consider the 'substrate' that makes up Bitcoin.

In the classical sense of governmental fiat, Bitcoin is not a currency. It has no value in terms of being accepted by the government to pay a debt. But, given the market and exchanges that have developed around Bitcoin, it clearly has a value. Why? What about Bitcoin is valuable, in and of itself, independent of its ability to be exchanged for other goods? Doesn't that make it like a currency?

It's tempting to delve into aspects of contracts or old style tokens that were promises to pay. Bitcoin shares a lot of common features with these, but inherently isn't rooted in a debt or a promise to pay. That's because Bitcoin, at its core, isn't a ledger of who will pay who, but rather a permanent record of who owns what. So being a debt that one person owes another doesn't really apply here.

Rather, Bitcoin's value comes from the system that it's built upon. Bitcoin is a globally available, persistent, decentralized accounting ledger with a genuinely verifiable timestamping machine. This timestamping mechanism is an important feature and value proposition of Bitcoin as a value store -- it's what gives you the ability to order payments in time. I'd argue that it's the most important, valuable aspect of the computer system that makes Bitcoin possible.

Satoshi didn't invent the time keeping machine that backs Bitcoin[4]. In fact, it was first proposed in Haber and Stornetta's 1991 paper in the _Journal of Cryptography_ "How to timestamp a digital document". In the paper, Haber+Stornetta propose two different mechansims for creating a global and perpetual timestamp verification machine. Satoshi used the first mechanism, of including the hash of a previous document in the following document, creating a chain of time verifiable documents. Bitcoin blocks are time verifiable documents. This is, to a large extent what makes them incredibly valuable. Due to their timestamped nature, and the lack of central control over this machine, they are unspoofable. The value of Bitcoin then, is in its digital timestamping value.

## A Short Digression on The Historicity of One-Way Functions

I stated earlier that Bitcoin isn't a debt system, but in a lot of ways the way that value is passed from one holder to the next closely resembles early currency systems of the Ancient Middle East and the Eurporean Middle Ages. In these systems, debts were often marked in notches on a rod or tablet and then broken.  The debtor would carry one half, the owner of the debt the other. 

I struggled for a while to understand how a broken rod or tablet was good as a contract, but it's quite simple and ingenious. Curiously, it functions very similarly to a cryptographic one way function. A clay tablet is easy to break into two parts. It is also easy to tell if two parts of a broken tablet belong to each other, merely by seeing if the broken edges fit back together. However, it is very difficult to break a second clay tablet in such a way as to absolutely mirror the first. This is why clay tablets were broken -- to create signatures that only the other half could fulfill.

Cryptographic one-way functions work in an incredibly similar manner, except that, instead of relying on the random ordering of physical tablet particles in a break, they rely on the finding and computation of large numbers.  Cryptographers and mathmeticians have largely succeeded in copying the ease of tablet breaking and matching with the use of public and private keys. 

The only downside to the numeric device is that you have to keep your private key a secret, whereas a tablet's contents can be public. It's a common trope of modern technology to convert a physical device into data -- in this case transforming the security from physical space to informational. Put another way, the clay tablet version of document verification was based on what you have, a matching clay tablet, the new Bitcoin mediated version of verification is based on what you know, a large number. [5]

## Supply is Irrelevant

The supply of Bitcoin is irrelevant in terms of its value, because the value of the system isn't like gold or silver. Gold and silver's value is based, to some extent, on how scarce it is. While it's true that Bitcoin isn't infinite in supply, it gets it's true value from existing as part of a global, always-available verifiable timestamping machine. 

The supply of Bitcoin is limited, but when newly mined blocks are no longer subsidized, I believe that people will still be willing to pay the required fees for values to be transferred, because being able to transfer obligations is a valuable enough service to continue operating the system. The external value of the currency may go up, but Bitcoin as a system won't crash because the digital ledger will still be a valuable service in and of itself.

The real trick to understanding this is to compare Bitcoin to the actual type of currency that it most closely resembles: wooden rods or clay, not gold and silver. Gold and silver, in some sense, are understood to derive their value from their scarcity or how much work it takes to get them, and admittedly, there is some work done in order to 'mine' more Bitcoin, and running the computer network that makes up the Bitcoin system has a non-negligible cost, but at the base level of computers bits and memory incurs a cost on the order of clay or wood, not gold or silver. Further, gold and silver have a more primary value derived not from their scarcity, per se, but instead from the governmental tax requirement levied on every citizen. 

So how scarce is Bitcoin? Internally, it's limited to 21 million Bitcoin, total. It may seem like a small number, but it works out to 262,500 satoshi apiece for 8 billion humans. One could argue that that's enough, at a raw level, for every human to transact with each other. If we, as a society, got organized, we could distribute every human a non-trivial allotment of Bitcoin from birth, no questions asked. 

On a technological level, the bits and computer infrastructure that makes up Bitcoin is cheap and widely available. You can see this assumption of a certain ubiquity of bits in Bitcoin's distributed model. As a system, it is designed to run on most medium-range consumer grade computers.  

Traditional gold and silver coinage systems make for a bad comparisons with digital currencies. What we think of as the metal money coinage system is inherently inseparable from government influence and meddling in exchange. The value of the coin rests largely on the ability of the government to stay in power. It's tied to the state and its power. 

Clay tablets and wooden rods, on the other hand, need no higher authority. They're a record of a debt owed between two private parties. They're made out of materials that everyone has access to, there's nothing special about the object in and of itself. Its value comes from who hodls it, and the fact that there are only two people who can set that debt to right. No state power is needed to enforce the value of the contract.

Bitcoin, then, isn't a store of value, it's a store of past, paid debts.

## Bitcoin and The State

I wondered a lot about why China would be so anti-Bitcoin. Graeber's linkage of fiat (ie money coins) to state control and taxes explained a lot of the state's resistance to it. Under Graeber's explanation of the ties between the state and coins, this antipathy makes more sense. 

Graeber shows that the state has a tendency to 'take over' or replicate independent stores of value, in official, sanctioned ways. This is how paper money became a thing -- the original paper spec started from private citizens issuing paper promissory notes. Eventually the state began to copy this method for accounting value. 

The same thing is happening in cryptocurrency. Bitmain and Circle are supposedly in the process of putting together a [cryptocurrency that would mirror the USD](https://www.investopedia.com/news/circle-bitmain-launch-us-dollar-cryptocoin/). Admittedly, it's not the US government making the coin, but so much of private market is an extension of the state (prisons, healthcare, debt collection, money printing) it wouldn't be unique for a private party to take on this role. (China's President Xi has even gone on record stating that he's in favor of cryptocurrency, in general, just not Bitcoin in particular. I have no doubt that the government is currently working on a cryptocurrency that it controls.)

## So is Bitcoin a Currency?

So is Bitcoin a currency? Viewed through the lens of debt tallies, the answer is an unequivocal yes. 

From the lens of actual spec, that is gold and silver based currency issued by a central government authority, the answer is an unequivocal no. 

Bitcoin has no utility for raising and paying an army, its value extends as far as people are willing and ready to incur debts between each other. In the larger view, Bitcoin is valid as long as the underlying computer network that accepts and timestamps transaction blocks still exists. 

Like a clay tablet, Bitcoin is only usable as long as you retain your 'half' of the broken rod, or access to your private key. Bitcoin is not actually a 'coin' at all, it's a digital store of broken tablets, with a bunch of private wallets holding the matching half. 


[1] Does anyone actually know how diluted copper pennies are these days? When's the last time someone did a physical inspection of the amount of copper in a penny?

[2] Most places. Seminole, Florida and Arizona are two exceptions though I will mention that they trade the Bitcoin into USD immediately so I'm not really sure that this counts.

[3] Tellingly, 3 of the 8 listed references in Satoshi's whitepaper are for papers on timestamping machines.

[4] As of this writing, but see note 2 about how a few governments will accept Bitcoin and immediately convert it into the state fiat.

[5] In this way, the storage of Bitcoin private keys is an interesting, hybrid challenge, mostly because humans aren't very good at remembering things -- you have to secure the place that you store the big secret number that is your private key.

References:   
Satoshi's Whitepaper [https://bitcoin.org/bitcoin.pdf](https://bitcoin.org/bitcoin.pdf)   
How to Timestamp a Digital Document [https://www.anf.es/pdf/Haber_Stornetta.pdf](https://www.anf.es/pdf/Haber_Stornetta.pdf)  
