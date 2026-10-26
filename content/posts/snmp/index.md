---
title: "SNMP"
date: "2023-07-11T12:00:00Z"
slug: "snmp"
description: "SNMP (Simple Network Management Protocol) is a widely used protocol for managing and monitoring network devices, such as routers, switches, servers, and printers."
categories: ["technical"]
aliases: ["/wps/2023/07/11/snmp/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

![](snmp.drawio.png)

SNMP (Simple Network Management Protocol) is a widely used protocol for managing and monitoring network devices, such as routers, switches, servers, and printers. It allows network administrators to gather information about network devices, monitor their performance, and manage their configuration remotely.

SNMP operates on the client-server model, where network devices act as SNMP agents and a centralized management system (SNMP manager) collects and analyzes data from these agents. The SNMP manager communicates with SNMP agents using SNMP messages, which are exchanged over UDP/IP.

SNMP uses a hierarchical structure called the Management Information Base (MIB) to organize and represent the managed objects in the network devices. The MIB contains a collection of variables (known as SNMP objects) that provide information about the device’s status, performance, and configuration.

An SNMP profile, also referred to as an SNMP community or SNMP string, is a configuration setting that controls access to SNMP-enabled devices. It acts as a password or authentication mechanism to allow or restrict access to the SNMP functionality of a device.

There are two types of SNMP profiles:

1. Read-only (RO) profile: A read-only profile allows SNMP managers to retrieve information from the SNMP agent but does not permit modifications to the device’s configuration. It is typically used for monitoring purposes.
2. Read-write (RW) profile: A read-write profile allows SNMP managers not only to retrieve information but also to modify the configuration of the SNMP agent. It provides full control and management capabilities over the device.

SNMP profiles are usually configured on the SNMP agent side and need to be properly set up and secured to prevent unauthorized access. The SNMP manager needs to use the correct SNMP profile credentials (community string) to establish communication with the SNMP agent and retrieve or modify the desired information.

It’s important to note that SNMP versions 1 and 2c use a community string as the authentication mechanism, while SNMP version 3 offers more secure authentication options such as username and password, providing improved security for SNMP communication.

Authentication helps verify the identity of the communicating parties and protects against unauthorized access or tampering of SNMP data. There are two common authentication methods used in SNMP:

1. SNMPv1 and SNMPv2c Community-Based Authentication:

- SNMPv1 and SNMPv2c use a community string as the authentication mechanism.
- The community string acts as a password or shared secret between the SNMP manager and SNMP agent.
- The SNMP manager includes the community string in SNMP messages to authenticate and authorize access to SNMP-enabled devices.
- It is crucial to protect the community string and ensure it is not easily guessable or exposed to unauthorized individuals.

1. SNMPv3 User-Based Authentication (USM):

- SNMPv3 introduces a more secure authentication mechanism known as User-Based Authentication (USM).
- USM supports multiple authentication protocols, including MD5 and SHA (Secure Hash Algorithm).
- SNMPv3 requires the SNMP manager and SNMP agent to have pre-configured user accounts with associated usernames and passwords.
- The SNMP messages exchanged between the SNMP manager and agent are encrypted using the authentication protocol, ensuring confidentiality and integrity of the data.

### Device discovery

`Device discovery`, also known as network discovery, is the process of identifying and gathering information about SNMP-enabled devices within a network. SNMP discovery involves finding and mapping network devices, discovering their SNMP capabilities, and populating the Management Information Base (MIB) with relevant data for monitoring and management purposes. The device discovery process typically includes the following steps:

1. Determining the IP Range: Define the range of IP addresses to scan for SNMP-enabled devices.
2. SNMP Community String: Provide the correct community string or authentication credentials to access SNMP-enabled devices. This may involve using default community strings or customized strings for specific devices.
3. Scanning the Network: Use SNMP discovery tools or network management systems to scan the defined IP range and send SNMP queries to each device.
4. SNMP Responses: Capture the SNMP responses from the devices, which include information such as system name, system description, IP address, SNMP version, and supported MIBs.
5. Building Device Inventory: Create an inventory of discovered devices, including their SNMP capabilities, and store the information in a centralized management system.
6. Populating the MIB: Retrieve specific information from the devices’ MIBs and populate the management system’s MIB for monitoring and management purposes.

Device discovery plays a vital role in network management, allowing administrators to identify and monitor network devices, track their configurations, and ensure proper maintenance and troubleshooting. It enables centralized management and control over network resources, leading to more efficient network operations.
