---
title: "Optimizing in JS"
date: "2019-12-13T12:00:00Z"
slug: "optimizing-in-js"
description: "You never stop learning is not just a phrase, it is something I live everyday. Today, I was just trying out my skills with JS and was solving an innocuous problem, in JS."
categories: ["others"]
tags: ["js", "learn", "pangram"]
aliases: ["/wps/2019/12/13/optimizing-in-js/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

![Sonic the hedgehog](img_20191204_212744-scaled-e1576230534272.jpg)

You never stop learning is not just a phrase, it is something I live everyday. Today, I was just trying out my skills with JS and was solving an innocuous problem, in JS.

> Pangram: A pangram is a sentence using every letter of the alphabet at least once.
>
> E.g. The quick brown fox jumps over the lazy dog.

Like every old school programmer I was trying to solve it in the easiest of ways without breaking a sweat and the first version I could come up with was as under.

```text
// Define an string of all Alphabets.
export const ALPHABETS = "abcedfghijklmnopqrstuvwxyz";

// isPangram allows you input a string to be validated for Pangram
export const isPangram = (pangram) => {

  if(pangram == null || pangram.length == 0) {

    return false;

  }

  pangram = pangra.toLowerCase();

  var x;

  for (x in ALPHABETS){
    if( pangram.indexOf(ALPHABETS[x]) >= 0) {
      continue;
    } else {
      return false;
    }
  }
  return true;
};
```

So v1 was not much fat code,  I was thinking but then the geek in me was trying to ask can it be simplified further? Optimized in a way it looks cool? and so started my struggle to better the version 1, I had just written.

## Problem 1: How to generate the character set

So I thought, instead of having a simple constant string, how about I make it a function to first generate an Array that has all the characters from English; all from A … Z. (Some helpful [link](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/from))

```text
Array.from({length: 26}, (_, i) => { String.fromCodeCode(97 + i)});
```

How I used it was like this.

```text
const Alphabets = () => Array.from({length:26}, (_, i) =>String.fromCharCode(97+i));
```

Now, after having this Array it was time to look for the ‘Pangram’ in the string. Another method [*every*()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/every) and [includes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/includes)() came to the [rescue](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/every).

### V2.0

```text
// isPangram allows you to look for Pangram.
export const isPangram = (pangram) => {
     var alphabets = Alphabets();
     var lowerCase = pangram.toLowerCase();
     return alphabets.every( character=>lowerCase.includes(character));
};
```

and Voila, I think made a better version from what I had at v1.0.

##### – The – End –
