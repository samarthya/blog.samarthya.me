---
title: "Package String"
date: "2020-02-15T11:40:19Z"
slug: "package-string"
categories: ["technical"]
tags: ["exercism", "golang", "string", "strings"]
aliases: ["/wps/2020/02/15/package-string/"]
wp_id: 415
---

Just like Java or C++ there are standard libraries (packages) available with golang. The one that you might end up using the most often is `strings`.

For this blog, I was writing another practice [exercise](https://exercism.io/my/tracks/go) that is meant to count number of words in an input string.

{{< lead >}}
Go string is a sequence of variable-width characters (each 1 to 4 bytes).
{{< /lead >}}

## Definition of Word

1. A *number* composed of one or more ASCII digits (ie "0" or "1234") OR
2. A *simple word* composed of one or more ASCII letters (ie "a" or "they") OR
3. A *contraction* of two *simple words* joined by a single apostrophe (ie "it's" or "they're")

## Package : Strings

The package string exposes utility functions to manipulate UTF-8 encoded strings.

![](img_0846.jpg)

> Strings are value types and immutable, which means that once created, you cannot modify the contents of the string. In other words, strings are immutable arrays of bytes.
>
> — Official GoDocs

---

## Solution

```text
package wordcount

import (
    "strings"
    "unicode"
)

// Frequency of the words
type Frequency map[string]int

// WordCount Count the words occurrence.
func WordCount(in string) Frequency {
    var myMap Frequency = make(map[string]int, 0)

    in = strings.ToLower(in)
    inStrings := strings.FieldsFunc(in, func(c rune) bool {
        return c == ' ' || c == '\n' || c == '\t' || c == ','
    })

    for _, val := range inStrings {
        val = strings.TrimFunc(val, func(r rune) bool {
            return !unicode.IsLetter(r) && !unicode.IsDigit(r)
        })
        myMap[val]++
    }
    return myMap
}
```

## Functions used

- FieldsFunc
- TrimFunc

### FieldsFunc

More details [here](https://golang.org/pkg/strings/#FieldsFunc).

#### func FieldsFunc(s [string](https://golang.org/pkg/builtin/#string), f func([rune](https://golang.org/pkg/builtin/#rune)) [bool](https://golang.org/pkg/builtin/#bool)) [][string](https://golang.org/pkg/builtin/#string)

> *FieldsFunc* splits the string s at each run of Unicode code points c satisfying f(c) and returns an array of slices of s. If all code points in s satisfy f(c) or the string is empty, an empty slice is returned. *FieldsFunc* makes no guarantees about the order in which it calls f(c). If f does not return consistent results for a given c, FieldsFunc may crash.
>
> golang official documentation

```text
func(c rune) bool {
        return c == ' ' || c == '\n' || c == '\t' || c == ','
    })
```

The function ***FieldFunc*** is supplied with an input string `s` and a function that runs through the runes (*unicode point*) and returns the split if the condition evaluates to be true.

#### Example

```text
in > testing, 1, 2 testing
```

The function will split it as under

```text
{"testing", "1", "2", "testing"}
```

### TrimFunc

More details [here](https://golang.org/pkg/strings/#TrimFunc).

#### func TrimFunc(s [string](https://golang.org/pkg/builtin/#string), f func([rune](https://golang.org/pkg/builtin/#rune)) [bool](https://golang.org/pkg/builtin/#bool)) [string](https://golang.org/pkg/builtin/#string)

> TrimFunc returns a slice of the string s with all leading and trailing Unicode code points c satisfying f(c) removed.
>
> golang documentation

This function trims down the unwanted characters in the string.

```text
func(r rune) bool {
            return !unicode.IsLetter(r) && !unicode.IsDigit(r)
}
```

Essentially we remove everything that is not letter or digit form the string.

#### Example

```text
in> car: carpet as java: javascript!!&@$%^&
```

It will strip `car:` to `car` likewise `javascript` will be stripped of the unwanted characters in the end.

### -- THE - END --
