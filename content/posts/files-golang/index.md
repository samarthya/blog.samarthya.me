---
title: "Files: GoLang"
date: "2021-01-21T17:26:56Z"
slug: "files-golang"
categories: ["golang", "technical"]
tags: ["files"]
aliases: ["/wps/2021/01/21/files-golang/"]
wp_id: 1259
---

Learning a new syntax and the libraries is always a task, and the only way forward is gradual. In this blog I will try to create a small program to read a text file and will keep updating the program to include more sophistication

{{< lead >}}
I will not talk about packages, code organization. If required please look at my previous blogs which cover them in detail.
{{< /lead >}}

## Code: File

I will give you the complete code and then explain what all I have done

```text
package files

import (
	"bufio"
	"fmt"
	"io"
	"log"
	"os"
)

func message(m string) {
	log.Printf(" FILES: %s", m)
}

// ReadFile reads the file and dump contents
func ReadFile(fn string) {
	message("ReadFile Invoked")
	fh, err := os.OpenFile(fn, os.O_RDONLY, 0666)

	if err != nil {
		message(" Unable to open file " + fn)
		os.Exit(1)
	}

	defer fh.Close()
	defer message(" Closing the handle")

	fr := bufio.NewReader(fh)
	for {
		li, err := fr.ReadString('\n')
		if err == nil {
			fmt.Printf(" ><: %s", li)
			continue
		} else if err == io.EOF {
			fmt.Println(" --- End of File ---")
			break
		}
		fmt.Println(" Error:", err)
		break

	}

}
```

## Step 1: Define the package

I keep the logic separate form the `main` package as a habit, and continuing the trend; I define a package `files` here.

```text
package files
```

`imports` will be explained later, but lets define a helper function - `message`.

## Step 2: Function `message`

```text
func message(m string) {
	log.Printf(" FILES: %s", m)
}
```

The primary purpose of this is printing a debug message with a predefined prefix `FILES:`

### Example

```text
2021/01/21 18:46:30  FILES: ReadFile Invoked
```

## Step 3: Function `ReadFile`

Let's write the function that will read the actual file which will be passed as an argument.

> Invoking this function is as easy as importing the `package` and calling `files.ReadFile`

### Arguments: fn - `FileName`

The `ReadFile` shall take an argument the `file-name` that needs to be read for contents. The objective of this function is simple - Dump everything on the STDOUT.

### package `os` - [Link](https://golang.org/pkg/os/)

Package `os` allows a platform independent interface to Operating System functionality and hence the name O.S.

### Function - [OpenFile](https://golang.org/pkg/os/#OpenFile)

The primary function we will be using the `OpenFile`. It opens the specified name with the specified flags.

```text
fh, err := os.OpenFile(fn, os.O_RDONLY, 0666)
```

The official documentation defines the signature of the function as

```text
func OpenFile(name string, flag int, perm FileMode) (*File, error)
```

Returning the FileHandle - `fh` and in case of error `err`.

More about the `File` can be found [here](https://golang.org/src/os/types.go?s=369:411#L6).

Check for error which can indicate file open was failure.

```text
if err != nil {
	message(" Unable to open file " + fn)
	os.Exit(1)
}
```

### Example: `readme1.txt`

In case the file doesn't exists the error message as below can be seen

```text
2021/01/21 22:45:04  FILES:  Unable to open file readme1.txt
```

A deferred call to [close](https://golang.org/pkg/os/#File.Close) the file. Which shall render the `fh` useless for `io` operation.

```text
defer fh.Close()
defer message(" Closing the handle")
```

### ReadContents: BufferedReader

After opening the file it is time to read the contents, for this we will use a `bufio` package.

#### [NewReader](https://golang.org/pkg/bufio/#NewReader)

Using the filehandle - `fh` lets create a reader `fr`.

```text
fr := bufio.NewReader(fh)
```

Ideally you should check for `nil` before you proceed to reading the contents. I am using the `ReadString` from the reader.

```text
func (b *Reader) ReadString(delim byte) (string, error)
```

It will read till the occurrence of the first newline (delimiter)

```text
li, err := fr.ReadString('\n')
```

rest of the code is quite simple that processes

- Checking error for the invocation of `ReadString`
- If no error - dump the contents on stdout
- In case of error check if it is `EOF`
- Else, show the nature of error and break out of the `for` loop.

```text
if err == nil {
	fmt.Printf(" ><: %s", li)
	continue
} else if err == io.EOF {
	fmt.Println(" --- End of File ---")
	break
}
fmt.Println(" Error:", err)
break
```

## -- THE END --
