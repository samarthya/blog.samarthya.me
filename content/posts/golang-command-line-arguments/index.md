---
title: "GoLang: Command line arguments"
date: "2021-01-27T17:06:11Z"
slug: "golang-command-line-arguments"
categories: ["golang", "technical"]
tags: ["commandline"]
aliases: ["/wps/2021/01/27/golang-command-line-arguments/"]
wp_id: 1280
---

Reading the golang official documentation is fun, today I saw the `Variables` in package `os`

{{< lead >}}
var Args [][string](https://golang.org/pkg/builtin/#string)
{{< /lead >}}

It allows you to hold command line arguments and a simple main program that can help you validate this.

```text
func main() {
	if len(os.Args) > 0 {
		fmt.Println(" More than one argument found: " + fmt.Sprintf("%s", os.Args[1:]))
	} else {
		fmt.Println(" No arguments passed ")
	}
}
```

### go run main 1 2 3 4

```text
More than one argument found: [1 2 3 4]
```

### Why I used `os.Args[1:]`

The argument `0` is the location of the exe itself in my case

```text
/var/folders/ry/xrnmhhjx5_sdyq4mv8dk54s00000gn/T/go-build749979406/b001/exe/main
```
