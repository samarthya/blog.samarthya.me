---
title: "Java Stream: Examples"
date: "2021-04-26T09:07:19Z"
slug: "java-stream-examples"
categories: ["java", "technical"]
tags: ["streams"]
aliases: ["/wps/2021/04/26/java-stream-examples/"]
wp_id: 1510
---

Streams are convenient way to reduce the line of codes, but an understanding them is equally challenging. I write this blog, after realising a desperate attempt at solving a trivial problem just took overwhelming time. (Could be that I am getting old, but never late to learn things again)

```text
public class PlaySteams {
    public static void main(String []args) {
        int[] a = new int[] {1,1,1,2,2,2,3,3,3,4,4,4};
        //Stream Sum of the array
        long sum = IntStream.range(0, a.length).count();

        System.out.printf("Sum: %d\n", sum);
        // Maximum
        System.out.printf("Max: %d\n", IntStream.range(0, a.length).map(i -> Integer.valueOf(a[i])).distinct().max().getAsInt());
        // Minimum
        System.out.printf("Min: %d\n", IntStream.range(0, a.length).map(i -> Integer.valueOf(a[i])).distinct().min().getAsInt());

        IntStream.range(0, a.length).map(i -> Integer.valueOf(a[i])).distinct().forEach(x -> System.out.printf("%d ", x));
        System.out.printf("Average (Distinct): %f\n", IntStream.range(0, a.length).map(i -> Integer.valueOf(a[i])).distinct().average().getAsDouble());

        System.out.printf(" Number of elements : %d\n", IntStream.of(a).asLongStream().count());

        IntStream.range(0, a.length).map(i -> Integer.valueOf(a[i])).forEach(x -> System.out.printf("%d ", x));
        System.out.printf("Average (All): %f\n", IntStream.range(0, a.length).map(i -> Integer.valueOf(a[i])).average().getAsDouble());

        List<Integer> listOfIntegers = IntStream.of(a).boxed().collect(Collectors.toList());
        System.out.println(listOfIntegers.toString());

        System.out.println("Length: ");
        System.out.println(listOfIntegers.size());

        // Creating a map
        // 1 -> 3
        // 2 -> 3 ...
        System.out.println(IntStream.range(0, a.length).map(i -> a[i]).boxed().collect(Collectors.groupingBy(Function.identity(), Collectors.counting())).toString());

        // Using list
        Map<Integer, Long> valueMap = listOfIntegers.stream().collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
        System.out.println(valueMap.toString());

        // Map of indexes
        // Indexes and value of the index
        System.out.println(IntStream.range(0, a.length).boxed().collect(Collectors.groupingBy( i -> a[Integer.valueOf(i)], Collectors.toList())));

    }
}
```

The example set remains the same for all the invocation.

```text
int[] a = new int[] {1,1,1,2,2,2,3,3,3,4,4,4};
```

## Example - 1:

```text
long sum = IntStream.range(0, a.length).count();
System.out.printf("Sum: %d\n", sum);
```

It simply runs over the length of the array and returns the total number of elements

```text
Sum: 12
```

## Example - 2:

Return the maximum

```text
System.out.printf("Max: %d\n", IntStream.range(0, a.length).map(i -> Integer.valueOf(a[i])).distinct().max().getAsInt());
```

```text
Max: 4
```

## Example - 3:

Returns the minimum

```text
System.out.printf("Min: %d\n", IntStream.range(0, a.length).map(i -> Integer.valueOf(a[i])).distinct().min().getAsInt());
```

```text
Min: 1
```

## Example - 4:

Run through the list and print distinct items

```text
IntStream.range(0, a.length).map(i -> Integer.valueOf(a[i])).distinct().forEach(
x -> 
System.out.printf("%d ", x));
```

```text
1 2 3 4
```

## Example - 5:

Average of the distinct items

```text
System.out.printf("Average (Distinct): %f\n", IntStream.range(0, a.length).map(i -> Integer.valueOf(a[i])).distinct().average().getAsDouble());
```

```text
Average (Distinct): 2.500000
```

## Example - 6:

Different way of getting the count of elements.

```text
System.out.printf(" Number of elements : %d\n", IntStream.of(a).asLongStream().count());
```

```text
Number of elements : 12
```

## Example - 7:

```text
IntStream.range(0, a.length).map(i -> Integer.valueOf(a[i])).forEach(x -> System.out.printf("%d ", x));
```

Get the list of elements

```text
1 1 1 2 2 2 3 3 3 4 4 4
```

## Example - 8:

```text
System.out.printf("Average (All): %f\n", IntStream.range(0, a.length).map(i -> Integer.valueOf(a[i])).average().getAsDouble());
```

```text
Average (All): 2.500000
```

## Example - 9:

```text
List<Integer> listOfIntegers = IntStream.of(a).boxed().collect(Collectors.toList());
System.out.println(listOfIntegers.toString());
```

```text
[1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
```

## Example - 10:

```text
System.out.println(IntStream.range(0, a.length).map(i -> a[i]).boxed().collect(Collectors.groupingBy(Function.identity(), Collectors.counting())).toString());
```

Creates a map of the value and the number of times it repeats

```text
1=3, 2=3, 3=3, 4=3}
```

## Example - 11:

```text
Map<Integer, Long> valueMap = listOfIntegers.stream().collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));
        System.out.println(valueMap.toString());
```

Using list that we had in `Example - 9` to get the map.

```text
{1=3, 2=3, 3=3, 4=3}
```

## Example - 12:

Returns the list of index for each value

```text
System.out.println(IntStream.range(0, a.length).boxed().collect(Collectors.groupingBy( i -> a[Integer.valueOf(i)], Collectors.toList())));
```

```text
{1=[0, 1, 2], 2=[3, 4, 5], 3=[6, 7, 8], 4=[9, 10, 11]}
```
