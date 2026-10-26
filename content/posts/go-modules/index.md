---
title: "Go Modules"
date: "2022-07-07T12:00:00Z"
slug: "go-modules"
description: "If you are like me and getting errors while trying to compile your go lang code without having a go.mod in v1.18"
categories: ["golang", "technical"]
aliases: ["/wps/2022/07/07/go-modules/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

If you are like me and getting errors while trying to compile your go lang code without having a `go.mod` in `v1.18`

```text
package src is not in GOROOT (/usr/local/Cellar/go/1.18.3/libexec/src/src)
```

Remember you have overlooked a basic change that happened post `1.16`

**Module Aware Mode**

The `go` command now builds packages in module-aware mode by default, even when no `go.mod` is present.

{{< lead >}}
[Helpful Link](https://go.dev/blog/go116-module-changes)
— https://go.dev/blog/go116-module-changes
{{< /lead >}}

```text
> go env|grep GO111
GO111MODULE=""
```

Set it off

```text
go env -w GO111MODULE=off
```

Try again

```text
go test
PASS
ok      _/Users/samarthya/sourcebox/github.com/git.golang/project-one/src        0.099s
```

> 💬 You can also set `GO111MODULE` to `auto` to enable module-aware mode only when a go.mod file is present in the current directory or any parent directory.
> 
> **`go env -w GO111MODULE=auto`**
