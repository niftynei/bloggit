timestamp: 1688909345
date: 9 Jul 2023
time: 07:29
title: RIPEMD160's Untimely Death
tags: python, dev, ripemd160

---

## WiFi Free Context

I'm about 30k feet in the air as I write this, on a laptop that's decidedly not connected to the Internet.  I'm trying to Get Things Done using just the stuff I have already on my laptop.

I'm trying to use a [key expression generator tool](https://github.com/base58btc/seed_tools) called `seed_tools` I wrote to get some keys for making multisig descriptors. It's currently failing to run, however.

The root cause for the failure is that I just updated my operating system from the last Ubuntu LTS 20.04 to the current one 22.04. This means that Python has updated from v3.8 to v3.10 and that a bunch of underlying libraries on machine are also now updated.

It seems that one of the hashing algorithms that's normally accessible from Python ('ripemd160' via the `hashlib` standard library) is no longer available.

RIP.

## Why Does This Matter?

Basically I'm blocked on getting the path computation library working until I can get some WiFi and figure out how to fix it. So much for wirelss computing.

Here's the error I'm getting. Note that yes, I am putting some 'secret' data here; I'm not going to commit any real or test bitcoins to it, so it's fine to post.

	tourmaline:seeds (master)$ ./pub_derive 063e3875f9a6624a9bbd21520da869227fa15f9125dcdf84413370c952732cb7 m/0'/0'/1
	Traceback (most recent call last):
	  File "/usr/lib/python3.10/hashlib.py", line 160, in __hash_new
	    return _hashlib.new(name, data, **kwargs)
	ValueError: [digital envelope routines] unsupported

	During handling of the above exception, another exception occurred:

	Traceback (most recent call last):
	  File "/home/niftynei/dev/seeds/./pub_derive", line 121, in <module>
	    main()
	  File "/home/niftynei/dev/seeds/./pub_derive", line 101, in main
	    master_fgpr = find_fingerprint(privkey)
	  File "/home/niftynei/dev/seeds/./pub_derive", line 42, in find_fingerprint
	    rip = hashlib.new('ripemd160')
	  File "/usr/lib/python3.10/hashlib.py", line 166, in __hash_new
	    return __get_builtin_constructor(name)(data)
	  File "/usr/lib/python3.10/hashlib.py", line 123, in __get_builtin_constructor
	    raise ValueError('unsupported hash type ' + name)
	ValueError: unsupported hash type ripemd160


The `ValueError: unsupported hash type ripemd160` describes the problem well.


Short description of this code block: I'm running the command `./pub_derive` and passing in a master secret, encoded as hex, and a path that I'd like it to generate the
testnet xpub/xprv for. This will give me a key expression I can use for hand-composing a descriptor (which I can then import into bitcoin-core using `importdescriptor`).

Note that you wouldn't want to do this for any *real* bitcoin secrets, as it's best to keep those on hardware wallets etc. See appendix below about the robustness of the `seed_tool` library for a longer discussion about what to think about when doing computation with secrets!


## Where did `ripemd160` go? And how to fix??

This isn't the first time I've seen this issue -- Peter K Todd's last update to his Python bitcoin library, [python-bitcoinlib](https://github.com/petertodd/python-bitcoinlib), actually patched itself to fix this issue months ago.

The issue is that the ripemd160 hashing algorithm is now considered legacy in OpenSSL, which is where Python gets its hashing algos from. I was able to quickly enable it in the OpenSSLs configs (I followed this [StackOverflow](https://stackoverflow.com/a/72508879) post). (Editor's Note: post updaed after wifi was acquired).

The fix that [python-bitcoinlib](https://github.com/petertodd/python-bitcoinlib) took is to import a full re-implementation of ripemd160 and rely on that instead.  (Patch [here](https://github.com/petertodd/python-bitcoinlib/commit/3a5ec119af1e3aa3b96445074d319460bc655b10)).

Someone's since uploaded a small python library onto pypi which you can get here: [https://pypi.org/project/ripemd-hash/](https://pypi.org/project/ripemd-hash/).

I've since updated the `seed_tools` library, and everything works great.


## In Exitus

I find it increasingly hard to do meaningful development work while disconnected. In theory, the task I set out to accomplish on this flight *should* have been accomplishable, but I ran into an unexpected error.  If I had run this while connected to the Internet, I could have debugged and diagnosed it and gotten it working before embarking but I didn't think to do that.

Futher, it's crazy how interconnected libraries on your computer are! I had no idea that Python depended on OpenSSL for its crypto implementations. Maybe it's naive of me, but if something is shipped in a standard library I'd sort of expect it to be implemented in the standard lib? I think crypto primitives have always been like this -- weirdly available some places and not others, with poorly documented dependencies that border on implicit. Why are crypto libraries built this way?  I guess most cryptographers aren't really known for their software packaging and distribution chops...

Anyway, we're on our way down now, so I should be reconnected shortly and hopefully get this patched soon.

Until next time!



## Appendix: How Robust is `seed_tools`?

Is the `seed_tools` path finder production quality? I don't know. It touches secret key data, so I'd say "definitely probably not".

Here's why. 

First of all, as with any secret data, you really don't want it touching on any computer that's got stuff you downloaded from the Internet. The ideal place for secret data to live is on a computer as disconnected from the Internet as possible.

The only thing you should pass to and from a computer that holds your secret keys are pre-determined messages.

So running `seed_tools`'s `pub_derive` on your laptop, like I'm doing, with "secret" that you're planning to commit any real funds to is decidedly a bad idea.

The second thing about `seed_tools`, and maybe a reason you wouldn't want to use it even in a fairly secure computing environment, is that I'm not really sure how susceptible it is to 'sidechannel' attacks.

What is a sidechannel attack? It's where someone observing your laptop or computer is able to figure out your secret key based on the time that the computer spends in certain functions.

I lowkey think this is more of a problem when you're using the secret for actual computations -- the `seed_tools` library only takes hashes of the secret data, and if I understand correctly, those tend to be fairly the same in terms of rounds of computation indpendent of the input data.

Which is really where sidechannel attacks get their intel from -- different data input to the same function will take different amounts of time and maybe touch different codepaths depending on the input data. To avoid sidechannels, I'd super reccommend using the libsecp256k1 for any and all actual production key operations. The level of engineering and checks they have in place to make sure that the project is and stays constant time for all critical codepaths that touch secret data.


