timestamp: 1573414713
date: 10 Nov 2019
time: 13:38
title: Ch-Ch-Ch-Chia!
tags: blockchains, bitcoin, chia, explainers

---

tl;dr: A "Proof of Space" algorithm doesn't actually have anything to do with storing user files



I've been curious lately about other 'crypto-system' projects. A friend of mine sent me this nice writeup they did of IPFS; I thought it'd be fun to do something similar for what I *thought* was another 'file coin' protocol - Chia's [Green Paper](https://www.chia.net/assets/ChiaGreenPaper.pdf). Turns out that I was wrong about it being a 'file coin', but it was interesting so here's a quick review of what the paper contained, plus some open questions that the paper doesn't address.



## What is Chia?

Chia is another cryptocurrency play. It's aiming to be a 'better' and 'greener' competitor to Bitcoin. As such, it's got a lot of the features that Bitcoin has[0]. It's got blocks, it's got 'miners' (more on this in a bit). It's rumored to have a scripting language not unlike Bitcoin's Script. It's not launched yet, testnet is expected to go live before the end of the year.

[0] I've culled this discussion from both the Green Paper and the public Keybase group.

### Mining Chia

The biggest single difference between Chia and Bitcoin is how they secure the network. Bitcoin uses a hash-function to act as a random lottery for all mining participants. Each lottery round is about 10 minutes long and involves you, and every other lottery participant, hunting for the winning combination of bits that will produce a hash of a small enough size. Your chance of winning this lottery is directly proportional (statistically, at least) to how many times you can call the 'hash' function in that ten minutes, relative to the number of times every other lottery participant can also do this. "How many times you call the 'hash' function" is also commonly referred to as 'hashpower'. If you control a lot of hashpower, relative to other miners/lottery players, that means that you're able to run that hash function a lot more times than your other lottery competitors. Over time, if you have 10% of the total hashpower, you can expect to 'win' 10% of the blocks.

You've got to be running computers the whole time to play in this lottery, and those computers consume electricity to run. So Bitcoin uses up electricity to mine; the larger the number of people playing in the miner lottery and the more powerful their machines, the more power that is used on every lottery round, or block mining.



Chia is trying to be 'greener', which means that reducing the amount of electricity you need to participate in the lottery of 'choosing' the next block that is mined. There's a couple of ways that different crypto projects choose to do this. Common ones are variations on Proof of Work or Proof of Stake.

Chia's approach is a combination of two different 'proof' systems, a lottery that requires disk space to participate and a 'timing delay' proof system, that is required to rate-limit the speed with which new blocks can be officially 'verified', as well as a filtering mechanism for picking a 'winner' from the disk-space lottery.

The paper itself names each of these participants in the block creation: there are Farmers, the ones with blocks and blocks of disk space that are being used to 'farm' a lottery share; and there are Time Lords, who use a fixed-step squaring function to rate-limit how fast a farmed block signature can be added to the chain.

The farmers are participating in a 'Proof of Space' algorithm; the Time Lords run a Proof of Time function (also known as a Verifiable Delay Function, or VDF).

####  Farming it Out

Proof of Space works by filling terabytes of space with junk data and calling it a 'farm plot'. Ok, that's a *little* rude; the data isn't junk necessarily. But don't think you're going to be able to use that space for anything else.

A farm plot is a set size, let's say 10G of disk data. So 100G of disk space you can fit 10 'farm plots'. I'm probably going to get the details a little bit wrong here, but the general idea is that each farm plot has it's own public/private key pair. Every time a new block is available to be mined, that farm plot signs the block with its private key; the signature scheme is _unique_[1], which means that one private key and block can only ever produce one signature.

In a previous post, I talked about how the ECDSA signatures that Bitcoin uses are malleable. This is because Bitcoin ECDSA sigs involve a randomly chose value, `r`. You can generate lots of valid signatures for the same message just by using a different `r` value (but you really shouldn't publish them, as I believe that this can eventually leak information about your private key).

BLS signatures, on the other hand, are not malleable. Which means for any given message and a single private key, you can generate at most one valid signature. In Chia, this means that one farm plot only ever equals one signature (per message, which is a block in this case).

Ok, so one plot means one signature. These signatures have a 'quality' (measured as the number of leading zeros of their serialized form). A good 'quality' signature has a high probability of being used to finish mining the block by the time lords (we'll come back to this shortly). 

This boils down to each plot being a single lottery ticket for every block reward. In our example above, where 10G of space is one plot, and we've got 100Gs that we're 'farming' with, this means that you've got 10 lottery tickets that you can submit for every block that gets mined. If there's 10 other farmers on the network, each with the same 100G of 10 plots, that means that you'd expect to have the best (or smallest) signature about 10% of the time.

In Bitcoin a lottery ticket is a 'hash' that you've computed. You generate additional lottery tickets by computing new hashes. In Chia, a lottery ticket is a farm plot (of disk space). To get more lottery tickets, you need to commit more disk space to farming.

Pretty cool huh? This turns disk space into lottery tickets, instead of CPU time and electricity.

[1] Chia uses BLS signatures to do this; they've got an implementation of it in C++ up on Github. Spec for the BLS signatures [here](https://github.com/Chia-Network/bls-signatures).  

#### Seeding Plots

But, what's in these plots? How does having disks filled with 'junk' give you anything resembling a lottery ticket? Why does the signature depend on this disk space?

The answer has to do with the 'algorithm' that's being used to sign blocks with. Signing a block requires taking squares of large numbers. This is computationally intensive and takes time to do if you compute it from scratch each time. Instead, you can generate lookup tables ahead of time that significantly cut down the amount of computation required to create signatures. A lookup table basically consists of pre-computing the squares of a bunch of combinations of numbers, and then storing them on disk until you need them.

These lookup tables take up a lot of space though. So you've got to store them on disk. This disk space that you fill up with lookup tables is your farm plot. It's required for being able to sign, since without them you'd need to run the computationally intensive calculation every time. This is why the algorithm is a 'Proof of Space' -- you wouldn't be able to competitively submit block signatures (in an attempt to get the 'best signature') if you didn't have gigabytes of data filled up with lookup tables.

Actually, generating these plots is computationally intensive, as you'd imagine, so the startup cost to creating a plot is non-zero. This is good for farming stability, in my opinion, as it makes joining the farming lottery costly. Ideally you'd use a high powered CPU machine to build your lookup tables, and then transfer them to cheap storage being run by a slow or low-powered CPU machine. I/O is more likely to be a bottleneck for farmers than CPU.



#### Searching For A Good Sig

Why don't farmers just try to sign a bunch of different blocks to get the best signature? Great question. Chia actually allows for this. They call the constant `k`, it's the number of different blocks at a single chain height that are considered valid. Bitcoin has a `k` value of 1, which is to say that there's a single chain tip that (honest) miners all attempt to extend. In Chia, they allow farmers to attempt to extend 3 simultaneous chaintips. Which means that for every chain link, your farm plot would sign up to three blocks, or have three chances at winning the block lottery.

There's no real discussion of where blocks come from (who's building them) or what the data that the blocks contain, so there's conveniently no discussion of how the spendable UTXO set is calculated amongst these three-heads of simultaneous block creations. Ostensibly, if a transaction is in one block it wouldn't be valid to be included in another one? Or maybe it has to be mined in 3 blocks before it's considered valid? The paper didn't talk at all about the data structures that are stored in the Chia chain, so it's hard to know what the plan is here, exactly. 

Actually, that's another interesting point about how Chia blocks work. The data portion of the blockchain isn't included in the 'stem' of the chain. Instead, the data is added to 'foliage' blocks which are bound to the mainline mined blocks by signatures. This is done to make the signatures non-malleable (because the inputs don't change). There weren't good details exactly how these foliage blocks are composed in the paper, either.

[2] The Chia paper has a good discussion around the implications of different `k` values.

#### Implications of Plotting

There's two ways that people can 'cheat' the Proof of Space requirements. One is that you figure out a short cut for running the signature generation step that makes it feasible to calculate the squared products on the fly instead of relying on lookup tables. This effectively turns Proof of Space into a Proof of Work. Since table look ups are constant time though, you'd really need something magical to beat lookup tables on speed.

Two, some form of compression that allows you to store lookup tables in a fast to access/decompress manner. I'd imagine that the Chia team has investigated this, or has even built a compression algorithm into the plot storage data structures. Even if not, table lookups are *fast* and hard to beat, so again kind of a stretch to imagine that compression will keep you competitive.



### The Lordiest Time of All

Using 'high quality' farmer signatures is just the first half of the block 'confirmation' process in Chia. We need something to rate-limit how fast blocks get mined. Rate limits are good because they allow time for blocks to propagate to signers, which gives everyone (in theory) an opportunity to sign the block (and therefore participate in the lottery for it). 

Just having farmers sign blocks isn't very rate-limity though. To overcome this problem, Chia tacks on another 'proof' system, a secondary algorithm or 'proof puzzle', whose answer takes a non-variable amount of time to calculate. This class of algorithms is called a 'Verifiable Delay Function' or VDF for short. They're called that because of the 'verifiable' delay that they introduce into a system; arrival at the answer means that you've run through a deterministic number of steps.

The solution to a VDF typically has the property that it is easy to verify but difficult (or time consuming) to calculate. Chia uses a squaring function to achieve this, where the number of required squaring operations is determined by a parameter `t`. `t` varies based on the 'difficulty' of the chain at the moment and the 'quality' of the farmer signature that it's attempting to prove. (Farmer signatures are one of the inputs to the VDF.) This is where being a lucky farmer and getting a 'good quality' signature for a block works out for you -- a good quality signature means that the Time Lord's VDF function will finish faster than any other farmer's signature. The first one to finish is most likely to be the highest 'quality' and therefore accepted as the chaintip to build blocks off of next.



The rate at which blocks are verified (and thus mined) is limited then by the difficulty factor which determines the `t` that is used to calculate the VDF result. A lot of good quality farmers (so lots of farm plots), will result in the difficulty rising; a decrease in 'farmer signature quality' results in the VDF increasing, which would bring down the difficulty at the next adjustment cycle. This is similar to Bitcoin.



#### Time Lord Incentives

One thing that I'm not super clear on is the incentives for Time Lords. Incentives on a whole aren't well covered in the Chia paper; it mainly focuses on the technical details of how to marry VDFs with 'space proofs'. The Chia chat on Keybase briefly touched on the idea that Time Lords won't be compensated for their time, only farmers who are participating in the sig-lottery will receive the block reward for each block mined.

In fact, the network doesn't even really need that many time lords, just enough to make sure that someone is sorting through all of the available signatures and then working towards the next proof that time has elapsed.



## Is Chia Actually 'Green'?

In some senses, Time Lords in Chia aren't much different from hashing miners in Bitcoin -- it takes computation power and time and calculate VDFs. I think that this might explain why there's a decided emphasis on devaluing the labor of Time Lords in the system -- adding incentives to the Time Lord function might create another mini-race to compute similar to Bitcoin. Such an arms race would greatly undermine Chia's ability to call itself a 'greener' alternative.

Instead, the protocol will initially pay out block rewards to lucky farmers, instead incentivizing users to fill their spare hard disks with 'junk' in return for a chance to play the Chia lottery. 

I don't think this is a terrible way to approach a chain, and I might be wrong about the exact incentive payout structure for Time Lords -- there wasn't any mention of payout schemes in the paper. I will say that I think it opens up the possibility for perverse incentives, or some amount of cheating incentive, in that Time Lords might only attempt to confirm their owner's plots, as that's the surest way to get paid. I can imagine a world where every big-time farmer basically runs their own Time Lord as well, so small independent farm vassals are at a bit of a disadvantage to big, corporate farms that have their own special-purpose built Time Lord machines that can crank out VDF proofs.



## Bald Patches

The Green Paper focuses pretty exclusively on the marriage of the two Proofs: of Time and Space, but leaves out a lot of details.

Specifically, there's no discussion of the format of data in the foliage blocks. This includes the UTXO set and transaction aggregation. Where do these blocks come from? Who composes them? It didn't seem like farmers would be the ones organizing and creating blocks to sign, but it's possible I missed something here that is stated.

I didn't really do a fair treatment of the implications of having a multi-headed chain, but to be fair neither did the paper. A lot of my questions on this are tightly tied to the UTXO set questions that I mentioned in the above paragraph, but mainly -- if you've got a 3-tip chain head, where does your transaction data need to be in relation to these chain-heads in order to be considered confirmed? How do you prevent a UTXO from being 'double spent' in two blocks at the same depth? I'm sure that the Chia designers have thought through this, as they seem like fairly obvious questions but it would have been more complete to have some discussion of the problem in the paper itself.

My biggest concern with Chia, however, stems from their lack of complete treatment of the incentive structure amongst the varying requirements and actors within their system. Take storage of the blockchain, for example. They're estimating 500kb blocks[3] every 5 minutes, or about 6MB per hour. Where exactly is this blockchain going to be stored? If you've got disk space to spare, it seems like it'd be in your best interest to turn it into farming plots, not a place to hold the chain's past transaction data. There's an assumption that 'nodes' will exist that host the Chia blockchain and participate in block propagation. On its face, this is analogous to how Bitcoin nodes work. There's a lot of nodes on the network that hold bitcoin, or act as live wallets, that don't participate in mining.  If Chia does grow to be as widely used as bitcoin, I can imagine this being a valid use case but in the early startup stage, I'd imagine it being difficult to bootstrap willing node hosters who aren't also interested in using their spare disk space to farm for lottery tickets.

One obvious way around this would be to make the minimum plot size larger than the expected blocksize in the near term. It's also possible that I'm grossly overestimating the total anticipated chain size, and this isn't actually as much of a conflict of interest as I surmise.

[3] I'm unclear what exactly constitutes a 'block' in this example; is that all 3 chain-tip blocks plus their associated foliage, or is it just a single foliage block?



## In Exitus

It's really interesting to see the benefits of the bitcoin hash function lottery laid out through the foil of someone else's attempt to replace it. Bitcoin is beautiful because of its simplicity -- its whitepaper is short yet well considered. I understand that it's likely Chia is relying on standard assumptions that were coined by the Bitcoin paper (and hence excludes them), but overall there is no denying that Chia as a system is more complicated and lacking in a few key details as to the practical interaction of its parts.

Nevertheless, I'm looking forward to the testnet launch in the next few weeks.

