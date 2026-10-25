---
title: "Linux Utils"
date: "2020-10-13T08:29:43Z"
slug: "linux-utils"
categories: ["technical"]
tags: ["linux", "utils"]
aliases: ["/wps/2020/10/13/linux-utils/"]
wp_id: 1083
---

# Ping

I have used `ping` often but never to an extend that I could understand the complete range of options and power available at hand.

{{< lead >}}
ping - send ICMP ECHO\_REQUEST to network hosts
— from - man page of ping
{{< /lead >}}

## ICMP Packet details

An IP header without options is 20 bytes. An ICMP ECHO\_REQUEST packet contains an additional 8 bytes worth of ICMP header followed by an arbitrary amount of data.

## Examples

```text
ping hostname #www.samarthya.me
```

```text
ping www.samarthya.me
PING samarthya.me (148.72.168.185) 56(84) bytes of data.
64 bytes from server4.hostsoch.in (148.72.168.185): icmp_seq=1 ttl=53 time=251 ms
64 bytes from server4.hostsoch.in (148.72.168.185): icmp_seq=8 ttl=53 time=252 ms
^C
--- samarthya.me ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 2007ms
rtt min/avg/max/mdev = 250.972/251.358/252.325/0.657 ms
```

```text
ping ip #148.32.168.185
```

```text
ping 148.72.168.185
PING 148.72.168.185 (148.72.168.185) 56(84) bytes of data.
64 bytes from 148.72.168.185: icmp_seq=1 ttl=53 time=251 ms
64 bytes from 148.72.168.185: icmp_seq=2 ttl=53 time=251 ms
64 bytes from 148.72.168.185: icmp_seq=3 ttl=53 time=251 ms
^C
--- 148.72.168.185 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 251.039/251.231/251.438/0.601 ms
```

Options available that I can use are

{{< lead >}}
ping [-aAbBdDfhLnOqrRUvV46] [-c count] [-F flowlabel] [-i interval] [-I interface] [-l preload] [-m mark] [-M pmtudisc\_option] [-N nodeinfo\_option] [-w deadline] [-W timeout] [-p pattern] [-Q tos] [-s packetsize] [-S

sndbuf] [-t ttl] [-T timestamp option] [hop …] destination
{{< /lead >}}

## -c [COUNT]

{{< lead >}}
Stop after sending count ECHO\_REQUEST packets. With deadline option, ping waits for count ECHO\_REPLY packets, until the timeout expires.
— from official man pages
{{< /lead >}}

```text
ping -c 10 10.0.1.11
PING 10.0.1.11 (10.0.1.11) 56(84) bytes of data.
64 bytes from 10.0.1.11: icmp_seq=1 ttl=64 time=0.609 ms
64 bytes from 10.0.1.11: icmp_seq=2 ttl=64 time=0.624 ms
64 bytes from 10.0.1.11: icmp_seq=3 ttl=64 time=0.586 ms
64 bytes from 10.0.1.11: icmp_seq=4 ttl=64 time=0.603 ms
64 bytes from 10.0.1.11: icmp_seq=5 ttl=64 time=0.624 ms
64 bytes from 10.0.1.11: icmp_seq=6 ttl=64 time=0.602 ms
64 bytes from 10.0.1.11: icmp_seq=7 ttl=64 time=0.688 ms
64 bytes from 10.0.1.11: icmp_seq=8 ttl=64 time=0.620 ms
64 bytes from 10.0.1.11: icmp_seq=9 ttl=64 time=0.663 ms
64 bytes from 10.0.1.11: icmp_seq=10 ttl=64 time=0.604 ms

--- 10.0.1.11 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9000ms
rtt min/avg/max/mdev = 0.586/0.622/0.688/0.035 ms
```

## -s [Packet Size]

{{< lead >}}
Specifies the number of data bytes to be sent. The default is 56, which translates into 64 ICMP data bytes when combined with the 8 bytes of ICMP header data.
— from official man pages
{{< /lead >}}

```text
ping -s 64 -c 2 10.0.1.11
PING 10.0.1.11 (10.0.1.11) 64(92) bytes of data.
72 bytes from 10.0.1.11: icmp_seq=1 ttl=64 time=0.665 ms
72 bytes from 10.0.1.11: icmp_seq=2 ttl=64 time=0.612 ms

--- 10.0.1.11 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1000ms
rtt min/avg/max/mdev = 0.612/0.638/0.665/0.036 ms
```

# DIG

dig is a flexible tool for interrogating DNS name servers. It performs DNS lookups and displays the answers that are returned from the name server(s) that were queried.

```text
dig www.samarthya.me

; <<>> DiG 9.11.4-P2-RedHat-9.11.4-16.P2.el7_8.6 <<>> www.samarthya.me
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 48626
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1220
;; QUESTION SECTION:
;www.samarthya.me.              IN      A

;; ANSWER SECTION:
www.samarthya.me.       13357   IN      CNAME   samarthya.me.
samarthya.me.           13357   IN      A       148.72.168.185

;; Query time: 221 msec
;; SERVER: 192.19.189.10#53(192.19.189.10)
;; WHEN: Tue Oct 13 08:05:36 UTC 2020
;; MSG SIZE  rcvd: 75
```

## ss

Utility to investigate sockets (Socket Statistics), similar to `netstat`

```text
ss -e --extended
```

Shows detailed information

```text
ss -e
Netid State      Recv-Q Send-Q                                                                 Local Address:Port                                                                                  Peer Address:Port                
u_str ESTAB      0      0                                                        /run/dbus/system_bus_socket 14506                                                                                            * 14457                 <->
u_str ESTAB      0      0                                                                                  * 13157                                                                                            * 13158                 <->
u_str ESTAB      0      0                                                                                  * 17900                                                                                            * 17901                 <->
u_str ESTAB      0      0                                                                                  * 17937                                                                                            * 17936                 <->
u_str ESTAB      0      0                                                                                  * 17909                                                                                            * 17910                 <->
u_str ESTAB      0      0                                                                                  * 17888                                                                                            * 17887                 <->
u_str ESTAB      0      0                                                                                  * 17922                                                                                            * 17921
```

```text
ss -l # All listening ports
```

```text
ss -l
Netid State      Recv-Q Send-Q                                                                 Local Address:Port                                                                                  Peer Address:Port                
nl    UNCONN     0      0                                                                               rtnl:kernel                                                                                            *                     
nl    UNCONN     768    0                                                                            tcpdiag:kernel                                                                                            *                     
nl    UNCONN     4352   0                                                                            tcpdiag:ss/11768                                                                                          *                     
nl    UNCONN     0      0                                                                               xfrm:kernel                                                                                            *                     
nl    UNCONN     0      0                                                                            selinux:systemd/1                                                                                         *                     
nl    UNCONN     0      0                                                                            selinux:dbus-daemon/492                                                                                   *                     
nl    UNCONN     0      0                                                                            selinux:kernel                                                                                            *                     
nl    UNCONN     0      0                                                                            selinux:dbus-daemon/492                                                                                   *                     
nl    UNCONN     0      0                                                                            selinux:systemd/1                                                                                         *                     
nl    UNCONN     0      0                                                                              audit:systemd/1                                                                                         *                     
nl    UNCONN     0      0                                                                              audit:auditd/422                                                                                        *                     
nl    UNCONN     0      0                                                                              audit:kernel                                                                                            *                     
nl    UNCONN     0      0                                                                          fiblookup:kernel                                                                                            *                     
nl    UNCONN     0      0                                                                          connector:kernel                                                                                            *                     
nl    UNCONN     0      0                                                                                nft:kernel                                                                                            *                     
nl    UNCONN     0      0                                                                             uevent:kernel                                                                                            *                     
nl    UNCONN     0      0                                                                             uevent:systemd-udevd/393                                                                                 *                     
nl    UNCONN     0      0                                                                             uevent:systemd/1                                                                                         *                     
nl    UNCONN     0      0                                                                             uevent:-4117                                                                                             *                     
nl    UNCONN     0      0                                                                             uevent:tuned/907                                                                                         *                     
nl    UNCONN     0      0                                                                             uevent:-4107                                                                                             *
```

```text
ss -s #summary
```

```text
ss -s
Total: 226 (kernel 0)
TCP:   8 (estab 2, closed 1, orphaned 0, synrecv 0, timewait 0/0), ports 0

Transport Total     IP        IPv6
*         0         -         -        
RAW       0         0         0        
UDP       3         2         1        
TCP       7         4         3        
INET      10        6         4        
FRAG      0         0         0
```

```text
ss -ta #all tcp ports
```

```text
ss -t -a
State       Recv-Q Send-Q                                                                   Local Address:Port                                                                                    Peer Address:Port                
LISTEN      0      128                                                                          127.0.0.1:10248                                                                                              *:*                    
LISTEN      0      128                                                                                  *:sunrpc                                                                                             *:*                    
LISTEN      0      10                                                                           127.0.0.1:45556                                                                                              *:*                    
LISTEN      0      5                                                                        192.168.122.1:domain                                                                                             *:*                    
LISTEN      0      128                                                                                  *:ssh                                                                                                *:*                    
LISTEN      0      128                                                                          127.0.0.1:ipp                                                                                                *:*                    
LISTEN      0      100                                                                          127.0.0.1:smtp                                                                                               *:*                    
LISTEN      0      128                                                                          127.0.0.1:43483                                                                                              *:*                    
ESTAB       0      0                                                                         10.80.241.80:ssh                                                                                     10.52.43.159:51667                
ESTAB       0      0                                                                         10.80.241.80:ssh                                                                                     10.52.43.159:51356                
ESTAB       0      0                                                                         10.80.241.80:39224                                                                                  54.242.91.190:ssh                  
ESTAB       0      64                                                                        10.80.241.80:ssh                                                                                     10.52.43.159:52010                
LISTEN      0      128                                                                               [::]:7946                                                                                            [::]:*                    
LISTEN      0      128                                                                               [::]:10250                                                                                           [::]:*                    
LISTEN      0      128                                                                               [::]:sunrpc                                                                                          [::]:*                    
LISTEN      0      128                                                                               [::]:ssh                                                                                             [::]:*                    
LISTEN      0      128                                                                              [::1]:ipp                                                                                             [::]:*                    
LISTEN      0      100                                                                              [::1]:smtp                                                                                            [::]:*
```

```text
ss -tl # All TCP listening ports
```

```text
ss -tl
State       Recv-Q Send-Q                                                                   Local Address:Port                                                                                    Peer Address:Port                
LISTEN      0      128                                                                          127.0.0.1:10248                                                                                              *:*                    
LISTEN      0      128                                                                                  *:sunrpc                                                                                             *:*                    
LISTEN      0      10                                                                           127.0.0.1:45556                                                                                              *:*                    
LISTEN      0      5                                                                        192.168.122.1:domain                                                                                             *:*                    
LISTEN      0      128                                                                                  *:ssh                                                                                                *:*                    
LISTEN      0      128                                                                          127.0.0.1:ipp                                                                                                *:*                    
LISTEN      0      100                                                                          127.0.0.1:smtp                                                                                               *:*                    
LISTEN      0      128                                                                          127.0.0.1:43483                                                                                              *:*                    
LISTEN      0      128                                                                               [::]:7946                                                                                            [::]:*                    
LISTEN      0      128                                                                               [::]:10250                                                                                           [::]:*                    
LISTEN      0      128                                                                               [::]:sunrpc                                                                                          [::]:*                    
LISTEN      0      128                                                                               [::]:ssh                                                                                             [::]:*                    
LISTEN      0      128                                                                              [::1]:ipp                                                                                             [::]:*                    
LISTEN      0      100                                                                              [::1]:smtp                                                                                            [::]:*
```
