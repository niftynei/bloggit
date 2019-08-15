timestamp: 1565892368
date: 15 Aug 2019
time: 13:06
title: Quick Note on Malleability
tags: bitcoin, sigs, malleability

---

tl;dr: There are a bunch of potentially valid signatures for the same transaction hash and public / private key pair. Read on to find out why.

## Problems
I'm working on getting my dual-funding implementation working. I've written a bunch of code, and now I've got to make sure it all works as expected. To do this, I've been writing 'protocol' level tests using a framework one of my teammates put together a few weeks ago. It allows you to specify wire calls that the test runner will send to the program under test, and then verifies that it receives the correct result back.

It's been a really great tool for debugging all the small programming errors that I've got in the code I wrote. Recently I ran into a verification error that stumped me.

The test files that I'm using are generated using a script that calls bitcoind. It builds a 'funding transaction' and all the required signatures, and then outputs that into a test case, that I can run the test runner against.

Part of what it generates is the expected signature data that the c-lightning node will produce for the signature. When c-lightning sends back its signature data, the test runner verifies that the bytes exactly match what it's expecting.

The problem I ran into is that the bytes aren't matching. The signature that my test-script maker produces is not the same as the signature data that c-lightning generates.


What's equally confusing, at least to me, is that the transactions are identical. So are the keys that they're signing with. How are they getting different signatures then?

Transaction they're both signing (they're signing the first input)

    02000000023f05da71fb470a53807eb01db4a9220941e3737fa44bccd1fb00f1968c98396c0000000000ffffffff3f05da71fb470a53807eb01db4a9220941e3737fa44bccd1fb00f1968c98396c0100000000ffffffff01a0e2160000000000220020c46bf3d1686d6dbb2d9244f8f67b90370c5aa2747045f1aeccb77d818711738200000000

Witness data that I get from bitcoind:

    3044022078afb02e8c8802f65fe92096eb851c623a3bfb631cc8e41878728f35fc94448202203958fb2ed3d58fcd30d1bdd7ab90e1e2dfb524d8423c457719065e7ea5bf98c001
    02d6a3c2d0cf7904ab6af54d7c959435a452b24a63194e1c4e7c337d3ebbb3017b

Witness data that I get from c-lightning:

    3045022100e4ac2f9b298df16be6c287f7b452468ca09d79816f89674ea4fbe0999a3ef6b80220179186b253e1df02714a01b2c19144efa141a7072049e51cddd299572a0cbbc801
    02d6a3c2d0cf7904ab6af54d7c959435a452b24a63194e1c4e7c337d3ebbb3017b

You'll notice that the second line of these is the same `02d6a3c2d0cf7904ab6af54d7c959435a452b24a63194e1c4e7c337d3ebbb3017b`, but the first line is different.

I thought that transactions in SegWit were supposed to not be malleable? Why are my signatures different?

## Short Explainer on ECDSA Signatures
Turns out that every ECDSA signature includes a nonce, called `r`. This is a randomly chosen number. The data that is sent in a 'bitcoin signature' includes this `r` value and the actual signature `s`. You use `r` and the public key to verify that the signature is correct for the transaction.

In fact, the second line that was the same above, `02d6a3c2d0cf7904ab6af54d7c959435a452b24a63194e1c4e7c337d3ebbb3017b`, is the compressed public key. We know that both c-lightning and bitcoind are using the same public / private key pair to sign it. The 'problem' is that the `r` values are different.

This isn't actually a problem. Both signatures are valid. We can dissect the signatures to get the `r` values out.


c-lightning signature, dissected:

    3044 02 20 
        // r   78afb02e8c8802f65fe92096eb851c623a3bfb631cc8e41878728f35fc944482
         02 20 
       // s   3958fb2ed3d58fcd30d1bdd7ab90e1e2dfb524d8423c457719065e7ea5bf98c0
    01

bitcoind signature, dissected:

    3045 02 21
        // r 00e4ac2f9b298df16be6c287f7b452468ca09d79816f89674ea4fbe0999a3ef6b8
         02 20
        // s 179186b253e1df02714a01b2c19144efa141a7072049e51cddd299572a0cbbc8
    01


The `r` value for the bitcoind signature is `78afb02e8c8802f65fe92096eb851c623a3bfb631cc8e41878728f35fc944482`. The `r` value for the c-lightning signature is `00e4ac2f9b298df16be6c287f7b452468ca09d79816f89674ea4fbe0999a3ef6b8`. Clearly not the same value.

Which is why the signature data is different. Sigh.

## What Happened to Malleability?
SegWit is known for having made transactions non-malleable. This does have something to do with the signatures, but not in the way that I thought.

Prior to segwit, you could take a transaction, change the transaction enough to change the transaction id, and still use the same signature. Which is to say that one signature would be valid for different versions of the same transaction. This is bad for lightning, in particular, because we rely on transaction ids staying the same, as we build transaction chains for commitments and the like.

This kind of malleability has to do with the range of transactions that any given signature is valid for. Basically, it means that one signature is only good for that one version of the transaction. If you have a signature, you can't change the transaction and publish it and still have the signature be valid.

It says nothing about the range of valid signatures for that one transaction.

A short diagram might be kind of nice here.

    One Signature -> Only valid for one transaction.

    One Transaction -> Lots of valid signatures! (with different `r` values)


So, are my test cases ok? Yes they're perfectly fine. What's the solution here? Probably not to verify the signature data that the node under test sends back. I should really just check that the public key works, and do a few modifications so that the node under test has to have their published transaction be accepted by bitcoind in order to continue (currently the test runner also broadcasts the transaction).

# In Exitus
Malleability only applies from the "I have a signature, what transactions is it good for" sense. Not "I have a transaction, what signatures are valid for it?".
