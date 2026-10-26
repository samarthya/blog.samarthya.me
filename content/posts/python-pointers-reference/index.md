---
title: "Python: Pointers & Reference"
date: "2023-01-31T12:00:00Z"
slug: "python-pointers-reference"
description: "In Python, there are no explicit pointers like in some other programming languages. In python everything is an object and references to objects are stored in variables."
categories: ["technical"]
tags: ["pointers", "python", "reference"]
aliases: ["/wps/2023/01/31/python-pointers-reference/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

In Python, there are no explicit pointers like in some other programming languages. In python everything is an object and references to objects are stored in variables.

When you assign an object to a variable, the variable stores a reference to the object in memory. This means that changes to the object will be reflected in all variables that reference that object.

Here’s an example that demonstrates how references work in Python:

```text
a = [1, 2, 3]
b = a
b[1] = 4

print(a)
# Output: [1, 4, 3]
```

In the example above

1. `a` is assigned a reference to a list object `[1, 2, 3]`.
2. Then `b` is assigned a reference to the same list object as `a`.

When you change the value of `b[1]` to `4`, the change is reflected in the original list object, which is referenced by `a`. When you print `a`, the output is `[1, 4, 3]`, which shows that the change to `b` also affected `a`.

This demonstrates that in Python, variables store references to objects, not the objects themselves. When you modify an object, all references to that object will see the changes.

If you want to create a copy of an object that is independent from the original object, you need to use the `copy` module.
