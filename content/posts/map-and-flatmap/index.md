---
title: "map and FlatMap"
date: "2020-11-30"
slug: "map-and-flatmap"
description: "Java 8 streams: what map and flatMap do, with small examples of each."
categories: ["technical"]
aliases: ["/wps/2020/11/30/map-and-flatmap/", "/wps/2026/10/23/map-and-flatmap/"]
wp_id: 1120
---

## package java.util.stream;

Referring to the original Java 8 [Documentation](https://docs.oracle.com/javase/8/docs/api/index.html?java/util/stream/Stream.html).

```text
<R> Stream<R> flatMap(Function<? super T,? extends Stream<? extends R>> mapper)
```

- Returns a stream consisting of
  1. Results of **replacing each element of this stream** with the contents of a mapped stream produced by applying the provided mapping function to each element.

```text
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

public class Main {

    public static void main(String[] args) {
	    // write your code here
        int myArray[] = { 1, 1, 2, 3, 4 , 5,6, 6,6, 7, 7, 7, 7, 7,7,3, 4, 3, 3, 2, 2, 2, 2, 2 };

        // Simple map
        // Multiply each element by 5
        Arrays.stream(myArray).map(index -> index * 5).forEach(System.out::println);
    }
}
```

The stream above multiplies each element by 5.

```text
public class Main {

    public static void main(String[] args) {
	    // write your code here
        int myArray[] = { 1, 1, 2, 3, 4 , 5,6, 6,6, 7, 7, 7, 7, 7,7,3, 4, 3, 3, 2, 2, 2, 2, 2 };

        // Will create a map of
        // Item that appears and the number of times it appears.
        Map<Integer, Integer> myMap = Arrays.stream(myArray).mapToObj(i -> Integer.valueOf(i)).sorted().collect(Collectors.groupingBy(Function.identity(), Collectors.summingInt(e -> {
            System.out.println(" Element read: " + e);
            return 1;
        })));

        myMap.keySet().forEach( e -> {
            System.out.println(" [ " + e + " ]  = " + myMap.get(e).intValue());
        });

        //[[1,2], [2,6], [3,4]]
        //[1,2,2,6....]
        int[] myInts = myMap.keySet().stream().mapToInt(i -> Integer.valueOf(i)).flatMap(i -> IntStream.of(i, myMap.get(i))).toArray();

        Stream.of(myInts).forEach(System.out::println);
    }
}
```

flatMap as used in the above example allows creation of one stream from individual elements of the original stream which had.

```text
[[1,2], [2,6], [3,4]]
```

FlatMap
