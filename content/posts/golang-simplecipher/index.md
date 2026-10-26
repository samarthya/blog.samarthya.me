---
title: "GoLang: SimpleCipher"
date: "2020-05-11T10:14:20Z"
slug: "golang-simplecipher"
categories: ["technical"]
tags: ["algo", "cipher", "golang"]
aliases: ["/wps/2020/05/11/golang-simplecipher/"]
wp_id: 645
---

Hello back again, Golang is just a new syntax for me. Even though behind the scenes they developers have simplified many things, for a consumer like me writing a program is more about learning the new syntax and getting familiarized with the control and stack.

In my constant quest to try something different, today I try and solve the simple cipher which by definition is a text replacement algorithm that makes the text a little difficult to break while reading with naked eyes.

[SimpleCipher](https://github.com/samarthya/goexercism/tree/master/simple-cipher): Code available in GitHub

![Caesar cipher with a left shift of 3: each letter is replaced by the one three places earlier in the alphabet](https://camo.githubusercontent.com/17a2d0ae02743554139d4045a62cb943a40c8e51/68747470733a2f2f75706c6f61642e77696b696d656469612e6f72672f77696b6970656469612f636f6d6d6f6e732f7468756d622f342f34612f4361657361725f6369706865725f6c6566745f73686966745f6f665f332e7376672f33323070782d4361657361725f6369706865725f6c6566745f73686966745f6f665f332e7376672e706e67)

## Version 1.0

```text
The first version was a basic logic writing which allowed to check for the code and decode capability.
```

```text
// Encrypt struct
type Encrypt struct {
	distance int
	key      string
}

// NewCaesar Object that implements the interface Cipher
func NewCaesar() Cipher {
	return Encrypt{distance: 3, key: ""}
}

// NewShift Object that implements the interface Cipher
func NewShift(distance int) Cipher {
	// Corner case when of 0, 26, -26
	if distance < -26 || distance > 26 || distance == 0 {
		return nil
	}
	return Encrypt{distance, ""}
}

// NewVigenere Object that implements the interface Cipher
func NewVigenere(key string) Cipher {

	if key == "" || checkKeyInvalid(key) {
		return nil
	}
	return Encrypt{0, key}
}

// checkAllAs Checks for all A's in the key.
func checkKeyInvalid(s string) (f bool) {

	// If any invalid character matches
	if matched, _ := regexp.MatchString(`[^a-z]`, s); matched {
		return true
	}

	for _, m := range s {
		switch m {
		case 'a':
			f = true
		default:
			f = false
			return
		}
	}
	return
}
```

I also wrote a utility to remove all invalid character basically all the chars that were not either of A-Z or a-z.

```text
// removeAllOtherCharcterBeforeEncoding replace all the other elements
func removeAllOtherCharcterBeforeEncoding(s string) (o string) {
	o = RegularExp.ReplaceAllString(s, "")
	log.Printf(" String: %s", o)
	o = strings.ToLower(o)
	return
}

var RegularExp = regexp.MustCompile(`[^A-Za-z]`)
```

The basic logic of transforming the input string to encoded string was written in these two functions below

```text
func transformWithString(s string, e string, flag bool) string {
	var sb strings.Builder

	em := []rune(e)

	for i, sm := range s {
		// The key has to be repeated
		var d rune = 0

		if i < len(em) {
			d = em[i] - 'a'
		} else {
			d = em[(i%len(em))] - 'a'
		}

		if flag {
			switch {
			case sm >= 'a' && sm <= 'z':
				fmt.Fprintf(&sb, "%s", string('a'+(sm-'a'+d)%26))
			}
		} else {
			switch {
			case sm >= 'a' && sm <= 'z':
				diff := ((sm - 'a' - d) % 26)
				newChar := ""

				if diff < 0 {
					newChar = string('z' + diff + 1)
				} else {
					newChar = string('a' + diff)
				}
				fmt.Fprintf(&sb, "%s", newChar)
			}
		}
	}
	return sb.String()
}

// transformWithDistance Allows transformation based on distance.
func transformWithDistance(s string, d int) string {

	rotateFunction := func(r rune) rune {
		switch {
		case r >= 'a' && r <= 'z':
			val := (r - 'a' + rune(d))
			if val < 0 && d < 0 {
				return 'z' + ((val + 1) % 26)
			}
			return 'a' + (val % 26)

		default:
			log.Printf(" Not a charcter: %s", string(r))
		}
		return ' '
	}

	return strings.Map(rotateFunction, s)

}
```

The basic functions that invoke these encode and decode functions are as under

```text
// Encode Implements the interface Cipher
func (e Encrypt) Encode(s string) (o string) {
	o = ""
	s = removeAllOtherCharcterBeforeEncoding(s)

	if s == "" || len(s) <= 0 {
		return
	}

	// Iterate throught the runes

	switch {
	case e.distance != 0:
		o = strings.ReplaceAll(transformWithDistance(s, e.distance), " ", "")
	default:
		o = transformWithString(s, e.key, true)
	}

	return
}

// Decode decides the encrypted string
func (e Encrypt) Decode(s string) (o string) {
	o = ""

	log.Printf(" Decode: %s", s)

	if s == "" || len(s) <= 0 {
		return
	}

	switch {
	case e.distance != 0:
		log.Printf(" Distance: %d", e.distance)
		o = transformWithDistance(s, -e.distance)
	default:
		o = transformWithString(s, e.key, false)
	}

	return
}
```

Now the general feeling after writing this was I have too much the same code that I should remove for example

- transformWithDistance
- transformWithString

They are essentially doing the same thing?

Version 2.... to follow soon.
