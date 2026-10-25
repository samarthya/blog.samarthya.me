---
title: "Smallest Integer"
date: "2021-04-24T05:43:46Z"
slug: "smallest-integer"
categories: ["java", "technical"]
tags: ["algos", "java8"]
aliases: ["/wps/2021/04/24/smallest-integer/"]
wp_id: 1504
---

Code available [here](https://github.com/samarthya/smallestinteger).

The ask was to identify the smallest possible integer (> 0) in the array of integers.

## Example

```text
1. [-1,2] -> 1
2. [-1,-2] -> 1
3. [1,3] -> 2
```

I was initially thinking of using `sets` and then finding out the missing one, but then reaized it is simpler and I do not need sets

```text
class Solution {
    public int solution(int[] A) {
        // write your code in Java SE 8
        int smallestInt = 1;
        if(A.length == 0) return smallestInt;
        // Sort
        Arrays.sort(A);

        // If the first element is greater than 1
        if(A[0] > 1) return smallestInt;

        //If the last element is less than 1
        if(A[ A.length - 1] <= 0 ) return smallestInt;
    
        //Iterate through the array and process
        for(int i = 0; i < A.length; i++){
            if(A[i] == smallestInt){
                smallestInt++;}
        }

        return smallestInt;
    }
}
```
