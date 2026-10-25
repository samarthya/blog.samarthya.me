---
title: "Files: GoLang"
date: "2021-01-25T12:46:47Z"
slug: "files-golang-2"
categories: ["golang", "technical"]
tags: ["files"]
aliases: ["/wps/2021/01/25/files-golang-2/"]
wp_id: 1269
---

In the last blog, I tried [reading a file in GoLang]({{< relref "/posts/files-golang" >}}).

{{< lead >}}
My repository in GitHub has all the code that I write ([link](https://github.com/samarthya/valueandpointer))
{{< /lead >}}

Now, I will extend the same program to write to the same file.

```text
// Debug messages - Centralized logging
func message(m string) {
	log.Printf(" FILES: %s", m)
}

func fileStats(f *os.File) {
	message(" File Name: " + f.Name())

	fs, _ := f.Stat()
	message(" File Mode: " + fs.Mode().String())
	message(" Last Mode time: " + fs.ModTime().String())
	message(" File Size: " + strconv.Itoa(int(fs.Size())))
}

// WriteFile writes to the file identified by f
func WriteFile(f string, m string) {

	message("--- Write Invoked --- ")

	fh, err := os.OpenFile(f, os.O_APPEND|os.O_WRONLY, os.ModeAppend)

	if err != nil {
		message(" Unable to open file " + f)
		// Conventionally, code zero indicates success
		os.Exit(1)
	}

	defer fh.Close()
	fileStats(fh)

	message(" Writing: " + m)
	n, err := fh.WriteString("\n")
	n, err = fh.WriteString(m)
	fh.WriteString(" ----- " + string(n) + " ----- ")

	if err == nil {
		// w.Flush()
		fmt.Println(" -- Closed --")
		return
	}

	fmt.Println(" Error: " + err.Error())

}
```

## What it does?

1. Opens a file `os.OpenFile(f, os.O_APPEND|os.O_WRONLY, os.ModeAppend)`
2. WritesString mesage `m` - and captures the response `n, err = fh.WriteString(m)`; Where n is the number of bytes written and err is error if encountered.
3. Close the file handle `fh.Close()`

For my sample program the readme looks like this

```text
I am just a plain text file
I have float, int, bool and string
int: 20
float: 20.50
string: "Get some content"
bool: true
> 2021-01-25 18:01:57.48917 +0530 IST m=+0.000089785
 ----- 5 ----- 
> 2021-01-25 18:02:07.965749 +0530 IST m=+0.000071314
 ----- 6 ----- 
> 2021-01-25 18:02:10.820226 +0530 IST m=+0.000066656
 ----- 6 ----- 
> 2021-01-25 18:02:12.732445 +0530 IST m=+0.000071841
 ----- 6 ----- 
> 2021-01-25 18:02:13.782766 +0530 IST m=+0.000071555
 ----- 6 ----- 
> 2021-01-25 18:02:14.574956 +0530 IST m=+0.000085469
 ----- 6 ----- 
> 2021-01-25 18:02:15.389384 +0530 IST m=+0.000068317
 ----- 6 ----- 
> 2021-01-25 18:08:07.145537 +0530 IST m=+0.000062991
 ----- 6 ----- 
> 2021-01-25 18:08:08.814768 +0530 IST m=+0.000122495
 ----- 6 ----- 
> 2021-01-25 18:08:09.710064 +0530 IST m=+0.000092775
 ----- 6 ----- 
> 2021-01-25 18:08:10.45252 +0530 IST m=+0.000073827
 ----- 5 -----
```
