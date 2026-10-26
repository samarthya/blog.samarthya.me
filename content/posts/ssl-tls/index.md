---
title: "SSL/TLS"
date: "2023-02-22T12:00:00Z"
slug: "ssl-tls"
description: "Secure Socket Layer and its successor TLS (Transport Layer Security) are cryptographic protocols that provide encryption, integrity, and authentication for network communication."
categories: ["technical"]
tags: ["handshake", "security", "ssl", "tls"]
aliases: ["/wps/2023/02/22/ssl-tls/"]
recovered: "Internet Archive snapshot 2026-06-10"
---

*[image unavailable: ssl-tls.png]*

Secure Socket Layer and its successor TLS (Transport Layer Security) are cryptographic protocols that provide encryption, integrity, and authentication for network communication. They are commonly used to secure online transactions, such as those made in online banking, e-commerce, and other sensitive online transactions.

When SSL/TLS encryption is used, the data being transmitted is encrypted using a **combination of a symmetric encryption algorithm and a public-key cryptography algorithm**. The symmetric encryption algorithm is used to encrypt the data, while the public-key cryptography algorithm is used to securely exchange a key that is used for the symmetric encryption.

Here are the steps involved in SSL/TLS encryption:

1. [Handshake`Handshake`]({{< relref "/posts/handshake" >}}): The SSL/TLS handshake is the initial communication between the client and server. During this phase, the server and client exchange information to establish a secure connection. This includes agreeing on the cryptographic protocol, exchanging public keys, and verifying digital certificates.
2. `Authentication`: Once the client and server have exchanged information, they authenticate each other. The server authenticates the client by requesting a digital certificate, which the client presents. The server verifies the digital certificate to ensure the client is who it claims to be. The client also verifies the server’s digital certificate to ensure that it is communicating with the correct server.
3. `Key exchange`: After authentication, the client and server exchange keys that will be used for symmetric encryption. The server sends a public key to the client, which the client uses to encrypt a random number that is used to generate a symmetric key. The symmetric key is then used to encrypt the data being transmitted between the client and server.
4. `Encryption`: Once the symmetric key has been established, the data being transmitted is encrypted using the symmetric encryption algorithm. This ensures that the data is protected from eavesdropping and data tampering.
5. `Integrity`: To ensure that the data has not been tampered with during transmission, SSL/TLS uses a message authentication code (MAC) to verify the integrity of the data. This ensures that the data has not been altered or corrupted in transit.

By using SSL/TLS encryption, organizations can ensure the confidentiality, integrity, and authenticity of their data, and safeguard against potential security breaches.
