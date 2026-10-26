---
title: "GoLang: encoding"
date: "2021-01-30T12:00:00Z"
slug: "golang-encoding"
description: "Package encoding provide capabilities to convert data to and from byte-level and textual representations."
categories: ["golang", "technical"]
tags: ["encoding", "gob", "golang"]
aliases: ["/wps/2021/01/30/golang-encoding/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

Package encoding provide capabilities to convert data to and from byte-level and textual representations.

- encoding/gob
- encoding/json, and
- encoding/xml

{{< lead >}}
The *gob* is Go’s format for *serializing* and *deserializing*. The gob was tailored for communicating between two servers written in Go.
{{< /lead >}}

- Only exported fields are encoded; zero values are not taken into account

{{< lead >}}
Package gob manages streams of gobs – binary values exchanged between an Encoder (transmitter) and a Decoder (receiver).
{{< /lead >}}

## Format GoB

Let’s create a simple Type `Blog` and we will encode and decode it using the gob format.

- https://golang.org/pkg/encoding/gob/#NewEncoder
- https://golang.org/pkg/encoding/gob/#Encoder.Encode

```text
package enc

import (
	"encoding/gob"
	"flag"
	"fmt"
	"log"
	"os"
)

// Blog blog structure
type Blog struct {
	Title, Author, Category string
	Length                  int
}

func (b *Blog) String() string {
	return fmt.Sprintf(" Blog: %s @ %s\n Category: %s\n Length: %d", b.Title, b.Author, b.Category, b.Length)
}

var fileName string
var logger = log.New(os.Stdout, " ENC: ", log.LUTC)

func init() {
	flag.StringVar(&fileName, "f", "", "Output/Input file")
	flag.Parse()
}

const (
	//ErrorMessage For the errors
	ErrorMessage = "need a file to write or read the contents."
)

var defBlog = Blog{Title: "My first blog", Author: "Samarthya", Category: "technical", Length: 200}

// Cmd main entry method
func Cmd() {
	if flag.NFlag() == 0 {
		flag.PrintDefaults()
		logger.Fatalf("%s", ErrorMessage)
	}

	f, err := os.OpenFile(fileName, os.O_CREATE|os.O_RDWR, 0666)

	defer f.Close()

	if err != nil {
		logger.Fatalf("%s", err.Error())
		os.Exit(1)
	}

	enc := gob.NewEncoder(f)
	err = enc.Encode(&defBlog)
	if err != nil {
		logger.Fatalf("%s", err.Error())
		os.Exit(1)
	}

	dec := gob.NewDecoder(f)
	var blogR Blog

	f.Seek(0,0)
	err = dec.Decode(&blogR)
	if err != nil {
		logger.Fatalf("%s", err.Error())
		os.Exit(1)
	}

	fmt.Printf(" Read: %s\n", blogR.String())
	fmt.Println(" --- End Program -- ")
}
```

```text
./main -f abc.txt
 Read:  Blog: My first blog @ Samarthya
 Category: technical
 Length: 200
 --- End Program --
```
