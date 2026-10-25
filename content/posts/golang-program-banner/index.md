---
title: "GoLang: Program Banner"
date: "2021-01-29T07:39:04Z"
slug: "golang-program-banner"
categories: ["golang", "technical"]
tags: ["banner", "flags"]
aliases: ["/wps/2021/01/29/golang-program-banner/"]
wp_id: 1284
---

In the last [blog]({{< relref "/posts/golang-command-line-arguments" >}}) I talked about command line arguments `os.Args[]`. In this I will try and create a sample banner program that shall

- Take 3 arguments
- `n` - Number of times a message has to be repeated.
- `m` - The message that needs to be shown.
- `d` - If debug message needs to be shown.

I am going to use the `flags` package.

{{< lead >}}
Source code is available [here](https://github.com/samarthya/gows)
— https://github.com/samarthya
{{< /lead >}}

## Defining: Banner

The package `flag` has the extended capability of parsing the flags.

### Define Flags

#### Variant one

```text
var times = flag.Int("n", 1, "number of times the message needs to be displayed")
var msg = flag.String("m", "", "the message that needs to be printed")
var dbg = flag.Bool("d", false, "to debug or not")
```

{{< lead >}}
A good reference available [here](https://gobyexample.com/command-line-flags).
{{< /lead >}}

You can also define flags using

```text
var nTimes int

func init() {
	flag.IntVar(&nTimes, "n", 1, "number of times the message needs to be displayed")
}
```

After all flags are defined you must call, to parse the command line into flags. If you miss this one you might not get the desired results. (Give it a try)

```text
// Must be called after all flags are defined and before flags are accessed within the program
flag.Parse()
```

How to pass values to these flags?

```text
-flag
-flag=x
-flag x
```

### Build

```text
go build src/cmdline/cmd.go
```

This will produce the binary - `cmd`.

### Run the `cmd`

```text
./cmd
  -d    to debug or not
  -m string
        the message that needs to be printed
  -n int
        number of times the message needs to be displayed (default 1)
```

```text
./cmd -n 2 -m="Why is world round?"

--- Command line Program ---

 >> Why is world round?

 >> Why is world round?
```

```text
./cmd -n 2 -m="Why is world round?" -d=true
DBG: Number of Arguments: 5
--- Command line Program ---

 >> Why is world round?

 >> Why is world round?
```

```text
./cmd -m="Why is world round?" -n=3  -d=true
DBG: Number of Arguments: 4
--- Command line Program ---

 >> Why is world round?

 >> Why is world round?

 >> Why is world round?
```
