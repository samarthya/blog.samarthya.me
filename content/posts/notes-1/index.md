---
title: "Notes: For self"
date: "2022-02-23T07:27:42Z"
slug: "notes-1"
description: "Personal notes on Bash: arithmetic, = versus ==, single versus double brackets, and the bc calculator."
categories: ["technical"]
tags: ["bash", "linux", "notes"]
aliases: ["/wps/2022/02/23/notes-1/"]
wp_id: 2156
---

{{< tabs >}}

{{< tab label="bash" >}}

- Bash is a string oriented language
- We do not write `step=$((step++))` this expression will return a numeric value which the shell will then take as the command to to be executed.
- No spaces are allowed around the equal sign for variable assignment.
- `let "step++"` is same as `(( step++ ))`
- Use `declare` to set variable values and attributes

{{< /tab >}}

{{< tab label="= & ==" >}}

In bash `=` and `==` both mean the same thing

{{< /tab >}}

{{< tab label="Brackets [" >}}

> 💬 What is the difference between `[` and `[[`?

{{< steps >}}

{{< step title="if cd $dir; then" >}}

In this case the command `cd $dir` will be executed and based on success or failure of the command executed the if or else part will be executed respectively.

### `if [$dir]; then`

Single bracket is equivalent to test command evaluate conditional expression

{{< steps >}}

{{< step title="< & >" >}}

- Within `[` compare using simple ASCII ordering & within `[[` comparison is lexicographic.
- Within `[` you have to escape `\>` to avoid redirection.

{{< /step >}}

{{< /steps >}}

{{< /step >}}

{{< /steps >}}

{{< /tab >}}

{{< tab label="bc" >}}

> 💬 BC is a language?

{{< accordion >}}

{{< accordionItem title="" >}}

{{< /accordionItem >}}

{{< /accordion >}}

> 💬 Supports arbitrary precision numbers with interactive execution of statements. (Command line)

{{< /tab >}}

{{< tab label="awk" >}}

`awk` provides filtering capabilities

```text
> printf 'gate\napple\nwhat\nkite\n' | awk '/at/'

gate
what
```

```text
printf 'gate\napple\nwhat\nkite\n' | awk '!/e/'

what
```

`awk` is primarily used for field based processing

One liner structure `awk 'cond1{action1} cond2{action2} … condN{actionN}'`

{{< /tab >}}

{{< /tabs >}}
