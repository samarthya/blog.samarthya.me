---
title: "XEE: XML Entity Attack (XXE)"
date: "2023-05-24T12:00:00Z"
slug: "xee-xml-entity-attack-xxe"
description: "XML entity attack, also known as Billion Laughs Attack, is a type of security vulnerability that exploits the way XML parsers handle entity expansion."
categories: ["technical"]
tags: ["owasp", "security", "xee", "xxe"]
aliases: ["/wps/2023/05/24/xee-xml-entity-attack-xxe/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

XML entity attack, also known as Billion Laughs Attack, is a type of security vulnerability that exploits the way XML parsers handle entity expansion. It can lead to denial-of-service (DoS) attacks by overwhelming the system’s resources with excessive entity expansions.

## History

The XML entity attack was first discovered and demonstrated in 2002 by David Kuhn, a researcher at `Argonne National Laboratory`. The attack was named “Billion Laughs Attack” due to the humorous nature of the XML payload used. The attack gained significant attention in the security community and exposed a vulnerability in XML parsers that had widespread implications.

## Citations

1. Kuhn, D. R. (2002). XML Denial of Service Attacks and Defenses. Proceedings of the 2002 IEEE Symposium on Security and Privacy, 2-15. DOI: 10.1109/SECPRI.2002.1004378

In his paper, Kuhn presented the concept of the XML entity attack and its potential impact on systems relying on XML parsing. He discussed the use of nested entity references to create an exponentially expanding XML document that overwhelms the parser, leading to resource exhaustion and potential system failure.

The XML entity attack highlights the importance of secure XML parsing and the need for proper input validation and handling to mitigate such vulnerabilities.

## OWASP definition

An XML External Entity attack is a type of attack against an application that parses XML input. This attack occurs when XML input containing a reference to an external entity is processed by a weakly configured XML parser. This attack may lead to the disclosure of confidential data, denial of service, server side request forgery, port scanning from the perspective of the machine where the parser is located, and other system impacts.

The `XML 1.0` standard defines the structure of an `XML` document. The standard defines a concept called an `entity`, which is a `storage unit` of some type. There are a few different types of `entities`, `external` `general/parameter` parsed entity often shortened to external entity, that can access local or remote content via a declared system identifier.

The system identifier is assumed to be a URI that can be dereferenced (accessed) by the XML processor when processing the entity. The XML processor then replaces occurrences of the named external entity with the contents `dereferenced` by the system identifier. If the system identifier contains tainted data and the XML processor dereferences this tainted data, the XML processor may disclose confidential information normally not accessible by the application. Similar attack vectors apply the usage of external DTDs, external stylesheets, external schemas, etc. which, when included, allow similar external resource inclusion style attacks.  
Attacks can include disclosing local files, which may contain sensitive data such as passwords or private user data, using file: schemes or relative paths in the system identifier. Since the attack occurs relative to the application processing the XML document, an attacker may use this trusted application to pivot to other internal systems, possibly disclosing other internal content via http(s) requests or launching a CSRF attack to any unprotected internal services. In some situations, an XML processor library that is vulnerable to client-side memory corruption issues may be exploited by dereferencing a malicious URI, possibly allowing arbitrary code execution under the application account. Other attacks can access local resources that may not stop returning data, possibly impacting application availability if too many threads or processes are not released.

## Read

- <https://portswigger.net/web-security/xxe/xml-entities>
