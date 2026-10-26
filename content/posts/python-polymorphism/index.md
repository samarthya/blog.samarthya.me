---
title: "Python: Polymorphism"
date: "2023-02-02T12:00:00Z"
slug: "python-polymorphism"
description: "Polymorphism is a key feature of Object Oriented Programming that allows objects of different classes to be treated as objects of a common class."
categories: ["technical"]
tags: ["polymorphism", "python"]
aliases: ["/wps/2023/02/02/python-polymorphism/"]
recovered: "Internet Archive snapshot 2026-05-18"
---

*[image unavailable: pypoly.png]*

Polymorphism is a key feature of Object Oriented Programming that allows objects of different classes to be treated as objects of a common class. It is done by implementing the same methods across all classes and making use of inheritance, interfaces and overloading.

The basic idea behind polymorphism is to allow an object to be used in multiple ways. In Python, polymorphism is achieved through the use of methods and inheritance. This means that classes can be created to represent objects of different types and the same method can be called on those objects and it will work differently depending on the object it is called on.

For example, consider a base class ‘Shape’ with a method ‘area’. This method can be implemented differently in subclasses ‘Rectangle’, ‘Triangle’ and ‘Circle’. When we call the method ‘area’ on an object of the subclass, the implementation specific to that subclass will be executed. This is an example of polymorphism, where the same method ‘area’ is behaving differently for different objects.

Another example of polymorphism in Python can be found in the use of operator overloading. In Python, the ‘+’ operator can be overloaded to perform different operations depending on the types of the operands. For instance, when the operands are integers, the ‘+’ operator performs arithmetic addition. However, when the operands are strings, the ‘+’ operator concatenates the strings.

In **conclusion**, polymorphism is a powerful feature in Python that allows us to write flexible and reusable code. By implementing the same methods across different classes and using inheritance, interfaces and overloading, we can write code that can be used in different ways for different objects. This makes our code more maintainable and easier to understand.

## Example

In this example, the `make_sound` method is defined in both the `Dog` and `Cat` classes. The `make_animals_sound` function takes a list of `Animal` objects and prints the sound they make using the `make_sound` method. The `Dog` and `Cat` objects can be treated as `Animal` objects because they inherit from the `Animal` class. This allows the `make_animals_sound` function to handle objects of different classes in a polymorphic way.

```text
class Animal:
    def make_sound(self):
        pass

class Dog(Animal):
    def make_sound(self):
        return "Bark"

class Cat(Animal):
    def make_sound(self):
        return "Meow"

def make_animals_sound(animals):
    for animal in animals:
        print(animal.make_sound())

animals = [Dog(), Cat()]
make_animals_sound(animals)

# Output:
# Bark
# Meow
```
