---
title: "SSH Protocol"
date: "2022-02-25T12:00:00Z"
slug: "ssh-protocol"
categories: ["technical"]
tags: ["learn", "ssh"]
aliases: ["/wps/2022/02/25/ssh-protocol/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

> 💬 What is SSH protocol?

> 💬 It is also referred to as Secure Shell, is a method for secure remote login from one computer to another. It is an alternative to `telnet` and `rlogin`

> 💬 It protects the communications security and integrity with strong encryption.

> 💬 How does it work?

> 💬 – It works in client server model.
> 
> – The SSH client drives the connection setup and uses `public key cryptography` to verify the identity of the SSH server.
> 
> – Once a connection is established data that is transmitted is encrypted according to the parameters negotiated in the setup.

> 💬 After the setup phase is done, SSH protocol uses **strong symmetric encryption** and **hashing algorithms** to ensure the privacy and integrity of the data that is exchanged.
> 
> RFC – [Link](https://assets.ctfassets.net/0lvk5dbamxpi/7wNRdbPyeUDql7sZjv3ZTp/ef86cf604b532728ee8da263d27883d8/RFC_4251_-_The_Secure_Shell__SSH__Protocol_Architecture)

![From SSH.com](https://www.ssh.com/hs-fs/hubfs/SSH_Client_Server.png?width=1112&name=SSH_Client_Server.png "From SSH.com")

> 💬 What are the options to initiate SSH?

> 💬 Amongst the several methods available the most common ones are `passwords` and `public key authentication`.

> 💬 In most of automation cases the public key authentication method is preferred. (ANSIBLE uses it)

> 💬 Is it driven via a cryptographic key pair – public key and private key?

> 💬 Duh?
> 
> The keys used for authentication are called SSH keys.
> 
> Configure the public key on a server to authorize access and grant anyone who has a copy of the private key access to the server.

> 💬 But WHY Public key?

> 💬 – Why not – It is passwordless login, and yet more secure?
> 
> – The motivation for using public key authentication over simple passwords is security.
> 
> – Public key authentication provides cryptographic strength that even extremely long passwords can not offer
