---
title: "Maths problem in JS"
date: "2020-01-10T12:00:00Z"
slug: "maths-problem-in-js"
description: "We will utilize regular expression to identify and parse the elements from the input string."
categories: ["others"]
tags: ["js", "maths", "regularexpression"]
aliases: ["/wps/2020/01/10/maths-problem-in-js/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

## Objective

Solve a simple math problem.

> Parse and evaluate simple math word problems returning the answer as an integer.

## RegularExpression (JS)

We will utilize regular expression to identify and parse the elements from the input string.

> Regular expressions are patterns used to match character combinations in strings.

### Defining

---

You can define a regular expression to be evaluated by using either of the two approaches mentioned below.

#### Slashes

```text
let exp = /[0-9]*/;
```

#### Constructor

let exp = new RegExp(‘[0-9]\*’);

First lets define the patterns to identify thee numerals.

1. It can be positive or negative
2. It can be single digit or more than one.

```text
const Numeric = /-?\d+\b/g; // Matches any digital numeric.
```

## Elements

### Numeric

Numeric defined above allows you match for any 1 or more (+) digits (\d) ending at a words boundary (\b) and starting with an optional (-?) negative symbol to denote a negative number.

> You can find more information [here](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions).

The regular expression can be evaluated against any string input. I used a method called *match()*

> String.match(regular\_expression)

This method returns

An *Array* whose contents depend on the presence or absence of the global (`g`) flag, or null if no matches are found.

- If the `g` flag is used, all results matching the complete regular expression will be returned, but capturing groups will not.
- if the `g` flag is not used, only the first complete
  match and its related capturing groups are returned. In this case, the
  returned item will have additional properties as described below.

### Operations

Likewise we can employ a similar regular expression to identify the operations.

> const ADDITION = /\bplus\b/ig;
>
> const SUBTRACTION = /\bminus\b/ig;
>
> const DIVIDE = /\bdivided\b/ig;
>
> const MULTIPLICATION = /\bmultiplied\b/ig;

The ‘i’ is for ignoring the case.

## Parsing

Before we write our logic to compute the Mathematical equivalent, we need to parse the information from the input string (question).

> this.numbers = this.question.match(Numeric).map((ele, i, arr) => parseInt(ele));

- this.numbers: Identifies the numerals present in the input string; All of them.
- this.question: It is the input string.
- Method match(): Takes the RegEx Numeric defined above.
- Map() allows mapping of the string parsed into a integer.

## Logic

The v1.0 I wrote is very basic, without much optimization. It simply splits the question (separated by ” “) and passed over each token to identify the operation and performs the operation on the Numerals identified in the previous step.

```text
1. if (this.question != null) {      
2.          const elements = this.question.split(" ");
3.          for (const element of elements) {
```

[split](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/split)(seperator) is a method that tokenizes the input string.

> It returns an Array of strings, split at each point where the separator occurs in the given string.

```text
4. if (element.match(ADDITION) != null) {
5.          if (index+1 <= this.numbers.length) {
6.            sum += (this.numbers[index] + this.numbers[index-1]);
7.          } else {
8.            sum += this.numbers[index-1]
9.          }
10.          index += 2;
11.       }
```

While we iterate through the individual element of the tokenized string. We can evaluate the operation found by matching the operation found. In 4. above we are looking for operation ADDITION if present we will move to check how many numerals were found.

> We have also defined a variable index that start at 1, it allows us to ensure we perform binary operation. It will just be clear why.

If the operation is found we need to perform x + y, where x is the first element found and y will be the second element if present.

### Checks

Loops starts with index at 1, assume we send in a statement

> What is 50 plus 3?

The operation is plus and the numerals identified are [53, 2]

When line 5. is executed the first time

```text
index = 1;
so
index + 1 = 2 is <= 2 which is [53, 2]
so sum is calculated to be
numbers[0] + numbers[1]
= 50 + 3
= 53
```

If it was just one number instead of two assuming just 50, then for the same loop

```text
index = 1;
index + 1 = 2 is not <= 1 so the loop else is evaluated
sum = numbers[1-1 = 0]
sum = 50.
```

— THE – END —
