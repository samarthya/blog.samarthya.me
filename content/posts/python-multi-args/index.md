---
title: "Python: Multi-Args"
date: "2023-01-31T12:00:00Z"
slug: "python-multi-args"
description: "In Python, you can define a function with a variable number of arguments using the  and  syntax in the function definition."
categories: ["technical"]
tags: ["python"]
aliases: ["/wps/2023/01/31/python-multi-args/"]
recovered: "Internet Archive snapshot 2026-06-10"
---

In Python, you can define a function with a variable number of arguments using the `*` and `**` syntax in the function definition.

A single asterisk `*` in the function definition is used to capture positional arguments passed to the function as a tuple.

Here’s an example:

```text
def foo(*args):
    for arg in args:
        print(arg)

foo(1, 2, 3)
# Output:
# 1
# 2
# 3
```

In this example, `foo` is defined to accept a variable number of positional arguments. The single asterisk `*` in the function definition `def foo(*args)` tells Python to capture any positional arguments passed to the function as a tuple `args`. When you call `foo(1, 2, 3)`, the arguments `1`, `2`, and `3` are captured as a tuple `(1, 2, 3)` and passed to the function as `args`.

Double asterisks `**` in the function definition are used to capture keyword arguments passed to the function as a dictionary.

Here’s an example:

```text
def bar(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

bar(a=1, b=2, c=3)
# Output:
# a: 1
# b: 2
# c: 3
```

In the example above, `bar` is defined to accept a variable number of keyword arguments.

The double asterisks `**` in the function definition

```text
def bar(**kwargs)
```

tells Python to capture any keyword arguments passed to the function as a dictionary `kwargs`. When you call `bar(a=1, b=2, c=3)`, the keyword arguments `a=1`, `b=2`, and `c=3` are captured as a dictionary `{'a': 1, 'b': 2, 'c': 3}` and passed to the function as `kwargs`.
