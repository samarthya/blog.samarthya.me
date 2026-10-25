---
title: "GoLang: Hex Output"
date: "2021-01-29T17:47:07Z"
slug: "golang-hex-output"
categories: ["golang", "technical"]
tags: ["files", "flags", "fmt"]
aliases: ["/wps/2021/01/29/golang-hex-output/"]
wp_id: 1293
---

In last few blogs I have written about reading `commandline` parameters reading `files` and using the `os` package.

In this blog, I will combine some these items to read a file `byte` by `byte` using the `bufio` package `func`'s.

Some of the things I am still learning while I try out different things is that how to organise the perfect folder structure to ensure what I learn is manageable to refer back when and if I revisit.

{{< alert "circle-info" >}}
Still refining, but am getting better by the day.
{{< /alert >}}

## Challenges

- Defining the flag to get the input from the command line using the `-f` flag.
- If the input is not provided the format expected should be printed.
- For a file present, read byte by byte and output `HEX:Byte` representation.

## Defining flag

```text
var fileName string

func init() {
	flag.StringVar(&fileName, "f", "", "File to read")
	flag.Parse()
}
```

Why the `flag.Parse()` is defined here in `Init()`? Before I get there let me add some details about `init` and `Parse`.

{{< lead >}}
You can read more about **init** methods [here](https://golang.org/doc/effective_go.html#init).
{{< /lead >}}

## What is Init()?

Each source file can define its own niladic (operator or function having no arguments) `init` function (one or more) to set up whatever state is required.

The function `init` is called after all the variable declarations in the package have evaluated their initializers, and those are evaluated only after all the imported packages have been initialized.

## Parse

Also Parse() must be called after all flags are defined and before flags are accessed by the program.

{{< lead >}}
Parse() (package flags) parses the command-line flags from os.Args[1:].
— Official go documentation
{{< /lead >}}

Since it is to set state and I will be calling the main processing logic from a different source file it is best to initialise the state in `init()` else the flag might not be set properly.

## Hex:Byte

The function below are quite self-explanatory

### OpenAndDump

This function is to open a file passed to it as an argument and uses `os.Open` to open the file and then a buffered reader is created to read the file byte by byte (using the method `dump`) and `fmt.Fprintf` is used to push the content to `Stdout`.

```text
//dump dumps the content from a reader
func dump(fr *bufio.Reader) {
	fmt.Println("\n -------- STARTOFFILE -------")
	for {
		b, err := fr.ReadByte()
		if err == io.EOF {
			break
		}
		fmt.Fprintf(os.Stdout, " %X:%c", b, b)
	}
	fmt.Println("\n ------ ENDOFFILE ------")
}

// OpenAndDump a file and dumps the content
func OpenAndDump(f string) {
	fh, err := os.Open(f)
	if err == nil {
		dump(bufio.NewReader(fh))
		os.Exit(0)
	}

	defer fh.Close()
	fmt.Fprintf(os.Stderr, "ERR: (%s) %s", f, err.Error())
	return
}
```

## Entry function: `Cmd()`

It does the following

- Checks for the number of flags ([NFlag](https://golang.org/pkg/flag/#NFlag)) passed, if 0 then prints the [default](https://golang.org/pkg/flag/#PrintDefaults) usage and exits with error.
- If argument `-f` is set then invoke the `OpenAndDump` method defined.

```text
const (
	// InvalidArgument for the program
	InvalidArgument = "Please provide a valid file\n"
)

// Cmd Runs the command
func Cmd() {
	// https://golang.org/pkg/flag/#NArg
	// fmt.Fprintf(os.Stdout, "DBG: %d %s\n", flag.NArg(), fileName)

	if flag.NFlag() == 0 {
		fmt.Fprintf(os.Stderr, "%s", InvalidArgument)
		flag.PrintDefaults()
		os.Exit(1)
	}

	//OpenAndDump(flag.Arg(i))
	OpenAndDump(fileName)

}
```

## Sample Output

```text
./main -f filer.txt
```

### File: filer.txt

```text
I am a sample file.
I have a new line.
I even have an int 10.
```

### Output

```text
-------- STARTOFFILE -------
 49:I 20:  61:a 6D:m 20:  61:a 20:  73:s 61:a 6D:m 70:p 6C:l 65:e 20:  66:f 69:i 6C:l 65:e 2E:. A:
 49:I 20:  68:h 61:a 76:v 65:e 20:  61:a 20:  6E:n 65:e 77:w 20:  6C:l 69:i 6E:n 65:e 2E:. A:
 49:I 20:  65:e 76:v 65:e 6E:n 20:  68:h 61:a 76:v 65:e 20:  61:a 6E:n 20:  69:i 6E:n 74:t 20:  31:1 30:0 2E:.
 ------ ENDOFFILE ------
```
