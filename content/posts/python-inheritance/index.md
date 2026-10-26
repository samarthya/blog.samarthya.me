---
title: "Python: Inheritance"
date: "2023-01-31T12:00:00Z"
slug: "python-inheritance"
description: "Inheritance is a mechanism in object-oriented programming (OOP) that allows you to create new classes that are derived from existing classes."
categories: ["technical"]
tags: ["python"]
aliases: ["/wps/2023/01/31/python-inheritance/"]
recovered: "Internet Archive snapshot 2026-04-21"
---

Inheritance is a mechanism in object-oriented programming (OOP) that allows you to create new classes that are derived from existing classes. The derived class inherits attributes and behaviors from the base class, and can also have additional attributes and behaviors of its own.

Here’s an example of inheritance in Python:

```text
class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        print("Some sound")

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def make_sound(self):
        print("Woof!")
```

In this example, the `Animal` class is the base class and the `Dog` class is the derived class. The `Dog` class inherits the `name` attribute from the `Animal` class, and also has its own `breed` attribute.

The `make_sound` method in the `Dog` class overrides the `make_sound` method in the `Animal` class. This is known as method overriding.

The `super()` function is used to call the `__init__` method of the base class, allowing the derived class to inherit the attributes and behaviors of the base class.

You can create instances of the `Dog` class just like any other class:

```text
dog = Dog("Mydo", "Belgian")
dog.make_sound()
# Output: Woof!
```

This creates a new instance of the `Dog` class, with the `name` attribute set to “Mydo” and the `breed` attribute set to “Belgian”. The `make_sound` method is then called on the `dog` instance to produce the output “Woof!”.
