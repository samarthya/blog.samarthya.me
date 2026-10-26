---
title: "Python: Class"
date: "2023-01-31T12:00:00Z"
slug: "python-class"
description: "Learning to write Python code? A Python class is a blueprint for creating objects."
categories: ["technical"]
tags: ["python"]
aliases: ["/wps/2023/01/31/python-class/"]
recovered: "Internet Archive snapshot 2026-03-12"
---

Learning to write Python code? A Python class is a blueprint for creating objects.

It defines a set of attributes and methods that can be used to manipulate those attributes. Here’s an example of a simple Python class:

```text
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print("Woof!")
```

The `class` keyword is used to define a new class. The name of the class is `Dog`.

The `__init__` method is a special method in Python that is used to initialize an object when it is created. The `self` parameter refers to the instance of the object being created.

The `name` and `breed` attributes are created within the `__init__` method and can be accessed using the `self` reference.

The `bark` method is an example of a custom method in the class. It can be called on an instance of the `Dog` class to print “Woof!”.

To create an instance of the class, you can use the following code:

```text
dog = Dog("Fido", "Labrador")
dog.bark()
# Output: Woof!
```

This creates a new instance of the `Dog` class, with the `name` attribute set to “Fido” and the `breed` attribute set to “Labrador”.

The `bark` method is then called on the `dog` instance to produce the output “Woof!”.
