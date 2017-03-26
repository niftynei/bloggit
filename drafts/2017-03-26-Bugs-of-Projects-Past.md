timestamp: 1490561064
date: 26 March 2017
time: 13:44
title: Bugs of Projects Past
tags: bugs, reflections, race-conditions, internationalization
---

## tl;dr: there is no such thing as a 'worst' bug

A question was put to me last week that I didn't have a ready answer for: what's been the worst bug you've encountered?  

I've enocuntered plenty of bugs in 7 years of software development, but when asked directly have trouble bringing a memorable one to mind.  Once they're solved they're hard to remember as being difficult.  Or maybe I'm too used to things crashing, or to dealing with those once in a Samsung release kinds of problems, that none of it seems re-telling.  You deal with Android long enough and crashes on specific systems due to differences of opinion on how an API should be implemented and function become mundane.  Once you have an explanation for a bug it seems far less mysterious or interesting.  And the tenth time you're blaming Samsung, the previous nine bugs are marginally less memorable.

## International Incidents

That being said, I do have a story that, with much prompting, I'll often drag out. It comes from the Android eco-system, from a logging framework that I wrote as one of my first projects as a Professional Developer.  

In the first version of the library, I sent back logs with localized datetime strings.  This works really well in every language that I tested it in; it works less well in Arabic, whose alphabet uses its own number glyphs.  The Arabic number timestamps were incomprehensible by our log ingestor, which meant every Arabic language Android phone was successfully avoiding our attempts to log information about their system.  

Arabic numbers are quite beautiful.  For a while thereafter, Arabic became my go to language for testing RTL layouts (right to left), even after I discovered there was a debug RTL language setting that was in English but backwards. Dear lord, I even made sure that the Electric Objects app looked decent RTL.  I'm a sucker for weird corner case testing.

---

You can also ask me anything about that one time that I spent a weekend hacking a currency selector into the Etsy Android app and introduced a bug that crashed the app on open for users on phones that had a non-existent locale set as default.  Lucky for me this wasn't a lot of users, but coding around it was hard as heck -- deciding on a fallback locale felt fraught with hegemonic implications.  

Much later, a co-worker re-wrote one of our navigation drawers in such a way that made it blank for users with their language settings set to Persian.  His mistake made me feel a bit better about my own international failures.

A fascination for corner cases would explain my strange fetish for internationalization.  While working on the currency selector, I spent a lot of time on the formatting function for prices.  There are a lot fun, semi-arcane things to know about price formatting.  For example, in some countries (like Sweden) you put the monetary symbol after the price.  In America we write $10; in Sweden they'd write it as 10$.  A lot of currencies have their own symbol for currency, like the pound or euro sign.  In other currencies they use the same symbol as the US, the $, but annotate after the amount to denote which version of dollars they're talking about.  A Hong Kong price would be $10HK[1].  Japanese don't use decimals for their prices, you just truncate it at the whole yen.  The Swiss franc doesn't have a currency symbol, it's usually only annotated with the letters CHF after the value.

If you really want to get trippy, decimal annotation changes between languages too. Canadian French put spaces between their thousands and use the "," as a decimal separator (1 000 000,34), whereas English Canadians do it like the Brits do (1,000,000.34).  Colonialism lives on.[2]

The Java libraries on Android had a fairly complete API for figuring out how many decimal places to show, and what punctuation marks to use, but the before and after split for prices wasn't exactly correct or necessarily nice to look at.  Not to mention that the code itself was rather verbose.  Of course, after I had figured most of this out, someone on the team (most likely my engineering lead) mentioned that it's best to let the server have all the logic for what to show people instead of embedding it in the client as it's easier to track down and fix bugs that originate with the server.  Which would have been all well and good if the server's price formatting logic had been anywhere near as complete as the Java + custom logic we wrote for the app.  One nice thing about phones is that they provide a locale and language preference for a user, which you can use to figure out whether to display fonts in British or French Canadian.  The server side location preferences were good but not French vs British Canadian good.

## Time Bugs

Timing errors led to some pretty memorable bugs.  One of the first ones I ran into was while I was at Etsy, working on developing a feature using an emulator.  For those of you unfamiliar with mobile development, an emulator is like having a fake phone that you run inside of your computer.  It's basically a virtual machine that runs all the same code that runs on a cell phone.  The only difference (in theory) is that you don't need the phone hardware.  And you can load up & run programs on the same machine you're developing them on.

The old school Android emulators were slow, especially when compared to the Apple iPhone simulators.  Simulators use the host computer's chip architecture and do a rough approximation of the same program on top of a different instruction set; emulators have virtual chips that they run the actual program against. Emulators run hella slow because there's more layers of software involved, but in theory are more accurate as far as exposing bugs.  Once you started up an emulator, you tended to keep it up as they often took 3-4 minutes to launch.

Anyway, I was working on a new feature for the Etsy Android app, and kept running into a problem with the API requests I was making.  The errors didn't make much sense though -- they seemed to indicate that there was something wrong with the certificate on my app, which had nothing to do with what I had changed or was building.

I didn't have a very good understanding of how network security worked at the time -- I knew how to set up a proxy with a man in the middle to read my network traffic (/me pours one out for Charles) but that was just me following a very simple wiki page.  It turned out that something about ssl and/or our pinned certificate could only work if the server time was within 2 hours of the phone's clock time.  Which is all well and good on a normal cellphone that gets its time from cell phone towers on the regular.  However, the emulator that I had been working on, while it had started off with a clocktime that matched that of my laptop, when I suspended my computer overnight the emulator was also suspended. The difference being that it didn't have a separate battery to keep track of the time like my laptop does (more about these later).  The clock fell behind by exactly the number of minutes the laptop slept for.  Which meant that network requests were failing because the SSL handshake timestamps fell outside of the 2 hour window.  Once I knew the problem it was easy to just restart the emulator.  I had to start restarting the emulator on the regular and eventually ended up just using real devices for testing because it was faster and easier than dealing with the slow pile of morass that was the Android emulator situation in 2013.

Timing issues came back for some fun when I worked at another job, where we were building proprietary Android devices. Basically someone forgot to put batteries on the bill of materials for parts that we'd need for manufacturing.  You need batteries to keep the clocks in sync while the unit is powered off.  Most electronics have a battery powering the clock, round the clock.  One of our engineering leads had to go find a couple hundred batteries in Arizona while they were attempting to get the devices manufactured the first time around. I believed they got them all in before they were shipped, thank goodness.

One of the hardest bugs I ever had to track down was a race condition (time again!) over a super slow, very spotty network.  The problem was in the OAuth renegotiation from a client to a server.  Normally OAuth tokens expire after a few hours and the application asks the server for a new one but there were a bunch of reasons why this check would sometimes randomly fail in my app, most of which could be traced to a lack of good locks around the refresh token sequence in the client app.  

I did a lot of work to lock the refresh token down to a single thread and moved our network requests to a queue rather than the firehose structure they had been using before, thereby completely erasing the race, but we still would get reports from the field of devices that were randomly logging themselves out due to an expired token.  Finally, I managed to replicate a condition where a device on a bad network could send off a request to the server, successfully generate a new token server side (thus invalidating the current token), and then never actually receive the packet with the new token on the client side.  At this point your client application is basically hosed -- there's no way to recover without the user logging in again since as far as the server knows it sent you good information.  We knew that a surprisingly large majority of devices we had manufactured had less than stellar wifi chips in them so we did what any self respecting software engineering team would do and gave up.

This problem, unique as it is, does highlight an interesting property of network requests -- that they're largely assumed to be successful.  I've worked with a lot of server teams, but i've never heard of anyone writing rollback protocols that are triggered by failed TCP deliveries.  If you know of one, I'd love to hear about it.

## Send Me Your Bugs

I also love hearing about bugs. I also love helping solve bugs, though I'm not great at it. If you've got a particularly juicy one that you'd like to tell me about, tweet it over to me [@basicbitchsofkw](https://www.twitter.com/basicbitchsoftw).




[1] Big thanks to my Canadian co-worker for writing this into our library, I wouldn't have known about it otherwise.

[2] Another front of formatting differences between languages: quotation marks.  I've never seen a library that accurately translates quotation marks between languages. I feel like I've seen Google Translate do this elegantly, but a quick check shows that to be mistaken.
