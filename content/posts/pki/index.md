---
title: "PKI"
date: "2022-11-18T12:00:00Z"
slug: "pki"
description: "PKI is the core of security for most organizations, and at its heart is a couple of keys that together allows the encryption/decryption of the traffic exchanged."
categories: ["learn", "technical"]
tags: ["pki", "security"]
aliases: ["/wps/2022/11/18/pki/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

PKI is the core of security for most organizations, and at its heart is a couple of keys that together allows the encryption/decryption of the traffic exchanged.

- Public key to encrypt a message.
- Private key to decrypt a message.

{{< lead >}}
Keys can be used by devices, people or applications
{{< /lead >}}

The challenge of any symmetric or asymmetric encryption is the MIM (man in the middle) attack. How does one validate the keys is really from the genuine entity or someone who has hijacked the conduit.

PKI addresses this challenge by assigning digital certificates – X509 certificates; that establishes the identity (verifiable) of the entity that owns the keys.

{{< lead >}}
X.509 is a standard format for public key certificates. Each X.509 certificate includes a public key, digital signature and information about the identity associated with the certificate and its issuing CA.
— https://www.ssl.com/faqs/what-is-an-x-509-certificate/
{{< /lead >}}

### Certificate Type

- Wildcard
- SAN – Subject Alternative Name
- Code-Signing
- Self-Signed
- Root

### CA : Certification Authority

An organization that issues the certificates. A certificate issued by a CA can be used to issue and sign another certificates and this allows hierarchies of intermediate CA’s

### Version of X.509

- X.509v1
- X.509v2
- X.509v3 Supports extension

#### Formats of certificate

- DER (Distinguished encoding rules)/(CER Canonical encoding rules) – Binary format
- PEM (Privacy enhanced Electronic Mail) – ASCII file format, that has the BEGIN CERTIFICATE and END CERTIFICATE tags
- PFX (Personal Information Exchange)/P12 (PKCS#12) – Binary format
- P7B – ASCII file format with tags BEGIN PKCS7 and END PKCS7

### CRL Certificate revocation list

A valid certificate that has been compromised and not to be trusted is maintained in a CRL. The owner might have more than one certificates valid, but the list determines which one is to be trusted.

### How SSL works?

Simples steps elaborating the process

1. The client sends a HTTPS request for a web page to the secure web site.
2. The server returns its public key to the client.
3. The client validates the certificate.
4. The client then creates a random symmetric key (known as a session key) used to encrypt the web page content, and then encrypts the symmetric key with the public key obtained from the web server.
5. The encrypted information is sent to the web server.
6. The web server decrypts and obtains the symmetric key.
7. The web server uses the key to encrypt information between the client and the server.
