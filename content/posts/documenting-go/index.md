---
title: "Documenting GO"
date: "2021-12-28"
slug: "documenting-go"
categories: ["technical"]
aliases: ["/wps/2021/12/28/documenting-go/", "/wps/2026/10/23/documenting-go/"]
wp_id: 1858
---

Documentation is a huge part of writing any software. In java you have `JavaDoc`, which most of the developers adhere to. It is healthy and rich way of exposing the source documentation.

{{< lead >}}
You spend more time reading source code than writing it, and hence it is critical to do the documentation properly.
— - Ask any engineer
{{< /lead >}}

`GoDoc` is conceptually related to `Docstring` and `Javadoc` but is simpler.

{{< lead >}}
Godoc comments are just good comments, the sort you would want to read even if godoc didn’t exist.
— - Official godocblog
{{< /lead >}}

## Convention

To document a type, variable, constant, function, or even a package, write a regular comment directly preceding its declaration, with no intervening blank line.

godoc
