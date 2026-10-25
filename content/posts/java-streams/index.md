---
title: "Java Streams"
date: "2020-11-12T11:47:49Z"
slug: "java-streams"
categories: ["java", "technical"]
tags: ["streams"]
aliases: ["/wps/2020/11/12/java-streams/"]
wp_id: 1111
---

*Stream* is an new abstraction that lets one process data in a declarative way.

{{< lead >}}
**A stream does not store data and, in that sense, is not a data structure. It also never modifies the underlying data source.**
{{< /lead >}}

The easiest way to learn a new API or a construct is by trying it. So here is an [exercise](https://github.com/samarthya/javaex/tree/local/grains) that I tried to learn the Stream API. This is an exercise from [exercism.io](https://exercism.io/my/solutions/428fcd2c497c4098b5bd3121a1d66110).

The problem is the famous `grains` problem doubling the number of grains on each square of the chess which has 64 squares (8x8).

I started of by keeping things simple having a `LinkedHashMap` that stores `pre-initalized` square and number of `grains`.

```text
private Map<Integer, BigInteger> lHM = new LinkedHashMap<>();
```

```text
private void Initialize() {
        for(int i=0; i<64; i++) {
            if (i == 0) {
                lHM.put(Integer.valueOf(1), BigInteger.ONE);
                continue;
            }
            lHM.put(i+1, lHM.get(i).multiply(BigInteger.TWO));
        }
    }
```

`lHM` defined is initalized for all the possible grain permutations for a 64 square board.

```text
lHM.put(i+1, lHM.get(i).multiply(BigInteger.TWO));
```

E.g.

- For every square > 1 we are putting `Grains in the previous square * 2`

This is very simple version of and had to be improved so time to use Streams.

```text
import java.math.BigInteger;
import java.util.LinkedHashMap;
import java.util.Map;

import java.util.stream.IntStream;

/**
 * Grains on a board.
 * 1 + 2 + 6 + 18 + .......
 */
class Grains {

    BigInteger grainsOnSquare(final int square) {
        if (square < 1 || square > 64) {
            throw new IllegalArgumentException("square must be between 1 and 64");
        }
       return BigInteger.TWO.pow(square - 1);
    }

    BigInteger grainsOnBoard() {
        return IntStream.range(1, 65).mapToObj( i -> grainsOnSquare(i)).reduce(BigInteger::add).get();
    }

}
```

I did away with the data-structure and resorted to use simple Streams - `IntStream`.

For the method

```text
grainsOnSquare
```

I have used `pow` method of [BigInteger](https://docs.oracle.com/javase/7/docs/api/java/math/BigInteger.html) which simple calculates 2^(Square - 1)

- 1st Square 2^0 = 1
- 2nd Square 2^1 = 2
- .... 4th Square 2^3 = 8

Now it is easier to read and optimised. How about the total grains here is where the streams come in handy for me as I do not have a DS storing any values.

```text
IntStream.range(1, 65).mapToObj( i -> grainsOnSquare(i)).reduce(BigInteger::add).get();
```

I used the `range()` method to iterate between 1-64 as the second parameter is exclusive, and then for each square `i` I got the `grainsOnSquare` which was reduced using `BigInteger.add` and the final value is returned.

## References

- https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html
- https://www.oracle.com/technical-resources/articles/java/ma14-java-se-8-streams.html
- https://docs.oracle.com/javase/tutorial/collections/intro/index.html
