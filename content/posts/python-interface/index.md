---
title: "Python: Interface"
date: "2023-01-31T12:00:00Z"
slug: "python-interface"
description: "n Python, unlike some other programming languages, there is no explicit syntax for defining interfaces."
categories: ["technical"]
tags: ["interface", "python"]
aliases: ["/wps/2023/01/31/python-interface/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

n Python, unlike some other programming languages, there is no explicit syntax for defining interfaces. However, you can create a similar concept by defining an abstract base class (ABC) that contains abstract methods. An abstract method is a method that is declared in a base class, but has no implementation. Subclasses of the abstract base class must implement these abstract methods.

Here’s an example:

```text
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side

square = Square(5)
print(square.area())  # 25
```

In the example above, the `Shape` class is defined as an abstract base class using the `ABC` class from the `abc` module.

The `area` method is defined as an abstract method using the `@abstractmethod` decorator. The `Square` class is a concrete implementation of the `Shape` interface, and implements the `area` method. When you create an instance of the `Square` class and call its `area` method, the implementation of the `area` method in the `Square` class is executed, and the result is returned.

{{< lead >}}
The “@” symbol in Python is used to define decorators. Decorators are a way to modify the behavior of a function, class, or method by wrapping it in another function.
— Help
{{< /lead >}}
