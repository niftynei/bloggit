timestamp: 1546501592
date: 28 Jan 2019
time: 22:00
title: Reflections on the Art of JSON in Golang
tags: json, golang, encoding, static, reflection

---

Last month, I put a good bit of time into writing a little [library](https://github.com/niftynei/golight/tree/master/jrpc2) to help bridge the gap between the requirements of JSON-RPC's [spec](https://www.jsonrpc.org/specification) and Go. 

The Go standard library provides functionality for the version 1.0 of JSON-RPC. There is no standard library implemenation for the 2.0 spec, but there's plenty of other [implemenations](https://godoc.org/?q=json-rpc+2.0), some of which seem to get pretty close to the idioms that I landed upon for my version of it. I ended up writing my own library for a few reasons. First off, I wanted some practice implementing a spec. The work I'm looking to do for lightning over the next few weeks is basically spec writing and implementation; it seemed like a good idea to get some practice following a very simple and well documented spec like the JSON-RPC 2.0 spec. 

Secondly, my motivation for needing a JSON-RPC implementation is that I was looking to write a 'driver' for the new plugin functionality that Christian Decker has been adding to c-lightning. c-lightning's plugins have a few very specific needs[1] that would likely require modifying another JSON-RPC implementation. Plus there's the overhead of figuring out how another person's library works. 

I leveraged the json encoder/decoder from the Go standard library as much as possible. The trickiest bit was getting a good idiom put together for how parameters are declared and marshalled into command calls. There's a lot more that went into putting the whole plugin/rpc thing together, but I think for this post it'd be the most delightful to just walk through the design decisions that I made for the way the params parsing works.

## Problem Statement

Let's talk a bit about what's going on during a JSON-RPC command message exchange. The general gist is that there's a client who wants to execute a method on the server. In order to do this, we need to tell the server what method we'd like to call (by providing a `name`) and then also passing in any and all of the information that the method needs (these are typically called 'parameters' or 'arguments'. The JSON-RPC spec terms them `params`).

Our job then is to provide an interface such that the client can smoothly call a method and then receive a response from the server. The ideal interface for such an interaction would look identical to any normal method call. For example:

    func hello(greeting string, to User) (string, error) {
        // magically invoked on the server
        return "result", nil
    }


Go provides a json marshaler/unmarshaler, a package called `encoding/json`. The problem is that the marshaler works on structs, not method signatures. 

Instead, `jrpc2` takes the tack of asking users to write their method calls as structs. Here's how the `hello` method that we saw above would be rewritten as a struct.

    type HelloMethod struct {
        Greeting string `json:"greeting"`
        To *User        `json:"user,omitempty"`
    }


Each of the method parameters is now represented as a public struct field. When we send this across the wire, we'd expect our library to generate the following json:

    {
        "jsonrpc":"2.0",
        "method":"hello",
        "params":{
            "greeting":"hola",
            "user":{
                "first_name":"Finn",
                "last_name": "Neal"
            }
        }
    }

We need a way to signal to our library that this is in fact a 'method' that our `jrpc2` library knows how to marshal into a valid command request object. We do that with an interface, that defines a single method, `Name()`. Any struct that implements this method will be considered ok for sending over the wire to the server.


    func (r *HelloMethod) Name() string {
        return "hello"
    }


We still need a way to pass this method call to the server, but from a client perspective that's all we need in terms of defining a new method.


## On the Server End

c-lightning's plugin framework requires your app to serve as both a JSON-RPC client and server, since users can invoke method calls from c-lightning that are then passed to your plugin to execute. Server RPC method objects are mostly the same as above, with two additional methods added to the interface, `New` and `Call`.

When the server receives a request from a client, it 'inflates' the json request into a `ServerMethod` object. The `New` method gives you the ability to do any initialization or setup needed for the new instance. If there's state that needs to be shared between instances of the `ServerMethod`, you can pass them along here.  Here's an example of where you want a New version of the GetManifestMethod to have access to the plugin object.


    // definition
    type GetManifestMethod struct {
        plugin *Plugin  // private so it's not mistaken for a method parameter
    }

    func (gm *GetManifestMethod) New() interface{} {
        method := &GetManifestMethod{}
        method.plugin = gm.plugin
        return method
    }


This is nice because it lets you share state between method calls.  Then there's the actual `Call` part of the `ServerMethod`, which obviously is where you do work. Since the 'inflated' struct is 'passed in' as the object of the call (i.e. the whole `(gm *GetManifestMethod)` declaration, you have access to all of the parameters that were sent by the client.

    func (gm *GetManifestMethod) Call() (jrpc2.Result, error) {
        // example of using the plugin obj
        for i, sub := range gm.plugin.subscriptions {
            // ...
        } 
        return result, err
    }


If you return a non-nil error from the Call, the server will ignore the result and send the client back an error object. As a final note, if you want your Result to be formatted for json correctly, you'll need to add good json annotations for its fields. We use the default `encoding/json` package to marshal and umarshal everything over the wire.


## A Few Things on The Way to the Forum

The trickiest part of the whole `jrpc2` mechanism is the custom marshalling for the param struct. The JSON-RPC spec defines two different ways that params can be passed from the client: either as an ordered array or as a named dict. i.e.


    // As an ordered array 
    "params": [1, 2, "hello", {"inner":"object"}]
   
    // As a named dict
    "params": {"first": 1, "second": 2, "greeting":"hello", "extra":{"inner":"object"}}


Basically, we're wrapping client calls in an outer object, with the 'method struct' being serialized into the params. `jrpc2` includes methods to serialize calls as either an ordered array or a named dict, but defaults to the named dict when used as a client. It's worth noting that the order of appearance of fields in a method struct is how they'll appear in the array. If you re-arrange the ordering, and have switched it to use 'vectorized params' (aka an ordered array) then they should be switched in the param call.


### Reflection Dragons
In order to do this correctly, I ended up digging in pretty hard to the `reflect` library. There's a bunch of nuance around deflating and re-inflating objects from json that I really struggled to find good resources on. Most golang articles on reflection stop and start with Rob Pike's article on the Go Blog, [The Laws of Reflection](https://blog.golang.org/laws-of-reflection), but it doesn't dig in much beyond the basics.

Re-creating a new version of the method struct is fairly straight forward, you can just call the `New` method.  However, for any param that is a pointer on the method struct, we have to allocate a new 'extra' object and then run the json Unmarshaler on it. There's a few steps to this.

First, we need to determine what type of object we should be inflating. We can use the method struct's field declaration to determine what type of new struct to inflate.  

When you 'inflate' a new object from a field type, it initially comes to you without a pointer address, because no memory has been assigned to it yet. 

Short aside. Originally, method structs on the server didn't have a `New` command, instead I inflated it directly. Figuring out how to do this took me some amount of time. Unfortunately, I replaced it with the `New` method, as I wanted a way to be able to share objects across every method call, and then I completely (and accidentally) destroyed my git repo and lost my commit history so I can't show it to you exactly but, it involved inflating a new copy from an existing one and then figuring out a way to get it assigned to an address space so that we'd have a pointer to pass around. This isn't *such* a problem for sub-fields on the struct, since creating a new one allocates space for all of its member fields.

The only place that you need to do allocate a new object is for a field on a struct that's a pointer. Here's a short example.

    // Method struct to inflate
    type IdkMethod struct {
        Clue *Clue
    }

When we're serializing this to json, we'll pass the `Clue` object as serialized json (if the pointer exists) or pass null if there is nothing assigned. On the server side, we need to 'inflate' this back into a `Clue` object, with a pointer that we can assign to the new `IdkMethod` object.  Here's how we do it.

    if fVal.IsNil() {
        fVal.Set(reflect.New(fVal.Type().Elem()))
    }


We use `reflect.New` to create a new version of the type of field. We have to use `Type().Elem()` because the type is a pointer -- we want to create a new struct of the type of the element that the pointer is pointing at, not a new 'pointer to element'.  `reflect.New` returns a pointer to the new object that it has just allocated, which we can directly set the value of that field (e.g. `fVal`) to.

Another short aside, I don't know how you're supposed to figure out how any of this more complex pointer magic works if you've never dealt with pointers on a fairly intimate level.  Language level abstractions are great ...until you fall into the pit of object marshalling.

There's a lot of other little neat things that I ended up needing to figure out to do, like filling in a slice or map. Briefly, here's the code for inflating a set of map objects:


        fVal.Set(reflect.MakeMap(fVal.Type()))
        // the only types of maps that we can get thru the json
        // parser are map[string]interface{} ones
        mapVal := value.(map[string]interface{})
        keyType := fVal.Type().Key()
        for key, entry := range mapVal {
                eV := reflect.New(fVal.Type().Elem()).Elem()
                kV := reflect.ValueOf(key).Convert(keyType)
                err := innerParse(targetValue, eV, entry)
                if err != nil {
                        return err
                }
                fVal.SetMapIndex(kV, eV)
        }

You can find all of these great things and more at work in the `innerParse` function of the `jrpc2` library. Currently it lives [here](https://github.com/niftynei/glightning/blob/master/jrpc2/jsonrpc2.go).

## In Exitus

I'm half-convinced there's a construction of param parsing where you only need to declare the method, and you can somehow 'shadow compose' the request objects that I settled on above. But!  After using the library for making a few plugins plus the RPC object for c-lightning calls, I think there's a nice balance between declarativeness and flexibility.  Particularly, while at first it seemed a bit redundant, having an explicit `Name()` function hook for the `Method` objects nicely decouples the declared method name from whatever is the nicest way to express it in Go.

By way of example, there's an RPC method on c-lightning called `dev-rhash`. With the `Name()` idiom, it's easy to handle this: 

    func (r *DevRhashRequest) Name() string {
        return "dev-rhash"
    }


Under the 'more syntactically sugarful' and also imaginary (because I'm not entirely certain you can do it) way that I've been imagining, you'd have to write the Go method like this:

    func dev-rhash() string {

And then every place you wanted to use it, you'd have all kinds of ugly `dev-rhash()` calls. Say nothing of the fact that Go uses upper and lower case letters on functions and objects to denote the 'visibility' of a method -- as written you wouldn't be able to call this method outside of the containing package, which for a library function renders it quite useless. Anyway, I think the API that I landed on is a decent one, for this reason alone, almost.

[1] The c-lightning plugin to c-lightning relationship is a bit complicated. A plugin is both a 'server', in JSON-RPC parlance, and a client. For most of the commands and the like, a plugin plays the role of a server, providing methods that c-lightning can call out to. Notifications from c-lightning to your plugin take advantage of the client -> server notification framework that's included in the JSON-RPC spce. The one exception, so far at least, is that you can pass back logs from the plugin to c-lightning, such that plugin logs will appear in the `getlogs` command on c-lightning. In order to do this, your plugin sends a log notification to the c-lightning parent, which inverts the server -> client relationship.


#### Resources
I cobbled together info on how the more magique aspects of reflection works from a variety of places. Here's some of the ones that I found the most helpful.

How to create an object with Reflection via [reddit](https://www.reddit.com/r/golang/comments/38u4j4/how_to_create_an_object_with_reflection/)  
Writing into a slice via [blog](http://intogooglego.blogspot.com/2015/06/day-17-using-reflection-to-write-into.html)  
The exhaustive list of reflection tests in the golang source [golang.org](https://golang.org/src/reflect/all_test.go)  
And of course the seminal "The Laws of Reflection" [Go Blog](https://blog.golang.org/laws-of-reflection)  
