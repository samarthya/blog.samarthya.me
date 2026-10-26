---
title: "Handshake: JS"
date: "2020-01-11T12:00:00Z"
slug: "handshake-js"
description: "Let’s say the input is 2 the output should be [“double blink”]."
categories: ["personal"]
tags: ["bitwise", "exercism", "js", "optimisation"]
aliases: ["/wps/2020/01/11/handshake-js/"]
recovered: "Internet Archive snapshot 2026-04-21"
---

# Secret Handshake

Objective was relatively simple.

- A numeral will be provided as input.
- Based on the binary equivalent, one needs to compute the secret handshake.

Rule for handshake.

> ```text
1 = wink
10 = double blink
100 = close your eyes
1000 = jump
10000 = Reverse the order of the operations in the secret handshake.
```

## Example

Let’s say the input is 2 the output should be [“double blink”].

## Version 1.0

```text
function binaryOptimized(number) {         
     var binaryRep = [];                 
     do {            
         binaryRep.push(parseInt(number%2));             
         number /= 2;          
    } while (parseInt(number) > 0);               
    return binaryRep;                     
}

function getCommand(pseudo, arr) {       switch(pseudo) {                  
case 1:   arr.push ("wink");  break;               
case 10:  arr.push ("double blink"); break;            
case 100:  arr.push ("close your eyes"); break;           
case 1000:  arr.push ("jump");   break;            
case 10000:  arr = arr.reverse();         
}                        
return arr;                      
} 
                              
export const commands = (input) => {       
    var rep = binaryOptimized(input);         
    var commands = [];            
    rep.map((element, i) => {            
           getCommand(element * Math.pow(10, i), commands)              
    });               
    return commands;               
};
```

The code is self explanatory

Defined a binary calculation function, computed the equivalent binary representation. Used the individual element to compute the corresponding command and responded back with the response.

## Can it be optimized?

The think I misinterpreted was that, binary calculation of number is an optional thing.

### BITWISE Operator

There are two basic bitwise operation ‘&’ and ‘|’.

> Bitwise operators treat their operands as a sequence of 32 bits (zeroes and ones), rather than as decimal, hexadecimal, or octal numbers.

#### Example

```text
5 => 101
We can check the bits now
2^0 = 1 => 1
2^1 = 2 => 10
2^2 = 4 => 100
2^3 = 8 => 1000
2^4 = 16 => 10000
2^5 = 32 => 100000
```

Now instead of converting it to binary I can simply & to compute the on bits.

```text
5&1  = 101 & 1 => 1
5&2 = 101 & 10 => 0
5&4 = 101 & 100 => 4 
5&8 = 101 & 1000 => 0
5&16 = 101 & 10000 => 0
5&32 = 101 & 100000 => 0
```

Also you can define the left shift to compute the bit rep.

```text
1<<0 = 1
1<<1 = 10 = 2
1<<2 = 100 = 4
1<<3 = 1000 = 8
1<<4 = 10000 = 16
1<<5 = 100000 = 32
```

So to compute the secret handshake it is just matter of computing the on bits and add it to the final array.

I defined the Array of handshakes

```text
HANDSHAKES = ["wink", "double blink", "close your eyes", "jump"];
```

To compute the handshake sequence I just to validate the ON bits.

### Array.filter

> let newArray = arr.filter(callback(element[, index[, array]])[, thisArg])

Documentation is available [here](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter).

Now utilizing the left shift operator, and bitwise & it was easy to compute the final array of handshakes.

```text
HANDSHAKES.filter( (signal, index) => n & (1 << index));
```

Where n is the input number from user.

### Illustration

If n = 3 then,

```text
HANDSHAKES.filter() will Execute from 0..3

3 = (11)BASE2

Now, 

[], 0 => 3&1, ["wink"]
[], 1 => 3&2, ["wink", "double blink"]
[], 2 => 3&4, ["wink", "double blink"]
[], 3 => 3&8, ["wink", "double blink"]
```

For the last condition to reverse we can employ

```text
if (n & (1 << HANDSHAKES.length)) {
    result.reverse();
}
```

For n = 3, above condition evaluates false so the final result comes out as

[“wink”, “double blink”]

```text
const HANDSHAKES = ["wink", "double blink", "close your eyes", "jump"];

export const commands = (n) => {
  if (typeof n !== "number") {
    throw new Error("Handshake must be a number");
  }  
  const result = HANDSHAKES.filter((signal, index) => n & (1 << index));

  if (n & (1 << HANDSHAKES.length)) {
    result.reverse();
  }

  return result;
};
```

— THE – END —
