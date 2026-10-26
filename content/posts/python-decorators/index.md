---
title: "Python: Decorators"
date: "2023-01-31T12:00:00Z"
slug: "python-decorators"
description: "Let’s learn about decorators @iamdecorator"
categories: ["technical"]
tags: ["decorators", "python"]
aliases: ["/wps/2023/01/31/python-decorators/"]
recovered: "Internet Archive snapshot 2026-04-21"
---

Let’s learn about decorators `@iamdecorator`

Decorators are used to modify or extend the behavior of functions and classes. They are useful for wrapping a function or class with additional functionality, such as logging, access control, performance measurement, or adding attributes. This can reduce code duplication, increase readability and maintainability.

Decorators in Python are a way to modify or extend the behavior of a function, class, or method without changing their source code.

They are implemented as special types of functions that can take another function or class as an argument, add or change its behavior, and then return the modified function or class

Decorators are indicated with the “@” symbol in front of the function or class definition.

## Example

```text
def logging_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Running {func.__name__} with args: {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result
    return wrapper

@logging_decorator
def add(a, b):
    return a + b

print(add(3, 4))
```

Output

```text
Running add with args: (3, 4), {}
add returned: 7
7
```
