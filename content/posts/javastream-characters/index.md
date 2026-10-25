---
title: "JavaStream: Characters"
date: "2020-11-13T10:20:02Z"
slug: "javastream-characters"
categories: ["java", "technical"]
tags: ["streams"]
aliases: ["/wps/2020/11/13/javastream-characters/"]
wp_id: 1116
---

Continuing from the last blog how about checking a pangram using streams.

```text
public class PangramChecker {

    private String allChars = "abcdefghijklmnopqrstuvwxyz";

    public boolean isPangram(String input) {
        if (input.length() <= 0 || input.isBlank()){
            return false;
        }
        return (allChars.chars().map(x -> (char) x).filter(x -> input.toLowerCase().indexOf(x) >= 0).count() == 26);
    }

}
```

All the for loops have been squeezed into a simple line

## The Logic

- Define a `String` for all the characters in the English language - `allChars`
- Get the Stream using `allChars.chars()`
- Since it returns an `int` map it to `Char`
- Look for every character one by one in the `Input String` using `indexOf`. (It returns -1 for character not found.)
- Get the count of all the characters found, if anyone was not found we will have less than 26.

It can be further optimized... want to try?
