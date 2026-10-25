---
title: "GOLANG: Proteins & RNA"
date: "2020-02-10T15:06:21Z"
slug: "golang-proteins-rna"
categories: ["technical"]
tags: ["golang", "maps", "regexp"]
aliases: ["/wps/2020/02/10/golang-proteins-rna/"]
wp_id: 375
---

It was an interesting exercise, and I solved in three ways. More details available here @ [exercism.io](https://exercism.io/my/solutions/94b768430cb84699bcbc07605d3bbe71)

## Introduction

RNA can be broken into three nucleotide sequences called codons, and then translated to a polypeptide like so:

RNA: `"AUGUUUUCU"` => translates to

Codons: `"AUG", "UUU", "UCU"`
=> which become a polypeptide with the following sequence =>

Protein: `"Methionine", "Phenylalanine", "Serine"`

There are 64 codons which in turn correspond to 20 amino acids;
however, all of the codon sequences and resulting amino acids are not
important in this exercise. If it works for one codon, the program
should work for all of them.
However, feel free to expand the list in the test suite to include them
all.

There are also three terminating codons (also known as 'STOP'
codons); if any of these codons are encountered (by the ribosome), all
translation ends and the protein is terminated.

All subsequent codons after are ignored, like this:

RNA: `"AUGUUUUCUUAAAUG"` =>

Codons: `"AUG", "UUU", "UCU", "UAA", "AUG"` =>

Protein: `"Methionine", "Phenylalanine", "Serine"`

Note the stop codon `"UAA"` terminates the translation and the final methionine is not translated into the protein sequence.

Below are the codons and resulting Amino Acids needed for the exercise.

| Codon | Protein |
| --- | --- |
| AUG | Methionine |
| UUU, UUC | Phenylalanine |
| UUA, UUG | Leucine |
| UCU, UCC, UCA, UCG | Serine |
| UAU, UAC | Tyrosine |
| UGU, UGC | Cysteine |
| UGG | Tryptophan |
| UAA, UAG, UGA | STOP |

### Version 1.0

```text
package protein

import (
	"errors"
	"fmt"
	"strings"
)

var (
	// ErrStop stop error
	ErrStop = errors.New("STOP word has been found")
	// ErrInvalidBase invalid base
	ErrInvalidBase = errors.New("the base is invalid")
)

// FromRNA Returns proteins
func FromRNA(rna string) (out []string, err error) {
	i := 0
	out := make([]string, 0)

	if rna != "" {
		newString := rna[i:3]
		for {
			fmt.Println(" Element: ", strings.ToUpper(newString))

			prt, err := FromCodon(newString)
			if err != nil && strings.Compare(err.Error(), ErrInvalidBase.Error()) == 0 {
				return out, err
			}

			if prt == "" {
				return out, nil
			}

			out = append(out, prt)
			i += 3
			if i+3 <= len(rna) {
				newString = rna[i : i+3]
				continue
			}
			break
		}

		return out, nil
	}
	return out, ErrInvalidBase
}

// FromCodon Returns proteins
func FromCodon(codon string) (string, error) {
	if codon != "" && len(codon)%3 == 0 {
		switch strings.ToUpper(codon) {
		case "AUG":
			return "Methionine", nil
		case "UUU":
			return "Phenylalanine", nil
		case "UUC":
			return "Phenylalanine", nil

		case "UUA":
			return "Leucine", nil
		case "UUG":
			return "Leucine", nil
		case "UCU":
			return "Serine", nil
		case "UCC":
			return "Serine", nil
		case "UCA":
			return "Serine", nil
		case "UCG":
			return "Serine", nil
		case "UAU":
			return "Tyrosine", nil
		case "UAC":
			return "Tyrosine", nil
		case "UGU":
			return "Cysteine", nil
		case "UGC":
			return "Cysteine", nil
		case "UGG":
			return "Tryptophan", nil

		case "UAA":
			return "", ErrStop
		case "UAG":
			return "", ErrStop
		case "UGA":
			return "", ErrStop
		default:
			return "", ErrInvalidBase
		}
	}
	return "", ErrInvalidBase
}
```

It was the simplest possible, wherein I had two functions as expected

- `func FromCodon(codon string) (string, error)`
- `func FromRNA(rna string) ([]string, error)`

### FromCodon

It has a simple SWITCH-CASE control loop that takes in the input string and returns the corresponding `Protein`.

### FromRNA

It has a little looping to iterate through the input string and tokenize it into `codon` and return the final array.

A simple for loop is employed which creates slice of length 3 to fetch the codon for using the `FromCodon`

`newString := rna[i:3]`

```text
 i += 3
 if i+3 <= len(rna) {
 newString = rna[i : i+3]
 continue
 }
```

This loops runs through the whole length and find the corresponding proteins and returns the final array.

E.g.

- Input : "AUGUUUUAA"
- Output: []string{"Methionine", "Phenylalanine"},

## Version 2.0

The previous version was a bad optimization, so came up with the next version.

```text
var (
	// ErrStop stop error
	ErrStop = errors.New("STOP word has been found")

	// ErrInvalidBase invalid base
	ErrInvalidBase = errors.New("the base is invalid")

	// Proteins that are to mapped
	Proteins = map[string]string{
		"AUG": "Methionine",
		"UUU": "Phenylalanine",
		"UUC": "Phenylalanine",
		"UUA": "Leucine",
		"UUG": "Leucine",
		"UCU": "Serine",
		"UCC": "Serine",
		"UCA": "Serine",
		"UCG": "Serine",
		"UAU": "Tyrosine",
		"UAC": "Tyrosine",
		"UGU": "Cysteine",
		"UGC": "Cysteine",
		"UGG": "Tryptophan",
		"UAA": "STOP",
		"UAG": "STOP",
		"UGA": "STOP",
	}
)

// FromRNA Returns proteins
func FromRNA(rna string) ([]string, error) {
	i := 0
	out := make([]string, 0)

	if rna != "" {
		newString := rna[i:3]
		for {

			prt, err := FromCodon(newString)
			if err != nil && strings.Compare(err.Error(), ErrInvalidBase.Error()) == 0 {
				return out, err
			}

			if prt == "" {
				return out, nil
			}

			out = append(out, prt)
			i += 3
			if i+3 <= len(rna) {
				newString = rna[i : i+3]
				continue
			}
			break
		}

		return out, nil
	}
	return out, ErrInvalidBase
}

// FromCodon Returns proteins
func FromCodon(codon string) (string, error) {
	out := ""
	if codon != "" {

		codon = strings.ToUpper(codon)
		out = Proteins[codon]

		if strings.Compare(out, "STOP") == 0 {
			return "", ErrStop
		} else if out == "" {
			return "", ErrInvalidBase
		}
	}
	return out, nil
}
```

I did away with the Switch-Case and used Map.

Proteins = map[string]string{  
  **"AUG": "Methionine",  
 "UUU": "Phenylalanine",  
 "UUC": "Phenylalanine",  
 "UUA": "Leucine",  
 "UUG": "Leucine",  
 "UCU": "Serine",  
 "UCC": "Serine",  
 "UCA": "Serine",  
 "UCG": "Serine",  
 "UAU": "Tyrosine",  
 "UAC": "Tyrosine",  
 "UGU": "Cysteine",  
 "UGC": "Cysteine",  
 "UGG": "Tryptophan",  
 "UAA": "STOP",  
 "UAG": "STOP",  
 "UGA": "STOP",**  
 }

and to find the corresponding protein from the codon it was just a matter of finding the key and value.

```text
    out = Proteins[codon]    
    if strings.Compare(out, "STOP") == 0 {
        return "", ErrStop
    } else if out == "" {
        return "", ErrInvalidBase
    }
```

The code for the FromRNA remained same.

## Version 3.0

The feeling of still can be optimized was there, so came up with the version 3.0.

```text
// FromRNA Returns proteins
func FromRNA(rna string) ([]string, error) {
	// 3 character long
	var rex = regexp.MustCompile(`...`)
	codons := rex.FindAllString(rna, -1)

	var proteins []string

	for _, codon := range codons {
		protein, err := FromCodon(codon)

		switch err {
		case ErrStop:
			return proteins, nil
		case ErrInvalidBase:
			return proteins, err
		}

		proteins = append(proteins, protein)
	}

	return proteins, nil
}
```

Utilized the regular expression to chunk the incoming data and utilized the `FindAllString` to get the codons.

## -- THE - END --
