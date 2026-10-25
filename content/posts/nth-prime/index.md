---
title: "Nth Prime"
date: "2020-12-15T08:21:32Z"
slug: "nth-prime"
categories: ["java", "technical"]
tags: ["prime", "streams"]
aliases: ["/wps/2020/12/15/nth-prime/"]
wp_id: 1172
---

Prime number is an age old problem. I am trying to solve it via streams.

```text
class PrimeCalculator {

    public int nth(int nth) {
        if (nth <= 0)
            throw new IllegalArgumentException();

        // Will skip the nth - 1
        // 2 to n-1
        return IntStream.iterate(2, i -> i + 1).filter(PrimeCalculator::isPrime).skip(nth - 1).findFirst().getAsInt();
    }

    public static boolean isPrime(int x) {
        // till half of x
        return IntStream.rangeClosed(2, (int) (x/2) ).dropWhile(i -> x % i != 0).findFirst().isEmpty();
    }
}
```

## Explanation

```text
public int nth(int nth) {
        if (nth <= 0)
            throw new IllegalArgumentException();

        // Will skip the nth - 1
        // 2 to n-1
        return IntStream.iterate(2, i -> i + 1).filter(PrimeCalculator::isPrime).skip(nth - 1).findFirst().getAsInt();
    }
```

The method `nth(int)` allows you to return the nth prime starting at `2, 3, 5....`

- If the `nth` is negative or l.t.e 0 return an illegal argument exception.
- Else, Iterate 2 onwards
- Filter all the elements that are prime.
- Skip all `n - 1` elements.
- Find first and return it as int.

```text
static <T> Stream<T> iterate(T seed,
                             UnaryOperator<T> f)
```

{{< lead >}}
Returns an infinite sequential ordered `Stream` produced by iterative application of a function `f` to an initial element `seed`.
{{< /lead >}}

```text
Stream<T> skip(long n)
```

{{< lead >}}
Skip is a stateful intermediate operation.
{{< /lead >}}

> `Skip()` Returns a stream consisting of the remaining elements of this stream after discarding the first `n` elements of the stream. If this stream contains fewer than `n` elements then an empty stream will be returned.
>
> from java docs

```text
Optional<T> findFirst()
```

{{< lead >}}
findFirst is a short-circuiting terminal operation
— java docs
{{< /lead >}}

> An intermediate operation is short-circuiting if, when presented with infinite input, it may produce a finite stream as a result. A terminal operation is short-circuiting if, when presented with infinite input, it may terminate in finite time.
>
> java docs

## Helpers

- https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html
- https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html#iterate-T-java.util.function.UnaryOperator-
- https://docs.oracle.com/javase/8/docs/api/java/util/stream/Stream.html#skip-long-
- https://docs.oracle.com/javase/8/docs/api/java/util/stream/package-summary.html#StreamOps
