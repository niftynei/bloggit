timestamp: 1752378161
date: 12 Jul 2025
time: 22:46
title: NixOS My Savior
tags: nixos, deploying, devops, nix

---

## Ode to NixOS

We really do live in an age of modern marvels, NixOS being no exception. I love using NixOS so much, it's probably one of my favorite tools at the moment.

Not that I've been doing a lot of coding, but the ease of use and how good it is at making deploying software very simple makes me happy to launch projects.

I recently updated some code that I've got on a box that I last updated in 2023. It's a little custom golang service worker that I use for sending emails for btc++ and Base58. The websites generate the emails then send it to my service worker who makes sure the emails make it out to their intended recipients. I have this in place mainly so that sending emails from the webapps is "idempotent". I can have the webapp 'resend' the same email a hundred times, but the recipient will only get it once.

I like this setup because it makes working on the main website much less stressful. In order to spam past attendees, I'd need to mess up from the service worker level. 

The btc++ app, every time I restart it, attempts to resend everyone a new copy of their tickets. This is great because if the webapp goes down at some point during sending out a ticket email, it'll get sent the next time the app starts up.

I very rarely touch the email middleware picee. I call him "mailer" (you can check out the code for it [here](https://github.com/base58btc/mailer).). The last time I updated the code for it was in 2023, around the same time that I wrote the previous blog post.

The webapp for btc++ lives on a $5 a month Digital Ocean box. I use their auto-deploy app pipeline, it's really nice, and really incredibly affordable. I'm not a web server developer by trade though. I know enough to get a box up and running, and how to use other people's deploy pipelines, but setting up a database and maintaining it in the cloud is not something I'm really good at. Instead of trying to pay for cloud storage for data, I decided I'd rather run the box at home with a simple SQLite flat file on the server that I can (in theory?) run backups for.

I should really learn how to do system backups.

The server that lives at home is a NixOS box. I was pretty new to NixOS (especially in 2023), but it seemed to me that in order to be able to deploy new software onto my server, I'd probably want to write a Nix module to build the code, and then write a systemd startup script for it.

It was definitely more overhead to figure out how to write my very first module for a golang app, and then wire it into my `configuration.nix`. One of the biggest issues I ran into was that the module definition was written in a `flake.nix` but I wanted to be able to reference it from the `configuration.nix`. I'm not really sure if there's a good way to do this. It's entirely possible that what I hacked together is unnecessary. It took me a while to figure out all the pieces, but eventually I got it all deployed and working.

It's been running largely without problems since I shipped it two years ago.

Recently, I decided to add some better newsletter capabilities to Base58's infrastructure, which meant I needed to make some changes to the `mailer`. I want to be able to keep track of emails that are scheduled to send to a user and which letter each send job belongs to.

Basically this meant adding two new fields to the database and some new API calls to allow a user to unsubscribe (we'll delete all scheduled but unsent emails that are destined for a particular email on a newsletter) or to unschedule an entire pending newsletter missive.

Coding it up was really straightforward (golang, you're alright), but I got pretty nervous about deploying it onto my Nixbox. I haven't touched the nixbox in ages, and I've been having weird issues with deploying the core-lightning node I run on it.

Turns out upgrading and redeploying a single module is incredibly easy and it worked on the first try with zero problems. The biggest issue I had was with trying to update the nixpkgs/nixOS dependencies to a later version, which ran into [a bug](https://discourse.nixos.org/t/updating-linux-kernel-results-in-modules-shrunk-not-in-nix-store/62343).

I pushed the newest code of the `mailer` up to Github, and then ran these two commands

    nix flake lock --update-input b58-mailer
    sudo nixos-rebuild switch

And that was it. The code got pulled from github, rebuilt locally, tests were run, and then it deployed. Magic.

I managed to fix the upgrade issues with nixpkgs by doing a mid-way update to a nixpkgs past the bug and then finishing the update. It took me longer than I would have liked given the upgrade bug, but I'm so happy with how easy and seamless it was to upgrade my box.


## Pieces of a Module

It's been a few years since I wrote the original module code for the mailer. Looking back through the logs though, it looks like there's two pieces to it.

One is a [`default.nix`](https://github.com/base58btc/mailer/blob/master/default.nix) which provides the build instructions for the project. I'm using`gomod2nix` to handle the majority of how to fetch golang dependencies and build a Go application. I'm going to be honest, I don't really understand what it's doing, but it works great and I haven't had any issues with it so we're going to leave it at that. Digging into Nix packege build tools is on my todo list.


    { pkgs ? (
        let
          inherit (builtins) fetchTree fromJSON readFile;
          inherit ((fromJSON (readFile ./flake.lock)).nodes) nixpkgs gomod2nix;
        in
        import (fetchTree nixpkgs.locked) {
          overlays = [
            (import "${fetchTree gomod2nix.locked}/overlay.nix")
          ];
        }
      )
    }:

    pkgs.buildGoApplication {
      pname = "mailer";
      version = "0.1";
      pwd = ./.;
      src = ./.;
      modules = ./gomod2nix.toml;
    }

So now that we've got the definition (or derivation as nix calls them) for how to build a piece of software, the next thing to write is a Module definition. The module I wrote for `mailer` consists of two portions: a list of config settings and a systemd service defintion. The config settings give someone setting up the `mailer` in their NixOS `configuration.nix` handles with which to adjust the settings of the software. The service definition wires the app into the services architecture of linux, as well as giving you an opportunity to wire the configs the user set in the module into the startup of the server application. Here's the `mailer`'s current `module.nix`.


    { pkgs, config, lib, ... }:

    with lib;

      let
        cfg = config.services.b58-mailer;
      in
      {
        options.services.b58-mailer = {

          enable = mkEnableOption "Base58 mailer service"; 

          mailerBin = mkOption {
            type = types.str;
            description = mdDoc "The package providing the b58-mailer binaries";
          };

          user = mkOption {
            type = types.str;
            default = "nobody";
            description = mdDoc "The user to run the b58-mailer binaries";
          };

          port = mkOption {
            type = types.port;
            default = 9090; 
            description = mdDoc "Port to start mailer on";
          };

          secretsFile = mkOption {
            type = with types; nullOr path;
            description = mdDoc "Name of file to load secrets from";
            default = "config.toml";
          };

          mailSendFrequency = mkOption {
            type = types.int;
            description = mdDoc "Frequency to check mailbox for new messages to send";
            default = 10;
          };

          dbFile = mkOption {
            type = types.str;
            description = mdDoc "Name of sqlite3 file to load";
            default = "mailer.sqlite";
          };

          mailerDomains = mkOption {
            type = types.str;
            description = mdDoc "Domain options for to sending mail requests from";
          };
        };

        config = mkIf cfg.enable {
          systemd.services.b58-mailer = {
            description = "Base58 mailer service";
            after = [ "network.target" ];
            wants = [ "network.target" ];
            wantedBy = [ "multi-user.target" ];
            script = "PORT=${toString cfg.port} SECRETS_FILE=${toString cfg.secretsFile} MAIL_SEND_TIMER=${toString cfg.mailSendFrequency} DB_NAME=${toString cfg.dbFile} MAIL_DOMAINS=${toString cfg.mailerDomains} ${cfg.mailerBin}";

            serviceConfig = {
              Type = "simple";
              User = "${cfg.user}";
            };
          };
        };	
      }

And that's more or less it. I love that Nix lets you package up the instructions for how to configure a piece of software, along with the instructions for deploying it, all in the same repo as the software. Huge win imo in terms of documentation and repeatability. These two files made it such that I was able to write new code and update it on the running box with very very little hassle.

## In Exitus

There's still a ton for me to learn about the nix language as well as build cycles, and derivation semantics in NixOS. But, just with the understanding I have so far about how all the pieces work together, I'm very impressed with how well I've been able to leverage a NixOS system for deploying software on my own hardware at home. 

(I also use it for managing one of a few cloud boxes, but hoping to turn all of my server boxes into NixOS boxes at some point).

If you haven't tried it out yet, really would suggest finding an opportunity to run NixOS on a server or spare computer you have at home; or on a rented server box. It's just such a joy to use.

