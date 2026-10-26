---
title: "Concurrency"
date: "2020-01-03T12:00:00Z"
slug: "concurrency-golang"
description: "Last few weeks have been interesting, a new year just embarked, my learning pace slowed down; comparatively due to the festivities and obligations around, but I am still trying to maintain."
categories: ["others"]
tags: ["golang", "mutex", "sync", "waitgroup"]
aliases: ["/wps/2020/01/03/concurrency-golang/"]
recovered: "Internet Archive snapshot 2026-03-13"
---

# Concurrency and Parallelism – (Helpful [link](https://blog.golang.org/concurrency-is-not-parallelism))

Last few weeks have been interesting, a new year just embarked, my learning pace slowed down; comparatively due to the festivities and obligations around, but I am still trying to maintain.

This week  tried another exercise from [exercism.io.](https://exercism.io/my/solutions/0c4d940813284b0c8dacf70d93c0edab) If you have not seen this site, I recommend it highly. It is just a fun way of keeping yourself engaged in learning and trying out exercises, and all the while engaging with fellow programmers or mentors.

This exercise, was about, counting the occurrence of characters in a string and trying to do it [parallel](https://www.golang-book.com/books/intro/10). The solution I wrote for it, is as under and will be explaining in detail.

```text
package letter

import "sync"

// FreqMap records the frequency of each rune in a given text.
type FreqMap map[rune]int

type SafeMap struct {
	val  FreqMap
	lock sync.Mutex
}

func (sm *SafeMap) Increment(e rune) {
	sm.lock.Lock()
	sm.val[e]++
	sm.lock.Unlock()
}

// Frequency counts the frequency of each rune in a given text and returns this
// data as a FreqMap.
func Frequency(s string) FreqMap {
	m := FreqMap{}
	for _, r := range s {
		m[r]++
	}
	return m
}

func ParallelFreq(s string, sm *SafeMap, wg *sync.WaitGroup) {
	for _, r := range s {
		sm.Increment(r)
	}

	if wg != nil {
		wg.Done()
	}
}

func ConcurrentFrequency(elements []string) FreqMap {
	var sm SafeMap

	var wg sync.WaitGroup

	sm.val = FreqMap{}

	wg.Add(len(elements))
	for _, r := range elements {
		go ParallelFreq(r, &sm, &wg)
	}
	wg.Wait()

	return sm.val
}
```

> The challenge was to do counting in parallel.

## Concurrency vs Parallel

What do we understand by concurrency and is it just another word for parallel execution?

> They are related but not the same thing.

Concurrency is about DEALING with lots of things at once, it is about structure.

Parallelism is about DOING lots of things at once, it is about execution.

### GoRoutine

A **goroutine** is a function that is capable of running concurrently with other functions. To create a **goroutine** we use the keyword `go` followed by a function invocation:

## Step 1

Defining the structure for storing the count and the letter.

```text
type FreqMap map[rune]int

type SafeMap struct {
	val  FreqMap
	lock sync.Mutex
}
```

## TYPE: FreqMap

**FreqMap** allows you to define a map of rune and int. E.g. { {‘a’, 2}, {‘b’, 1}…}

## STRUCT: SafeMap

**SafeMap** allows you to extend the basic type **FreqMap** and add the synchronization behavior, as it will be used by multiple go routines in parallel.

## Method: Parallel Counting – `ParallelFreq`

In order to utilize the parallel counting I defined a method that utilizes the objects from sync:module of golang.

```text
func ParallelFreq(s string, sm *SafeMap, wg *sync.WaitGroup) {
	for _, r := range s {
		sm.Increment(r)
	}

	if wg != nil {
		wg.Done()
	}
}
```

It takes in the following argument

1. **s** – String to be scanned through to populate the Map – **SafeMap** and when the processing is done it notifies the WaitGroup by invoking Done() method.
2. **sm** – **SafeMap** that has a method Increment() to increment the respective rune value.
3. **wg** – **WaitGroup** to be notified of task completion.

## GoRoutine creator – ConcurrentFrequency

```text
func ConcurrentFrequency(elements []string) FreqMap {
	var sm SafeMap

	var wg sync.WaitGroup

	sm.val = FreqMap{}

	wg.Add(len(elements))
	for _, r := range elements {
		go ParallelFreq(r, &sm, &wg)
	}
	wg.Wait()

	return sm.val
}
```

1. It receives an input a slice of strings
2. Defines a WaitGroup for the len of the slice.
3. Creates go routines by invoking *go ParallelFreq.*
4. Waits for all the goroutines to finish
5. Returns the FreqMap.

## Benchmark : go test -v –bench . –benchmem

```text
pkg: letter
BenchmarkSequentialFrequency-16 55041 21012 ns/op 2995 B/op 13 allocs/op
BenchmarkConcurrentFrequency-16 25628 48832 ns/op 2136 B/op 14 allocs/op
PASS
ok letter 3.127s
```

You can further optimise the declaration and initialization of the SafeMap

```text
var sm = SafeMap{FreqMap{}, sync.Mutex{}}
```

\* You can find more samples in my GitRepo.

— THE – END —
