---
title: "Handshake"
date: "2023-02-22T12:00:00Z"
slug: "handshake"
description: "The SSL/TLS handshake is the initial communication between the client and server in a SSL/TLS connection."
categories: ["technical"]
tags: ["handshake", "security", "ssl"]
aliases: ["/wps/2023/02/22/handshake/"]
recovered: "Internet Archive snapshot 2026-05-17"
---

*[image unavailable: ssl-handshake.png]*

The SSL/TLS handshake is the initial communication between the client and server in a SSL/TLS connection. The purpose of the handshake is to establish a secure connection between the client and server and to negotiate the cryptographic parameters for the session.

The SSL/TLS handshake follows a set of steps:

1. Client Hello: The client initiates the SSL/TLS handshake by sending a Client Hello message to the server. The Client Hello message contains the client’s SSL/TLS version, a list of supported cryptographic algorithms, and a random number called the Client Random.
2. Server Hello: The server responds to the client’s message by sending a Server Hello message. The Server Hello message contains the server’s SSL/TLS version, the cryptographic algorithm that will be used for the session, and a random number called the Server Random.
3. Certificate: The server sends its SSL/TLS certificate to the client. The certificate contains the server’s public key and other information such as the certificate issuer, expiration date, and the signature of the certificate authority.
4. Client Key Exchange: The client and server exchange a set of encryption keys that will be used to encrypt and decrypt the data being transmitted. The client sends its public key to the server, which is used to encrypt the session key. The client also sends a premaster secret, which is a random value encrypted with the server’s public key.
5. Server Key Exchange: In some cases, the server may also send a Server Key Exchange message to the client. This message is used to send additional information required for the session, such as Diffie-Hellman parameters.
6. Certificate Request: The server may also send a Certificate Request message to the client, requesting that the client send its SSL/TLS certificate for authentication purposes.
7. Certificate Verify: If the server requested the client’s SSL/TLS certificate, the client sends a Certificate message containing the certificate. The client may also send a Certificate Verify message to prove that it has the private key that corresponds to the public key in the certificate.
8. Finished: The client and server exchange Finished messages to confirm that the SSL/TLS handshake was successful. The Finished message contains a hash of all the messages that were exchanged during the handshake, which ensures that the handshake was not tampered with.

Once the SSL/TLS handshake is complete, the client and server can begin to exchange encrypted data using the negotiated cryptographic parameters. The SSL/TLS handshake is a critical part of establishing a secure connection and ensuring the confidentiality, integrity, and authenticity of the data being transmitted.
