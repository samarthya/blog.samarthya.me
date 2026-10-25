---
title: "Consumer <Intf>"
date: "2020-12-04T14:38:51Z"
slug: "consumer"
categories: ["technical"]
tags: ["consumer", "functional", "interface", "java"]
aliases: ["/wps/2020/12/04/consumer/"]
wp_id: 1124
---

The utility package `java.util.function` has this functional [interface Consumer](https://docs.oracle.com/javase/8/docs/api/java/util/function/package-summary.html).

Each functional interface (Annotated with @[FunctionalInterface](https://docs.oracle.com/javase/8/docs/api/java/lang/FunctionalInterface.html)) conceptually has a single method (abstract) called the functional method to which the lambda expression's parameter and return types are matched against. Functional interfaces often represent abstract concepts like functions, actions, or predicates.

> Instances of functional interfaces can be created with lambda expressions, method references, or constructor references.

{{< lead >}}
Functional interface provide target types for lambda expressions and method references.
— Oracle 8 [Java Doc]
{{< /lead >}}

Instance methods

| Modifier and Type | Method and Description |
| --- | --- |
| `void` | `accept(T t)` Performs this operation on the given argument. |
| `default Consumer<T>` | `andThen(Consumer<? super T> after)` Returns a composed `Consumer` that performs, in sequence, this operation followed by the `after` operation. |

{{< lead >}}
Functional interfaces can provide a target type in multiple contexts - assignment context, method invocation, or cast context
— Oracle 8 [Java Doc]
{{< /lead >}}

## Examples

Let's use this `Consumer.accept` method.

> Performs this operation on the given argument.
>
> `accept(T t)`

```text
package me.samarthya;

import java.util.function.Consumer;

public class Main {

    public static void ExampleOne() {
        Consumer<String> myString = (x) -> System.out.println(x);
        myString.accept("Hello World!");
    }
    public static void main(String[] args) {
        ExampleOne();
    }
}
```

```text
public class Main {

    public static void ExampleOne() {
        Consumer<String> myString = (x) -> System.out.println(x);
        myString.accept("Hello World!");
    }
    public static void ExampleTwo() {
        Consumer<List<String>> myList = (x) -> x.stream().sorted().forEach( e -> System.out.println(" Element: "+ e));
        List<String> dummyContents = new LinkedList<String>(){
            {
                add(" Hello");
                add(" World");
                add("!");
            }
        };

        myList.accept(dummyContents);
    }

    public static void main(String[] args) {
        System.out.println(" Ex1.");
        ExampleOne();
        System.out.println(" Ex2.");
        ExampleTwo();
    }
}
```

### andThen(Consumer)

```text
public static void ExampleThree() {
        Consumer<List<String>> toUpper = (x) -> x.replaceAll(String::toUpperCase);
        Consumer<List<String>> toJoin = (x) -> x.stream().map(e -> String.format("%s(%d) ", e, e.length())).forEach(e -> System.out.printf(e));

        List<String> dummyContents = new LinkedList<String>() {
            {
                add("Hello");
                add("World");
                add("!");
            }
        };

        toUpper.andThen(toJoin).accept(dummyContents);

    }

    public static void main(String[] args) {
        System.out.println(" Ex3.");
        ExampleThree();
    }
```

Outputs

```text
Ex3.
HELLO(5) WORLD(5) !(1)
```

## Helpers

- https://docs.oracle.com/javase/8/docs/api/java/util/function/Function.html
- https://docs.oracle.com/javase/8/docs/api/java/util/function/Consumer.html
- [Interface Predicate<T>](https://docs.oracle.com/javase/8/docs/api/java/util/function/Predicate.html)
