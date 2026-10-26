---
title: "DAST"
date: "2023-06-07T12:00:00Z"
slug: "dast"
description: "DAST stands for Dynamic Application Security Testing. It is a type of security testing that assesses the security of an application while it is running."
categories: ["technical"]
tags: ["dast", "security"]
aliases: ["/wps/2023/06/07/dast/"]
recovered: "Internet Archive snapshot 2026-04-21"
---

![](dast.drawio.png)

DAST

DAST stands for Dynamic Application Security Testing. It is a type of security testing that assesses the security of an application while it is running. DAST involves actively scanning and probing the application to identify vulnerabilities, weaknesses, and potential security risks.

Unlike Static Application Security Testing (SAST), which analyzes the source code of an application, DAST evaluates the application in its deployed state. It simulates real-world attacks and interactions with the application, examining how it responds and identifying any security flaws that can be exploited.

DAST tools work by sending various types of requests to the target application, including inputs that attempt to exploit common security vulnerabilities such as cross-site scripting (XSS), SQL injection, and insecure access controls. The tool then analyzes the responses and behavior of the application to identify any potential security issues.

The benefits of DAST include:

1. Real-world simulation: DAST mimics the behavior of attackers by interacting with the application in a running state, providing a more realistic assessment of its security posture.
2. Comprehensive coverage: DAST examines the entire application, including all the components, modules, and interactions, ensuring a thorough evaluation.
3. Quick feedback: DAST can provide immediate feedback on the security of the application, allowing developers to address vulnerabilities promptly.
4. Detection of runtime vulnerabilities: DAST can identify vulnerabilities that may only be present during runtime, such as configuration issues, session management problems, and server misconfigurations.
5. Compliance requirements: DAST can help organizations meet compliance requirements by validating the security of their applications and ensuring they adhere to industry standards and best practices.

It’s important to note that while DAST is a valuable security testing approach, it should not be the sole method for ensuring application security. It is recommended to combine DAST with other security testing techniques such as SAST (Static Application Security Testing), manual code reviews, vulnerability scanning, and penetration testing to establish a comprehensive security testing strategy.
