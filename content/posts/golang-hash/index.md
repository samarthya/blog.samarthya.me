---
title: "GoLang: Hash"
date: "2021-02-01T09:20:50Z"
slug: "golang-hash"
categories: ["golang", "technical"]
tags: ["crypto", "hash"]
aliases: ["/wps/2021/02/01/golang-hash/"]
wp_id: 1307
---

Previously I talked about files, encoding in `golang`. In this LTD (learn to do) I will talk about `hash` package in general.

https://blog.samarthya.me/wps/2021/01/30/golang-encoding/

## Help

- <https://golang.org/pkg/hash/#Hash>
- <https://golang.org/pkg/crypto/#Hash.New>
- <https://golang.org/src/crypto/crypto.go?s=364:378#L6>
- <https://golang.org/pkg/crypto/#pkg-subdirectories>

{{< lead >}}
Package crypto collects common cryptographic constants.
— Official golang documentation
{{< /lead >}}

```text
const (
    MD4         Hash = 1 + iota // import golang.org/x/crypto/md4
    MD5                         // import crypto/md5
    SHA1                        // import crypto/sha1
    SHA224                      // import crypto/sha256
    SHA256                      // import crypto/sha256
    SHA384                      // import crypto/sha512
    SHA512                      // import crypto/sha512
    MD5SHA1                     // no implementation; MD5+SHA1 used for TLS RSA
    RIPEMD160                   // import golang.org/x/crypto/ripemd160
    SHA3_224                    // import golang.org/x/crypto/sha3
    SHA3_256                    // import golang.org/x/crypto/sha3
    SHA3_384                    // import golang.org/x/crypto/sha3
    SHA3_512                    // import golang.org/x/crypto/sha3
    SHA512_224                  // import crypto/sha512
    SHA512_256                  // import crypto/sha512
    BLAKE2s_256                 // import golang.org/x/crypto/blake2s
    BLAKE2b_256                 // import golang.org/x/crypto/blake2b
    BLAKE2b_384                 // import golang.org/x/crypto/blake2b
    BLAKE2b_512                 // import golang.org/x/crypto/blake2b

)
```

Let's try out a simple MD5 hasher.

{{< lead >}}
Package md5 implements the MD5 hash algorithm as defined in RFC 1321
— packagemd5
{{< /lead >}}

```text
fmt.Printf(" Is BLAKE2b_256 available: %t\n", crypto.BLAKE2b_256.Available())
fmt.Printf(" Is MD5 available: %t\n", crypto.MD5.Available())

var hasher hash.Hash
// Creates a new MD5 hasher
hasher = md5.New()

io.WriteString(hasher, "And Leon's getting laaarger!")
fmt.Printf("%x\n", hasher.Sum(nil))
```

## New()

New returns a new hash.Hash computing the MD5 checksum.

## Sum()

Sum returns the MD5 checksum of the data.

```text
fmt.Printf(" Is MD5 available: %t\n", crypto.MD5.Available())
	fmt.Printf(" Is SHA1 available: %t\n", crypto.SHA1.Available())
	fmt.Printf(" Is SHA256 available: %t\n", crypto.SHA256.Available())
var hasher hash.Hash

// Creates a new MD5 hasher
hasher = md5.New()

// Version 1
io.WriteString(hasher, "And Leon's getting laaarger!")
fmt.Printf("%x\n", hasher.Sum(nil))
fmt.Printf("Size: %d\n", hasher.Size())

// Version 2
var data = []byte("Data for which the md5 hash will be computed")

fmt.Printf("%x\n", hasher.Sum(data))
fmt.Printf("Size: %d\n", hasher.Size())

sha1 := sha1.New()
fmt.Printf("%x\n", sha1.Sum(nil))
fmt.Printf("Size: %d\n", sha1.Size())

sha256 := sha256.New()
fmt.Printf("%x\n", sha256.Sum(nil))
fmt.Printf("Size: %d\n", sha256.Size())
```
