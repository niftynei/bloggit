timestamp: 1530470171
date: 1 Jul 2018
time: 11:36
title: On the Nature of Bitcoin
tags: bitcoin, economy, crypto, debt, david-graeber

---

I just finished reading David Graeber's book _Debt: the first 5,000 years_. It was a great, masterful book, that gets some things wrong, but largely, seems to get things very right. What I really liked about _Debt_ is how it devles deep into the anthropological and archeological record to draw new, compelling conclusions about the actual history of monetary systems.[1]

My motivation for reading this book was to try to get a historical view on digital currencies, specifically Bitcoin. So let's do that. Let's take _Debt_'s conclusions about money systems and apply them to the recent birth of digital money.[2]

## The Local Value of Currency

One thing that really stood out to me in Graeber's explanation of how even gold and bronze based currencies got their start was how the power of the government that issued the coin largely dictated the extent of that coin's value, independent of the value of the metal that it was made of.  Metal, notably, has a value independent of the value of the coin that it constructs. The fact that the reach of a government's power was, and still largely is, the extent of the value of its currency says a lot about the actual nature of a currency. A currency is a locally understood store of value. It's accepted in certain territories and markets because it has a value in that realm. The value that it carries is largely related to the government. For example, Graeber makes the point that early currencies were often given their value via the government requiring their own money as the only thing that would satisfy taxes. As a farmer, or herdsman, or general land owner, paying your taxes required the physical posession of that government's coinage. Hence, the government has the power to drive the value of its currency by requiring it from its populace as tribute at tax time. More people who owe a greater debt to the government, payable only in the government's own currency, makes the value of the currency go up. The government has the ultimate manipulatory power, in that they can raise or lower taxes, inherently changing the value of the currency that's used to pay the taxes.

Drawing from the insights of Scott in _Seeing Like a State_, quantifying an economy in terms of the system of currency that is owned and controlled by the government is a great way of accounting and making visible opportunities for taxation. By measuring all goods and services by a common, government controlled yardstick, the tax maker has a method for determining the tribute owed by all members of the economic society under its purview.

Ok, so, if currencies are only able to derive their value from their use of payment for governmental tribute, where does the value of a cryptocurrency like Bitcoin come from? You can't use Bitcoin to pay your taxes. As far as I know, as of this writing, there is no government that will accept Bitcoin as payment for taxes.

Under the lens of currency as a token for state obligations, Bitcoin is not a currency. Thus as far as any national government is concerned, Bitcoin has no value.[3]

## The 'Value' of Bitcoin

But is Bitcoin valueless? Even the coins of old empires had a monetary value based on their physical substrate. Let's consider the 'substrate' that makes up Bitcoin.

In the classical sense of governmental fiat, Bitcoin is valueless. But, given the market and exchanges that have developed around Bitcoin, it clearly has a value. Why? What about Bitcoin is valuable, in and of itself, independent of its ability to be exchanged for other goods?

It's tempting to delve into aspects of contracts or old style tokens that were promises to pay. Bitcoin shares a lot of common features with these, but inherently isn't rooted in a debt or a promise to pay. That's because Bitcoin, at its core, isn't a ledger of who will pay who, but rather a permanent record of who owns what.

Bitcoin's value comes from the system that it's built upon. Bitcoin is a globally available, persistent, decentralized accounting ledger with a genuinely verifiable timestamping machine. This timestamping mechanism is an important feature and value proposition of Bitcoin as a value store -- it's what gives you the ability to order payments in time. I'd argue that it's the most important, valuable aspect of the computer system that makes Bitcoin possible.

Satoshi didn't invent the time keeping machine that backs Bitcoin[6]. Rather, it was first proposed in Haber and Stornetta's 1991 paper in the _Journal of Cryptography_ "How to timestamp a digital document". In the paper, Haber+Stornetta propose two different mechansims for creating a global and perpetual timestamp verification machine. Satoshi used the first mechanism, of including the hash of a previous document in the following document, creating a chain of time verifiable documents. Bitcoin blocks are time verifiable documents. This is, to a large extent what makes them incredibly valuable. Due to their timestamped nature, and the lack of central control over this machine, they are unspoofable.

## A Short Digression on The Historicity of One-Way Functions

I stated earlier that Bitcoin isn't a debt system, but in a lot of ways the way that value is passed from one holder to the next closely resembles early currency systems of the Ancient Middle East and the Eurporean Middle Ages. In these systems, debts were often marked in notches on a rod or tablet and then broken.  The debtor would carry one half, the owner of the debt the other. I struggled for a while to understand how a broken rod or tablet was good as a contract, but it's quite simple and ingenious. Curiously, it functions very similarly to a cryptographic one way function. A clay tablet is easy to break into two parts. It is also easy to tell if two parts of a broken tablet belong to each other, merely by seeing if the broken edges fit back together. However, it is very difficult to break a second clay tablet in such a way as to absolutely mirror the first. This is why clay tablets were broken -- to create signatures that only the other half could fulfill.

Cryptographic one-way functions work in an incredibly similar manner, except that, instead of relying on the random ordering of physical tablet particles in a break, they rely on the finding and computation of large numbers.  Cryptographers and mathmeticians have largely succeeded in copying the ease of tablet breaking and matching with the use of public and private keys. The only downside to the numeric device is that you have to keep your private key a secret, whereas a tablet's contents can be public. It's a common trope of modern technology to convert a physical device into data -- in this case transforming the security from physical space to informational. Put another way, the clay tablet version of document verification was based on what you have, a matching clay tablet, the new Bitcoin mediated version of verification is based on what you know, a large number. [4][5]

## The Supply of Bitcoin is Irrelevant

The supply of Bitcoin is irrelevant in terms of its value, because the value of the system isn't from the amount of currency that is available, but rather from its value as a globally consistent, timestamping machine. Although the supply of Bitcoin will be limited, eventually, when newly mined blocks are no longer provide a subsidy to the miner, people will still be willing to pay the required fees for values to be transferred. The real trick to understanding this is to compare Bitcoin to wooden rods or clay, not gold and silver. Gold and silver, in some sense, are understood to derive their value from their scarcity[7] or how much work it takes to get them.  Admittedly, there is some work done in order to 'mine' more Bitcoin, and running the computer network that makes up the Bitcoin system has a non-negligible cost, but at the base level of computers bits and memory incurs a cost on the order of clay or wood, not gold or silver.

Traditional gold and silver coinage systems are bad comparisons for other reasons. Gold and silver are the tools of the state. What we think of the metal money coinage system is inherently inseparable from government influence and meddling in exchange. Gold and silver are the materials of royalty and the central state -- coins are largely impersonal and unsigned by the relationship between the debtor and creditor. In socieites where coins are used as tribute, or taxes, to the state, and are a method of value extraction by a central, authorized authority. The value of the coin rests largely on the ability of the government to stay in power. It's tied to the state and its power. 

Clay tablets and wooden rods, on the other hand, need no higher authority. They're a record of a debt owed between two private parties. They're made out of materials that everyone has access to, there's nothing special about the object in and of itself. It's value comes from who hodls it, and the fact that there are only two people who can set that debt to right.

Bitcoin is low cost and relationship based in the same way that tablets and rods are. It requires a computer and some world-class engineered yet freely available software, things that the vast majority of people have access to. Buying a mining rig might be expensive, but setting up your laptop to mine Bitcoin is fairly trivial. Once you're over the inital time cost of setting up a Bitcoin wallet, making transaction costs almost nothing. You're free to transact with whomever you want and can make a lasting, timestamped record of your relatiionship in bits.

Bitcoin isn't a store of value, it's a store of past, paid debts.

## Bitcoin and The State

I wondered a lot about why China would be so anti-Bitcoin. Graeber's linkage of fiat (ie money coins) to state control and taxes explained a lot of the state's resistance to it. It's largely true that Bitcoin is decentralized and unregulated. In some ways, having a monetary exchange value only made Bitcoin more easily traceable by the state.

Graeber shows that the state has a tendency to 'take over' or replicate independent stores of value, in official, sanctioned ways. This is how paper money became a thing -- private citizens that would issue papers as promissory notes. Eventually the state began to copy this method for accounting value. (todo look up notes on this).  The same thing is happening in cryptocurrency. Bitmain and Circle are supposedly in the process of putting together a [cryptocurrency that would mirror the USD](https://www.investopedia.com/news/circle-bitmain-launch-us-dollar-cryptocoin/). Admittedly, it's not the US government making the coin, but so much of private market is an extension of the state (prisons, healthcare, debt collection) it wouldn't be unique in that. China's President Xi has even gone on record stating that he's in favor of cryptocurrency, in general, just not Bitcoin in particular.


## So is Bitcoin a Currency?

The question remains: is Bitcoin a currency? Viewed through the lens of classical age debt tallies, the answer is an unequivocal yes. 

From the lens of actual spec, that is gold and silver based currency issued by a central government authority, the answer is an unequivocal no.  Bitcoin has no utility for raising and paying an army, its value extends as far as people are willing and ready to incur debts between each other. In the larger view, Bitcoin is valid as long as the underlying computer network that accepts and timestamps transaction blocks still exists. From a smaller, more individual view, Bitcoin is actually only useful as long as you retain your 'half' of the broken rod, or access to your private key. There's plenty of stories about Bitcoin holders that lost their private key and, well, let's just say you can't really count them as Bitcoin holders anymore. Bitcoin is not actually a 'coin' at all, it's a digital store of broken tablets, with a host of random people holding the other end of the stick.


[1] Graeber also massively drags Adam Smith's inivisible hand and I am HERE for it.

[2] While also spending some time just going through the key takeaways about money that Graeber's book points to.

[3] As of this writing, lol.

[4] In this way, the storage of Bitcoin private keys is an interesting, hybrid challenge, mostly because humans aren't very good at remembering things -- you have to secure the place that you store the big secret number that is your private key.

[5] If you've ever had a friendship bracelet you're probably familiar with the concept of how broken halves that make a whole can be used as a verification. Thinking back, it's rather tragic that all the ones that I owned as a child were mass produced, and hence lacked the uniqueness property that made the original tokens so valuable.

[6] Telling, 3 of the 8 listed references in Satoshi's whitepaper are for papers on timestamping machines.

[7] This isn't true, for several reasons, but for now let's just let the assumption stand.

References:   
Satoshi's Whitepaper [https://bitcoin.org/bitcoin.pdf](https://bitcoin.org/bitcoin.pdf)   
How to Timestamp a Digital Document [https://www.anf.es/pdf/Haber_Stornetta.pdf](https://www.anf.es/pdf/Haber_Stornetta.pdf)  
