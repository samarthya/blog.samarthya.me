---
title: "CSS continued"
date: "2019-03-15T12:00:00Z"
slug: "css-continued"
description: "State dependent styling, e.g Style a checkbox when it is in checked state. It is usually denoted by a preceding colon ‘:’ (without the quote)."
categories: ["personal"]
aliases: ["/wps/2019/03/15/css-continued/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

# Pseudo classes

State dependent styling, e.g Style a checkbox when it is in checked state. It is usually denoted by a preceding colon ‘:’ (without the quote).

> :active  
> :checked  
> :default  
> :dir  
> :disabled  
> :empty

E.g.

> <div id=”myDiv”> <a href=#> Dummy link</a> </div>

Styling

> <style>  
> div {  
> background: cyan;  
> margin: 15px 0px 15px 25px;  
> border: 0px;  
> }
>
> div:focus {  
> border: 1px;  
> }  
> a {  
> text-decoration: none;  
> color: red;  
> }
>
> a:visited {  
> color: rosybrown;  
> }
>
> a:hover {  
> color: green;  
> text-decoration: overline;  
> }  
> </style>

## Pseudo elements

Keywords denoted by two colons (::) specified at the end of selector.

I am trying to add the URL information after the Anchor content.

> div id=”myDiv”> <a href=”http://www.yahoo.com”> Dummy link</a> </div>

Using the style and the pseudo element ::after

> a::after {  
> content: ” (” attr(href) “)”;  
> }

Brings the desired result

![Dummy link](screenshot-2019-03-15-at-2.31.28-pm.png)
