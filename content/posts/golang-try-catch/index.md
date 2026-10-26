---
title: "GoLang: try-catch"
date: "2021-02-22T12:00:00Z"
slug: "golang-try-catch"
description: "GoLang doesn’t have a try and catch like the popular C++ or Java languages, what it has is panic-recover."
categories: ["golang", "technical"]
tags: ["defer", "golang", "panic", "recover", "try-catch"]
aliases: ["/wps/2021/02/22/golang-try-catch/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

GoLang doesn’t have a try and catch like the popular C++ or Java languages, what it has is `panic-recover`.

Non critical errors are returned as normal values and for the critical ones, `panic` is used

```text
func myFunc(myvalue string) (string, error)
```

## Creating Error

- `errors.New()`
- `fmt.Errorf()`

```text
func throwError() (string, error) {
	return "", fmt.Errorf("I am an simple error")
}

func main() {
	_, err := throwError()

	if err != nil {
		fmt.Println(" catch error...." + err.Error())
	}
}
```

```text
catch error....I am an simple error
```

## Recover

**Recover** is a built-in function that allows the regain of control from a panicking goroutine. For the normal flow of execution, a call to recover will return `nil` and will have no effect.

For a panicking `gomodule`, call to recover will capture the value given to panic and **resume normal execution**.

{{< lead >}}
**Recover is only useful inside deferred functions.**
{{< /lead >}}

```text
func throwPanic() {
	fmt.Println("I will throw panic after few seconds.")
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf(" Caught Panic: %v\n", r)
		}
	}()
	panic(fmt.Errorf("%s", "Panic has struck...."))
}

func main() {
	fmt.Println("main function")
	throwPanic()
	fmt.Println("I will now print...")
}
```

```text
main function
I will throw panic after few seconds.
 Caught Panic: Panic has struck....
I will now print...
```

You can now see that in function `throwPanic()` we have defined a `deferred` function invocation in which the recover function will be invoked to see what error has happened and finally the normal flow resumes and hence the “`I will now print`” is returned.

## Help

- <https://blog.golang.org/defer-panic-and-recover>
