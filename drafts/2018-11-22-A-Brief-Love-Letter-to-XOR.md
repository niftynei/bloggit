timestamp: 1542916617
date: 22 Nov 2018
time: 11:56
title: A Brief Love Letter to XOR
tags: xor, boolean, love-letter

---

I'm taking an online crypto class[1] right now, and it's been forcing me to get more intimate with the bitwise operator XOR. On top of being incredibly lightweight, there's a few really cool things that XOR can do. 

In the spirit of the Thanksgiving season, here's a brief love letter to my favorite little boolean operator, XOR.

## What is XOR? 
XOR stands for 'eXclusive OR', where 'or' refers to the boolean logic operation. What does that mean, a boolean logic operation? Briefly, it's what conclusion you draw from two truth values. It's kind of like a predetermined agreement mechanism. Boolean logic is a rule that you apply to two results, to resolve those two results to a single true or false. 

A simple example is probably helpful. Let's say that we've got two voters, and we're trying to take their two votes (either YES or NO) and return a single decision for the 'election'. How these two imaginary voter's votes are counted is the role of the Boolean logic operator.

There's two, fairly common boolean operations that you might have heard of before: and & or. The decision for 'and' is fairly intuitive: if both voters vote YES, then the result is YES. Otherwise, the result is NO. We'll only get a final YES vote if both of the people we're asking say YES. If either voter votes NO, the final result from the boolean operation will be NO. The 'and' decision framework requires 100% agreement.

'Or', on the other hand, says that if either voter says YES, then we'll take the result to be YES. The 'or' decision framework requires only one single 'voter' to say YES in order to return a YES.

So what is XOR? XOR only returns true if the voters disagree. If both voters say YES, 'xor' will return NO. Same thing if both voters say NO: 'xor' will still return a NO. It's only  when one 'voter' has chosen YES and the other NO that XOR resolves to a YES. It doesn't matter which voter says YES and which one NO, as long as the voters disagree XOR returns YES.

Why is it called exclusive or? Great question. I have no idea, but you can probably find out on the [Internet](https://en.wikipedia.org/wiki/Exclusive_or).

## XOR As Your Encryption Friend

XOR does some pretty fancy things. If you take a series of bits and XOR it together with another series of bits, the original series of bits can be retrieved out of the resulting string, but only if you know what the second series of bits was. It's almost impossible to tell what the original bit series was. Here's a quick example, to show you what I mean.

    // If I take the bit series 0101 and XOR it with 1010  
    0101 xor 1010 =  1111  

A result of `1111` doesn't tell you what bits belong in which of the strings that you xor'd together.  You could have xor'd 1111 with 0000. Or 1100 with 0011. But! If you do happen to know one of inputs, you can easily extract the other.

    // If I know 1010 and the result, 1111, I can extract the other input   
    1010 xor 1111 = 0101  

This is incredibly useful in cryptography. If you take a message and XOR it with a 'secret key' (a random series of bits) as the same size as your message, viola, your message is now encrypted. If your 'secret key' is a random enough series of bits, then it will be practically impossible for anyone to know what the original message bits were. To decrypt this message, all you need is the encrypted message and the key that was used to encrypt it.[2]

    // How to encrypt a message   
    message xor key = encrypted_message  
     
    // How to decrypt a message  
    encrypted_message xor key = message  

## Other XOR Magic

XOR has a little bit of 'magic' that happens when you use either a set of all 0's or all 1's to XOR against. 

You can 'bitflip' any series of bits by XOR'ing it with a series of 1's. 

    // Flip a bit set!
    111000 xor 111111 = 000111

XOR'ing by a set of 0's is an 'identity fucntion' -- it'll return the same series of bits as what you originally XOR'd in. It's probably not a good idea to use a set of 0's as your encryption key -- it'd be like putting your message behind a piece of glass.  XOR'ing by 0 is transparent!

    // Show me the same!
    111000 xor 000000 = 111000

## In Exitus

The next time you use encryption to send a message with a friend over the Internet, give a little thanks for your crypto workhorse bestie, XOR.





[1] Dan Boneh's Crypto I on [Coursera](https://www.coursera.org/learn/crypto)  
[2] This method of encryption is generally called the One Time Pad encryption, as the key is as long as the message. So long as you never reuse the same key on a different message and your key is a random stream of bits, this method of encryption (xor'ing the message with a key) has what's known as perfect secrecy.  The biggest, practical problem with this method of encryption is that the person decrypting your message needs to know the key.  You'd need a secure way to send them the key, as anyone who gets the key can then decrypt the message. The key is as long as the message though! If you have access to a secure method of communication that can transmit something as long as the message, you should just send the message itself over that secure communication channel. It's just as long, and your chatting partner won't have to decrypt it. This equal length key problem is why they say that perfect secrecy is practically impractical.
