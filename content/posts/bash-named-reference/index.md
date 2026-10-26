---
title: "Bash: Named Reference"
date: "2022-03-02T12:00:00Z"
slug: "bash-named-reference"
description: "Bash is different world. Powerful, simple, elegant and complex all at the same time."
categories: ["technical"]
tags: ["bash", "indirect", "linux", "nameref"]
aliases: ["/wps/2022/03/02/bash-named-reference/"]
recovered: "Internet Archive snapshot 2026-04-21"
---

Bash is different world. Powerful, simple, elegant and complex all at the same time. Recently while trying to reduce the burden of repetitive code, I was trying to check what can be done to use references in Bash (something like pointers) and it was an interesting problem that I enjoyed solving.

> 💬 The ‘`$`’ character introduces parameter expansion, command substitution, or arithmetic expansion. The parameter name or symbol to be expanded may be enclosed in braces, which are optional but serve to protect the variable to be expanded from characters immediately following it which could be interpreted as part of the name.

## `declare -n <name>`

In bash version 5.1.8 (`bash --version`) I could see that you can utilize the `local -n` or `declare -n` to help you define a named reference but in the version before like `4.2.46` there was no support for named reference

```text
> bash --version
GNU bash, version 4.2.46(2)-release (x86_64-redhat-linux-gnu)
Copyright (C) 2011 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

```text
declare: declare [-aAfFgilrtux] [-p] [name[=value] ...]
    Set variable values and attributes.
    
    Declare variables and give them attributes.  If no NAMEs are given,
    display the attributes and values of all variables.
    
    Options:
      -f	restrict action or display to function names and definitions
      -F	restrict display to function names only (plus line number and
    	source file when debugging)
      -g	create global variables when used in a shell function; otherwise
    	ignored
      -p	display the attributes and value of each NAME
    
    Options which set attributes:
      -a	to make NAMEs indexed arrays (if supported)
      -A	to make NAMEs associative arrays (if supported)
      -i	to make NAMEs have the `integer' attribute
      -l	to convert NAMEs to lower case on assignment
      -r	to make NAMEs readonly
      -t	to make NAMEs have the `trace' attribute
      -u	to convert NAMEs to upper case on assignment
      -x	to make NAMEs export
    
    Using `+' instead of `-' turns off the given attribute.
    
    Variables with the integer attribute have arithmetic evaluation (see
    the `let' command) performed when the variable is assigned a value.
    
    When used in a function, `declare' makes NAMEs local, as with the `local'
    command.  The `-g' option suppresses this behavior.
    
    Exit Status:
    Returns success unless an invalid option is supplied or an error occurs.
```

## Example of `-n`

I defined a function set\_var that takes one argument ( a variable name) and sets the value to ‘`NewValue`‘ as shown below.

> 💬 A variable can be assigned the nameref attribute using the `-n` option to the `declare` or `local` builtin commands (see [Bash Builtins](https://www.gnu.org/software/bash/manual/bash.html#Bash-Builtins)) to create a nameref, or a reference to another variable.

```text
#!/bin/bash

function set_var {
    local -n myVar=$1
    echo " before: $myVar"
    myVar="New Value"
    echo " After: ${myVar}"
}

(( $# < 1 )) && (echo " Usage: ${0##*/} <any value>")  && exit 1;
OLDVALUE=$1
echo " Before function invoke: OLDVALUE := ${OLDVALUE}"
echo " Invoking the function change"
set_var OLDVALUE
echo " After function invoke: OLDVALUE := ${OLDVALUE}"
```

## Example of without `-n`

If I use the code above in the older bash version where `-n` is not supported.

```text
> ./script.sh old
 Before function invoke: OLDVALUE := old
 Invoking the function change
./script.sh: line 4: local: -n: invalid option
local: usage: local [option] name[=value] ...
 before: 
 After: New Value
 After function invoke: OLDVALUE := old
```

The basic form of parameter expansion is ${parameter}.

> 💬 If the first character of parameter is an exclamation point (!), and parameter is not a nameref, it introduces a level of indirection.

> 💬 Read more about it in the official documentation [here](https://www.gnu.org/software/bash/manual/bash.html)

Let’s improvise and see what we can do

```text
#!/bin/bash

function set_var {
    local myVar=$1
    echo " before: ${!myVar}"
    eval $myVar='abcdef'
    echo " After: ${!myVar}"
}

(( $# < 1 )) && (echo " Usage: ${0##*/} <any value>")  && exit 1;
echo " Parameter:  $*"
OLDVALUE=$1
echo " Before function invoke: OLDVALUE := ${OLDVALUE}"
echo " Invoking the function change"
set_var OLDVALUE
echo " After function invoke: OLDVALUE := ${OLDVALUE}"
```

> 💬 Indirection: The expansion `${!prefix*}` expansion, which expands to the names of all shell variables whose names begin with prefix, is available.

```text
 > ./script.sh old
 Parameter:  old
 Before function invoke: OLDVALUE := old
 Invoking the function change
 before: old
 After: abcdef
 After function invoke: OLDVALUE := abcdef
```
