---
title: "Securing Kafka Brokers: A Practical Operations Checklist"
date: "2025-06-14"
description: "Broker-level controls for a safer Kafka deployment, from service accounts and filesystems to monitoring and recovery."
categories: ["technical"]
tags: ["kafka", "security", "linux"]
series: ["Back to basics"]
draft: false
---

I used to think of Kafka security as a client configuration problem. Then I started thinking about the broker host itself: which user owns the process, who can read the configuration, what is exposed on the network, and what happens during an incident.

Client authentication is only one part of Kafka security. The brokers themselves need a secure operating environment and a predictable maintenance process.

{{< alert "circle-info" >}}
Written up in October 2026 from my notes at the time. The file permissions and monitoring values below are illustrative examples, not evidence from a current broker.
{{< /alert >}}

## Run with a dedicated identity

Run Kafka as a dedicated service user with no interactive login. Keep data directories, configuration files, logs, and certificates separated by purpose. The service user should not own files it only needs to read, and private key files should be more restrictive than general configuration.

Example permissions should be treated as a starting point, not copied blindly:

```text
/etc/kafka/server.properties       root:kafka  0640
/etc/kafka/secrets/                 root:kafka  0750
/var/lib/kafka/                     kafka:kafka 0750
```

## Protect listeners

Expose only the listeners required by the architecture. A listener intended for internal broker traffic should not be reachable from an untrusted network. Use firewall rules, security groups, and network policy as layers rather than relying on Kafka authorization alone.

Separate advertised addresses from bind addresses carefully. A broker can be listening on the correct interface while advertising an address that clients cannot reach.

## Treat configuration as sensitive

Broker configuration can contain usernames, paths, TLS references, and sometimes secrets depending on the authentication mechanism. Store the source configuration in a protected system and render it with least-privilege permissions.

When using Ansible, template configuration from variables but keep secret values in Vault or an external secret store. Never print the rendered file in CI logs.

## Patch and monitor

Keep a tested upgrade path for the Kafka version, Java runtime, operating system, and security libraries. Monitor:

- under-replicated partitions;
- offline partitions;
- failed authentication;
- authorization denials;
- disk usage and inode usage;
- certificate expiry;
- controller or metadata quorum health.

Alerts should include enough context to act without exposing credentials or message contents.

## Backups are part of security

Retention is not a backup. Define what must be recovered, how long recovery may take, and where cluster metadata and application configuration are stored. Test restoration in a separate environment. A backup that has never been restored is an assumption.

## Incident readiness

Prepare procedures for revoking a client, rotating broker certificates, isolating a compromised broker, and preserving logs. Use separate administrative identities so that one leaked application credential does not become a cluster-wide credential.

Broker security is mostly disciplined operations: narrow access, protected files, timely patches, useful telemetry, and rehearsed recovery. The checklist matters because distributed systems make small configuration mistakes visible at scale.

Illustrative permission check:

```text
-rw-r----- 1 root kafka 18432 server.properties
drwxr-x--- 3 kafka kafka  4096 /var/lib/kafka
```
