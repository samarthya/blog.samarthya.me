---
title: "House that Jack built."
date: "2020-01-17T12:00:00Z"
slug: "house-that-jack-built"
description: "Funny thing about simple programs is that there are too many optimization options available that never lets you feel content."
categories: ["others", "technical"]
tags: ["fprintf", "golang", "strings", "struct", "types"]
aliases: ["/wps/2020/01/17/house-that-jack-built/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

Funny thing about simple programs is that there are too many optimization options available that never lets you feel content.

So here I am trying to solve another problem from [exercism.io](https://exercism.io/my/solutions/19fb3977b3be4ff4bedfee14c711af1a) which is totally a must visit for anyone who wants to learn and practice.

> Nursery rhyme

I wrote a couple of version before trying to improvise in a different way what soothes the undying thirst of improving that something, which is still not right.

> Beauty lies in the eyes of beholder!
>
> Funny context though

It is still not the best `version`, but has brought some peace to my vacillating mind.

### The Rhyme

```text
This is the house that Jack built.

This is the malt
that lay in the house that Jack built.

This is the rat
that ate the malt
that lay in the house that Jack built.

This is the cat
that killed the rat
that ate the malt
that lay in the house that Jack built.

This is the dog
that worried the cat
that killed the rat
that ate the malt
that lay in the house that Jack built.

This is the cow with the crumpled horn
that tossed the dog
that worried the cat
that killed the rat
that ate the malt
that lay in the house that Jack built.

This is the maiden all forlorn
that milked the cow with the crumpled horn
that tossed the dog
that worried the cat
that killed the rat
that ate the malt
that lay in the house that Jack built.

This is the man all tattered and torn
that kissed the maiden all forlorn
that milked the cow with the crumpled horn
that tossed the dog
that worried the cat
that killed the rat
that ate the malt
that lay in the house that Jack built.

This is the priest all shaven and shorn
that married the man all tattered and torn
that kissed the maiden all forlorn
that milked the cow with the crumpled horn
that tossed the dog
that worried the cat
that killed the rat
that ate the malt
that lay in the house that Jack built.

This is the rooster that crowed in the morn
that woke the priest all shaven and shorn
that married the man all tattered and torn
that kissed the maiden all forlorn
that milked the cow with the crumpled horn
that tossed the dog
that worried the cat
that killed the rat
that ate the malt
that lay in the house that Jack built.

This is the farmer sowing his corn
that kept the rooster that crowed in the morn
that woke the priest all shaven and shorn
that married the man all tattered and torn
that kissed the maiden all forlorn
that milked the cow with the crumpled horn
that tossed the dog
that worried the cat
that killed the rat
that ate the malt
that lay in the house that Jack built.

This is the horse and the hound and the horn
that belonged to the farmer sowing his corn
that kept the rooster that crowed in the morn
that woke the priest all shaven and shorn
that married the man all tattered and torn
that kissed the maiden all forlorn
that milked the cow with the crumpled horn
that tossed the dog
that worried the cat
that killed the rat
that ate the malt
that lay in the house that Jack built.
```

## Logic building

The obvious question I had in mind was, what can help me break it in a way that it has a meaningful structure.

### Grammar to the rescue

The subject is the “who” or “what” of the sentence, the predicate is the verb, and the object is any noun or concept that is part of the action of the subject.

> Subject, predicate, and objects are the three different components when breaking down a sentence.

This helped me define a structure that I though will help me solve the poem into smaller chunks for each para.

```text
type Predicate struct {
    character string
    predicate string
}

type Character struct {
    adjective string
    pred      Predicate
}
```

```text
Example: This is the house that Jack built.
```

In this I was able to Identify `house` as the `Character` (Subject) and `built` is the `action` or `predicate` and Jack is the `character` embedded in predicate who took the action.

Using this as a building block I initialized two maps.

```text
var verses map[int]string = map[int]string{
    1: "house",
    2: "malt",
    3: "rat",
    4: "cat",
    5: "dog",
    6: "cow", 
    7: "maiden",
    8: "man", 
    9: "priest",
    10: "rooster", 
    11: "farmer",
    12: "horse",
}

var characters map[string]Character = map[string]Character{
    "house": {adjective: "", pred: Predicate{
        predicate: "built.", character: "Jack",
    },
    },
    "malt": {adjective: "", pred: Predicate{
        predicate: "lay in the", character: "house",
    },
    },
    "rat": {adjective: "", pred: Predicate{
        predicate: "ate the", character: "malt",
    },
    },
    "cat": {adjective: "", pred: Predicate{
        predicate: "killed the", character: "rat",
    },
    },
    "dog": {adjective: "", pred: Predicate{
        predicate: "worried the", character: "cat",
    },
    },
    "cow": {adjective: "with the crumpled horn", pred: Predicate{
        predicate: "tossed the", character: "dog",
    },
    },
    "maiden": {adjective: "all forlorn", pred: Predicate{
        predicate: "milked the", character: "cow",
    },
    },
    "man": {adjective: "all tattered and torn", pred: Predicate{
        predicate: "kissed the", character: "maiden",
    },
    },
    "priest": {adjective: "all shaven and shorn", pred: Predicate{
        predicate: "married the", character: "man",
    },
    },
    "rooster": {adjective: "that crowed in the morn", pred: Predicate{
        predicate: "woke the", character: "priest",
    },
    },
    "farmer": {adjective: "sowing his corn", pred: Predicate{
        predicate: "kept the", character: "rooster",
    },
    },
    "horse": {adjective: "and the hound and the horn", pred: Predicate{
        predicate: "belonged to the", character: "farmer",
    },
    },
}
```

The problem that was still wasn’t that obvious to me was some subjects had adjectives which were unassumingly borrowed when used in the predicate.

```text
Example: This is the maiden all forlorn that milked the cow with the crumpled horn
```

Now to write the function to return the verses numerically from 1 to 12, a simple stitcher which uses `fmt`‘s `Fprintf` method and `StringBuilder` from `strings`

```text
func Verse(stanza int) (verse string) {
    var v strings.Builder
    var character string
    character = verses[stanza]
    if stanza == 1 {
        fmt.Fprintf(&v, "%s %s that %s %s", This, character, characters[character].pred.character, characters[character].pred.predicate)
    } else {
        for j := stanza; j > 0; j-- {
            character = verses[j]
            predChar := characters[character].pred.character
            if j == stanza {
                if characters[character].adjective == "" {
                    fmt.Fprintf(&v, "%s %s\nthat %s %s", This, character, characters[character].pred.predicate, characters[character].pred.character)
                } else {
                    fmt.Fprintf(&v, "%s %s %s\nthat %s %s", This, character, characters[character].adjective, characters[character].pred.predicate, characters[character].pred.character)
                }
            } else if j == 1 {
                fmt.Fprintf(&v, " that %s %s", characters[character].pred.character, characters[character].pred.predicate)
            } else {
                fmt.Fprintf(&v, "\nthat %s %s", characters[character].pred.predicate, characters[character].pred.character)
            }
            if predChar != "" && characters[predChar].adjective != "" {
                fmt.Fprintf(&v, " %s", characters[predChar].adjective)
            }
        }
    }

    verse = strings.TrimSpace(v.String())
    return verse
}
```

## — THE – END —
