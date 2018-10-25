timestamp: 1540494752
date: 25 Oct 2018
time: 12:12
title: Reproducible builds with Bitcoin, Tor and turtles
tags: bitcoin, tor, reproducible-builds, turtles

---

Within the last few years, modern open source software, particularly ones that deal with vulnerable or important systems[1], have worked to make the built binaries that they publish for download verifiable. A binary is considered verifiable if anyone can download the source code, build it, and end up with a binary that exactly matches the publicly available ones.

Ending up with an exactly matching binary, however, is a non-trivial task. As such, software projects such as Bitcoin and Tor have undertaken the project of making their builds deterministic and reproducible.

There's two parts to ensuring deterministic, reproducible builds. The first is to eliminate any amount of non-determinism from your build itself. The second is to remove any amount of non-determinism from your build environment.

The first is typically managed by removing timestamps, fixing the order of outputs or inputs via a stable sorting algorithm, and stripping out variable version information. You can see a more through treatment of the various sources of non-determinism in builds on the Reproducible Builds working group's [website](https://reproducible-builds.org/docs/), under the heading "Achieve Deterministic Builds".

The second, removing non-determinism from your build environment, typically entails creating a clean room container that the build will take place in.

As part of an investigation to better understand reproducible builds, I spent some time walking through both the Bitcoin and the Tor project's reproducible build process. What follows is a short overview of how the Bitcoin reproducible build process works and a comparison between the Tor project's build process and Bitcoin's. Finally I'll talk a bit about turtles, a work in progress project that takes the trustworthiness of reproducible builds a step further.

## Building Bitcoin

Bitcoin, in keeping with the spirit of the project, relies on a public, multi-party verified binary. Any individual can download the source code for bitcoin core from Github, check out a tag, and then build the project. Gitian, the build verification tool that Bitcoin makes use of, outputs an assert file that lists all of the inputs, outputs, and packages used to build the source along with the SHA256 hash of each of them. An independent verifier then signs this file with their PGP key and submits a pull request to the gitian.sigs repository. I did this a few days ago, for the linux and windows versions of the binaries; you can see the PR I submitted [here](https://github.com/bitcoin-core/gitian.sigs/pull/887). It's got two assert files, one for the linux binary and one for the unsigned Windows binary, plus two separate PGP signature files, which is just the assert file signed with my PGP key.

Bitcoin's reproducible build setup uses a script-wrapped version of the [Gitian builder](https://github.com/devrandom/gitian-builder). There's a couple of steps involved in setting up your machine to do a reproducible build and this [doc](https://github.com/bitcoin-core/docs/blob/master/gitian-building.md) in the bitcoin-core notes does a good job of walking through the specifics; I'll go over them briefly.

First, you need to decide how and where you're running Gitian itself. If you're running a Debian/Ubuntu distro you can set up a secondary user on your computer to 'host' Gitian builds. You can also set up a virtual machine (via Docker or VirtualBox) to host Gitian builds within. I'm sort of lazy, so I went the route of setting up a secondary user on my machine to run Gitian in. 

Once you have Gitian configured, you can start the Bitcoin build process. Mostly, this involves cloning the bitcoin gitian.sigs repository (where it'll create the output asserts files for you) and then running `gitian-build.py`, a [script](https://github.com/bitcoin/bitcoin/blob/master/contrib/gitian-build.py) included in bitcoin/bitcoin's contrib directory.

`gitian-build.py` acts as a wrapper around gitian-builder, that organizes the build process into a few general tasks: setup, build, verify, and sign. Once you have Gitian setup, you can run the verified build process with the following command, where `username` is your github handle, and `0.XX.0` is the source tag that you'd like to build and verify.

```
    ./gitian-build.py --detach-sign --no-commit -b username 0.XX.0
```

The gitian-build.py Bitcoin script has a couple of extra options, that you can run, for instance, using `-B` instead of `-b` will also build signed versions of the Windows and OSX binaries. To be honest, I'm not sure what the difference is between a signed and non-codesigned binary, but there's options for both!

You may notice that my PR for verifying the 0.17.0 Bitcoin binaries is missing the OSX binaries; in order to compile the OSX binaries (particularly on a non OSX device) you need to install [extra packages](https://github.com/bitcoin-core/docs/blob/master/gitian-building/gitian-building-mac-os-sdk.md).

There's a few more pieces of Bitcoin's Gitian setup that I should mention. Both the gitian builder and the gitian-build.py scripts are wrappers for ordering and running the actual build script. So where is the actual build script for bitcoin? They're defined as a set of YAML files, in [`bitcoin/contrib/gitian-descriptors`](https://github.com/bitcoin/bitcoin/tree/master/contrib/gitian-descriptors). There's one for each of the build targets (linux, windows-nonsigned, windows-signed, mac-nonsigned, mac-signed). The `gitian-build.py` file is hardcoded to load these YAML files into gitian-builder, depending on what options you've passed it and your current system setup (ie do you have the OSX dependencies downloaded?).

Now that we've got a pretty good idea of what the setup is that Bitcoin's established for the build, let's talk a bit about how Gitian itself works. Gitian itself will spin up a container (defaults to KVM, but can also be configured to use LXC) that it will download the listed dependencies into (these are specified in the YAML file), and then run the build script (also outlined in the YAML file).

After the build has completed, Gitian's `gverify` script is run against the built binaries, which outputs an assert file. These are the files that you sign and upload to Bitcoin's `gitian.sigs` repo, signalling that you also have independently verified the Bitcoin binary!

Notice that if you've setup Gitian to run inside a VM on your machine, the build itself will take place inside yet another container, one spun up by Gitian itself. It's a bit of a build turducken.

There's a number of reasons for this. The container that Gitian spins up has its time set to a known value, such that all builds use the same time, it also uses the same container architecture, which ensures that the file system irregularities are hopefully largely eradicated. Having users to use the same architecture for the build machine removes a good deal of possible variability from the build process.

## Comparing Bitcoin and Tor
To be honest, I didn't spend a lot of time digging into the Tor build process, but a few things about it stuck out. First, they use something called [rbm](https://rbm.torproject.org/), which is based on [runc](https://github.com/opencontainers/runc), another container based solution. They used to have a Gitian driven process, but moved away from it - their original Technical Details [blog post](https://blog.torproject.org/deterministic-builds-part-two-technical-details) on reproducible builds mentions Gitian, but their links to the build setup instructions leads to a [git commit](https://gitweb.torproject.org/builders/tor-browser-bundle.git/blob/HEAD:/gitian/README.build) about how it's been deprecated. I didn't do a deep dive into how rbm or runc works, but this comment on their [docs](https://trac.torproject.org/projects/tor/wiki/doc/TorBrowser/Hacking#BuildingOfficialTorBrowserReleaseBinaries) leads me to believe that I'm not missing much.

> We have written a pair of blog posts that describe in more detail [why this is important](https://blog.torproject.org/deterministic-builds-part-one-cyberwar-and-global-compromise), and the [technical details](https://blog.torproject.org/deterministic-builds-part-two-technical-details) behind how this previously got achieved when using the [Gitian](https://gitian.org/) system, if you are curious. The new build system based on rbm is working similarly and is facing pretty much the same issues.

The new rbm based process isn't well documented, but appears to be invoked when you run `make` - in this way it's much easier than the Bitcoin Gitian build process, as you run the `rbm` process every time you build the project.

Finally, Tor doesn't have a set of signed verified assert files, rather you can individually build and [check the shas](https://www.torproject.org/docs/verifying-signatures.html.en#BuildVerification) yourself. It feels incredibly Bitcoinic to have a publicly available set of signed signatures that verify the build, whereas with Tor you have to do it independently, if you care, rather than having a published set of signed verifications.

## Turtles

There's a problem with Gitian, however, in that you're largely depending on the binaries of the packages you download from Debian being uncompromised. If, for some reason, the gcc compiler binary that you've downloaded from the Debian repo is compromised, all of the software that you compile with it will also be compromised. Gitian trades off relative speed for some amount of trust in the Debian packages.

There's another project[2]  that's currently in the works that would replace Gitian. Instead of downloading a VM to run a build in, you'd instead build an entire runtime from scratch, first by downloading the source for a compiler, and then compiling another version of gcc, etc. What were packaged binaries that were downloaded in a VM in Gitian are now source compiled on your machine. The project's still a work in progress, but if successful, it would both decrease the required, systematic trust for build verification, as well as potentially exponentially increase the time required, at least on first run.

If you're curious, you can check out turtles [here](https://github.com/theuni/turtles).


[1] Bitcoin (money) or the Tor project (anonymity) are two examples that currently have a public reproducible build process. Debian (computing platform) is currently in the beginnings of an enormous effort to create a reproducible build process for all of the packages that they publish.

[2] Thanks Carl for clueing me in to the work you've been doing on this!
