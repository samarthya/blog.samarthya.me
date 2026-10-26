---
title: "Docker: Clean in Bulk"
date: "2021-12-27T12:00:00Z"
slug: "docker-clean-in-bulk"
description: "So to delete there was one hard hack way of cleaning it all"
categories: ["docker", "technical"]
tags: ["clear", "delete", "docker"]
aliases: ["/wps/2021/12/27/docker-clean-in-bulk/"]
recovered: "Internet Archive snapshot 2026-05-18"
---

I will define the problem I was facing

> Too many snapshots versions for the same image were there on my system
>
> Freaky developer

So to delete there was one hard hack way of cleaning it all

```text
docker system prune -f
```

That would have killed all the dangling images but still left many I wished cleaned.

## Light bulb moment

So while pondering what to do which included manually going one by one, I thought of trying this

### Step 1

List all the images I wished to delete and narrow down to the specific versions

```text
docker image ls

// Gave a long listing
```

```text
[root@samarthya ~]# docker image ls myartifactory.samarthya.me/opendataconnector/2.2/my-connector 
REPOSITORY                                                      TAG                        IMAGE ID       CREATED          SIZE
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211227-0800   2ff1893f12dc   51 minutes ago   658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211226-0801   41516ac3d35b   25 hours ago     658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211225-0800   f0b1d434f8ff   2 days ago       658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211224-0800   1a0e64e65e6e   3 days ago       658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211223-1024   0f6426638df8   3 days ago       658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211223-0800   c5afad3c4ad3   4 days ago       658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211222-0800   cd45ff9d8ae9   5 days ago       658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211221-0800   74f9e90099b0   6 days ago       658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211220-0800   0e1b917654ac   7 days ago       658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211219-0800   f7341845f1db   8 days ago       658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211218-0800   79d6911c6ab9   9 days ago       658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211217-0922   e26236e6dbc9   10 days ago      658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211217-0800   1b513e15af6b   10 days ago      658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211216-1035   edc8e8a7cf12   10 days ago      658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211216-0945   50a0755bb248   10 days ago      658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211216-0800   61899dbefc88   11 days ago      658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211215-0800   0376ceb8248e   12 days ago      658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211214-1031   1527a2319dcc   12 days ago      658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211214-0917   7dd6eb7a7382   13 days ago      658MB
myartifactory.samarthya.me/opendataconnector/2.2/my-connector   2.2-SNAPSHOT-211210-0916   b304d9979b4b   2 weeks ago      658MB
```

So I know I could get the listing, now if I just pipe this listing to the `docker rmi` it should work & I tried the following command.

```text
[root@muntest001601 ~]# docker rmi -f `docker image ls myartifactory.samarthya.me/opendataconnector/2.2/my-connector -q`
Untagged: myartifactory.samarthya.me/opendataconnector/2.2/my-connector:2.2-SNAPSHOT-211227-0800
Untagged: myartifactory.samarthya.me/opendataconnector/2.2/my-connector@sha256:b3b551ccb8d29ad713fc861e2fe105a7289d37e21cff4c902db07a602270e9ae
Untagged: myartifactory.samarthya.me/my-connector:2.2-SNAPSHOT
Deleted: sha256:7153d9c5af71f8ab1c8e13e12d0f4950483bf4aaa6174709f7d1acc1dfbbab89
Deleted: sha256:5d429c41cf582d9c0171e9e3dd3f6bb536b337ba84e4b28c908cb6b0d9b800ff
Deleted: sha256:eb15a2cfecc1b94a96cd9f850404ebd2bbc0f5d61e6b6525f72a5290fe927421
Deleted: sha256:65e53cf22b400bd45c3e59f830db99b89830c732e2caece1036dec33174d3132
Deleted: sha256:99d887aa09ea61c49f1047526faf7bb534118720ea77308b4d8b1d1b96143b9d
Deleted: sha256:ae210b60ea32790c0fccbdfd1067b3fcaa9a73ec255c71605edd48e88e62e20d
Untagged: myartifactory.samarthya.me/opendataconnector/2.2/my-connector:2.2-SNAPSHOT-211226-0801
Untagged: myartifactory.samarthya.me/opendataconnector/2.2/my-connector@sha256:bd7b869e78d45279a66936b53116e8e7c016707ca60c7578ffcf49bb62be7c25
Deleted: sha256:fb04a750af2dad61e9d03a45a06ec0d32de233b67ce147e39337501f3f2ba6e2
Deleted: sha256:cdfef45f754806478708a4ab676919b517d0d39a91bd8c7f33ec8bc026b76476
Deleted: sha256:1249ed58b9173463a2a11897ae3328a5ec1d44965e9dc6ded56b2b69db827191
Deleted: sha256:62d46db913565fc8b20f03ee7971a1f4cd1facfa09922dfa2c9c1189f3be275c
Deleted: sha256:95b6effdca41891099d4677465e5a07a5f60529a4a5c1d12eabe05848ce50aae
Deleted: sha256:c5f9b59d60e5097fcaa29212af49e9cd30155af49df707a7ab60e7d458074e0b
Untagged: myartifactory.samarthya.me/opendataconnector/2.2/my-connector:2.2-SNAPSHOT-211225-0800
Untagged: myartifactory.samarthya.me/opendataconnector/2.2/my-connector@sha256:9126e9b4421cb0b6c13208a6ee3ddaedd212585ed88aeeb13927af86b564be72
...
```

Result all the selected image versions were wiped clean!
