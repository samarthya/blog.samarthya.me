---
title: "GOLang: Reflection"
date: "2021-01-16T08:18:34Z"
slug: "golang-reflection"
categories: ["golang", "technical"]
tags: ["go", "reflection"]
aliases: ["/wps/2021/01/16/golang-reflection/"]
wp_id: 1244
---

## Must Read

- <https://blog.golang.org/laws-of-reflection>
- <https://golang.org/pkg/reflect/>
- <https://golang.org/pkg/reflect/#Kind>
- <https://golang.org/pkg/reflect/#Value>

{{< lead >}}
Package reflect implements run-time reflection, allowing a program to manipulate objects with arbitrary types.
{{< /lead >}}

Reflection is a way to examine own structure. Let's try and learn it via examples.

```text
func main() {
	//exampleOne()
	i := 0
	fmt.Println(reflect.TypeOf(i))
	fmt.Println(reflect.ValueOf(i))
}
```

Here I have defined a variable `i := 0` and inspecting it using reflection.

```text
int
0
```

{{< lead >}}
TypeOf returns the reflection Type that represents the dynamic type of i.
{{< /lead >}}

```text
i := 0
fmt.Println(" Reflection: Int")
fmt.Println(reflect.TypeOf(i))
fmt.Println(reflect.ValueOf(i))
str := "Abc"
fmt.Println(reflect.TypeOf(str))
fmt.Println(reflect.ValueOf(str))
```

The same way it works on other type

```text
int
0
string
Abc
```

How about using a custom type instead of `int`

```text
	type MyInt int
	var myInt MyInt
	
	myInt = 0
	fmt.Println(reflect.TypeOf(myInt))
	fmt.Println(reflect.ValueOf(myInt))
```

```text
main.MyInt
0
```

Variable `i` and `myInt` have distinct static types. Underlying types are same for both of them, but we cannot assign them to each other without conversion.

```text
myInt = i
```

Any statement like that will lead to a compile time error.

> cannot use `i (type int)` as type `MyInt` in assignment

```text
i = 10
myInt = MyInt(i)
fmt.Println(reflect.TypeOf(myInt))
fmt.Println(reflect.ValueOf(myInt))
```

```text
main.MyInt
10
```

Let's define a custom type with more content and read about using the `StructField`

```text
// MyStructTags Reflect pacakge to learn more about a field.
type MyStructTags struct {
	Fi int64   `json:"intField" defines:"age"`
	Fb bool    `json:"boolField" defines:"state"`
	Ff float64 `json:"floatField" defines:"currency"`
	Fs string  `json:"stringField" defines:"name"`
}

// ReadTags Reads the tag
func ReadTags(tt MyStructTags, ix int) {
	ttType := reflect.TypeOf(tt)
	ixField := ttType.Field(ix)                                                           // getting field at a position ix
	fmt.Printf("%v:%s:%v:%v\n", ixField.Tag, ixField.Name, ixField.Offset, ixField.Type) // printing tags
}
```

```text
myRef := ref.MyStructTags{1, false, 1.52, "What is my name?"}

for i = 0; i < 4; i++ {
	ref.ReadTags(myRef, i)
}
```

The output is as under

```text
json:"intField" defines:"age":Fi:0:int64
json:"boolField" defines:"state":Fb:8:bool
json:"floatField" defines:"currency":Ff:16:float64
json:"stringField" defines:"name":Fs:24:string
```

Looking at the documentation for the `SructField`

```text
type StructField struct {
    // Name is the field name.
    Name string
    // PkgPath is the package path that qualifies a lower case (unexported)
    // field name. It is empty for upper case (exported) field names.
    // See https://golang.org/ref/spec#Uniqueness_of_identifiers
    PkgPath string

    Type      Type      // field type
    Tag       StructTag // field tag string
    Offset    uintptr   // offset within struct, in bytes
    Index     []int     // index sequence for Type.FieldByIndex
    Anonymous bool      // is an embedded field
}
```

## Setting Values

How about setting the value of the field?

```text
type MyInt int
var myInt MyInt

reflect.ValueOf(myInt).SetInt(22)
```

{{< lead >}}
reflect: reflect.flag.mustBeAssignable using unaddressable value
{{< /lead >}}

{{< lead >}}
*Settability* is a property of a reflection Value, and not all reflection Values have it.
{{< /lead >}}

```text
if reflect.ValueOf(myInt).CanSet() {
	reflect.ValueOf(myInt).SetInt(22)
}else {
	fmt.Println(" CanSet returned false")
}
```

We will use `Elem` to set the value

{{< lead >}}
Elem returns the value that the interface v contains or that the pointer v points to. It panics if v's Kind is not Interface or Ptr. It returns the zero Value if v is nil.
{{< /lead >}}

```text
fmt.Println(reflect.ValueOf(&myInt).Kind())
fmt.Println(reflect.ValueOf(&myInt).Elem().CanSet())
reflect.ValueOf(&myInt).Elem().SetInt(24)
fmt.Println(reflect.ValueOf(myInt).Interface())
```

```text
ptr
true
24
```
