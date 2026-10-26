---
title: "ssh-keygen & ssh-copy-id"
date: "2022-02-25T12:00:00Z"
slug: "ssh-keygen-ssh-copy-id"
description: "– The SSH protocol uses public key cryptography for authenticating hosts and users."
categories: ["technical"]
tags: ["ssh-key-gen"]
aliases: ["/wps/2022/02/25/ssh-keygen-ssh-copy-id/"]
recovered: "Internet Archive snapshot 2026-05-18"
---

`ssh-keygen` allows generation of new key pair for authentication (SSH).

```text
> ssh-keygen --help
unknown option -- -
usage: ssh-keygen [-q] [-b bits] [-t dsa | ecdsa | ed25519 | rsa | rsa1]
                  [-N new_passphrase] [-C comment] [-f output_keyfile]
       ssh-keygen -p [-P old_passphrase] [-N new_passphrase] [-f keyfile]
       ssh-keygen -i [-m key_format] [-f input_keyfile]
       ssh-keygen -e [-m key_format] [-f input_keyfile]
       ssh-keygen -y [-f input_keyfile]
       ssh-keygen -c [-P passphrase] [-C comment] [-f keyfile]
       ssh-keygen -l [-v] [-E fingerprint_hash] [-f input_keyfile]
       ssh-keygen -B [-f input_keyfile]
       ssh-keygen -D pkcs11
       ssh-keygen -F hostname [-f known_hosts_file] [-l]
       ssh-keygen -H [-f known_hosts_file]
       ssh-keygen -R hostname [-f known_hosts_file]
       ssh-keygen -r hostname [-f input_keyfile] [-g]
       ssh-keygen -G output_file [-v] [-b bits] [-M memory] [-S start_point]
       ssh-keygen -T output_file -f input_file [-v] [-a rounds] [-J num_lines]
                  [-j start_line] [-K checkpt] [-W generator]
       ssh-keygen -s ca_key -I certificate_identity [-h] [-n principals]
                  [-O option] [-V validity_interval] [-z serial_number] file ...
       ssh-keygen -L [-f input_keyfile]
       ssh-keygen -A
       ssh-keygen -k -f krl_file [-u] [-s ca_public] [-z version_number]
                  file ...
       ssh-keygen -Q -f krl_file file ...
```

```text
ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:KjqBCXEEFIBOOPDJ6j45tOBogwggxw3pAqECLG/r9fI root@mymachine.net
The key's randomart image is:
+---[RSA 2048]----+
|%* .             |
|%==.             |
|O*+o             |
|*o* .            |
|=* .    S        |
|*.o .  .         |
|Oooo...          |
|=Oo....          |
|..=. oE          |
+----[SHA256]-----+
```

****SSH Keys****

– The SSH protocol uses public key cryptography for authenticating hosts and users.

– SSH keys are authentication credentials just like passwords.

`ssh-copy-id` allows copying/installation of public key to a server to allow public key authentication.

```text
> ssh-copy-id -h
Usage: /usr/bin/ssh-copy-id [-h|-?|-f|-n] [-i [identity_file]] [-p port] [[-o <ssh -o options>] ...] [user@]hostname
        -f: force mode -- copy keys without trying to check if they are already installed
        -n: dry run    -- no keys are actually copied
        -h|-?: print this help
```

```text
> ssh-copy-id root@othermachine.net
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/root/.ssh/id_rsa.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
root@othermachine.net's password: 
 
Number of key(s) added: 1

Now try logging into the machine, with:   "ssh 'root@othermachine.net'"
and check to make sure that only the key(s) you wanted were added.
```
