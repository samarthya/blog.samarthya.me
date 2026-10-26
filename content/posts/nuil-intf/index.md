---
title: "Nil Interface"
date: "2020-01-26T12:00:00Z"
slug: "nuil-intf"
description: "An interface in Golang is a set of methods and a type."
categories: ["others", "technical"]
tags: ["interface", "nil"]
aliases: ["/wps/2020/01/26/nuil-intf/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

An interface in Golang is a set of methods and a type.

What is the purpose of Nil interface in GO-lang

> A nil interface value holds neither value nor concrete type.

```text
type NilI interface {
     NoFunction()
}
```

Just defined an interface with a simple function `NoFunction`

```text
func main() {
    NilI i
    i.NoFunction()
}
```

Executing it results in

```text
panic: runtime error: invalid memory address or nil pointer dereference
```

On the same lines there is `empty` interface, but that can hold any value; but what is nil interface suppose to do?

```text
interface{}
```

> An empty interface that specifies zero methods.

An empty interface is used for unknown types.

```text
e.g 
func Printf(format string, a ...interface{}) (n int, err error)

var i interface{}
fmt.Printf("(%v, %T)\n", i, i)

Outputs
(<nil>, <nil>)

if, we assign 
i = 42

Outputs
(42, int)
```

What if you want to evaluate the type of the object or interface?

## Type Assertion

A *type assertion* provides access to an interface value’s underlying concrete value.

> t.(type)

#### type, identifies the concrete value such as int, float etc.

The statement asserts the t holds the concrete type `type`. If t does not holds Type `type` it will throw a panic error.

```text
another syntactical sugar
s, ok := t.(type)
```

If t has a Type `type` then s will have the concrete value and `ok` will have value true, else `ok` will be false and `s` zero value of Type `type`.

```text
e.g.
var i interface{} = "simple"

s := i.(string)
fmt.Println(s)

Outputs:
simple

s, ok := i.(string)
fmt.Println(s, ok)

Outputs:
simple true

f, ok := i.(int)
fmt.Println(f, ok)

Outputs:
panic: interface conversion: interface {} is string, not float64
```

### — THE – END —
