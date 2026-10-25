---
title: "Pangram"
date: "2020-01-30T15:59:51Z"
slug: "pangram"
description: "A pangram (Greek: παν γράμμα, pan gramma, \"every letter\") is a sentence using every letter of the alphabet at least once. The best known English pangram is:\nThe quick brown fox jumps over the lazy dog."
categories: ["others", "technical"]
tags: ["golang", "pangram"]
aliases: ["/wps/2020/01/30/pangram/"]
wp_id: 359
---

I wrote my first program for Pangram in JS [here]({{< relref "/posts/optimizing-in-js" >}}) and attempted few variations to optimize the readability and execution time. This time the code challenge was in Golang and it was satisfying attempt to do in first try.

> Determine if a sentence is a pangram. A pangram (Greek: παν γράμμα, pan gramma, "every letter") is a sentence using every letter of the alphabet at least once. The best known English pangram is:
>
> The quick brown fox jumps over the lazy dog.

```text
package pangram

import "strings"

// Alphabets all the characters.
const Alphabets string = "abcdefghijklmnopqrstuvqxyz"

// IsPangram checks for pangram in the inputs string.
func IsPangram(in string) bool {
    in = strings.ToLower(strings.TrimSpace(in))
    if in == "" {
        return false
    }

    for _, v := range Alphabets {
        if strings.IndexRune(in, v) < 0 {
            return false
        }
    }
    return true
}
```

I could have simplified it further by instead of having the `const Alphabets` just loop through rune `'a'` to `'z'`.

The code is simple enough to go through, where I check in for the index of all the runes in the string `Alphabets` and if any one is not found, it is not a `PANGRAM`.

-- THE - END --
