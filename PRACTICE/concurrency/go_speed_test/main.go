package main

import (
	"fmt"
	"time"
)

// The function that will run in a separate Goroutine
// It takes a slice of numbers and a channel to send the result.
func sum(s []int, c chan int) {
	sum := 0
	for _, v := range s {
		sum += v
	}
	// Send the calculated sum to the channel. This operation blocks
	// until the main Goroutine is ready to receive it.
	c <- sum 
}

func main() {
	const N = 100000000 // 100 million elements

	// Create a slice (dynamic array) of 1 to N
	fmt.Printf("Preparing slice with %d elements...\n", N)
	s := make([]int, N)
	for i := 0; i < N; i++ {
		s[i] = i + 1
	}
	fmt.Println("Slice ready.")

	// Create an unbuffered channel to communicate the results
	c := make(chan int)

	start := time.Now()

	// 1. Concurrently sum the first half of the slice (using a Goroutine)
	// The result is sent to the channel 'c'.
	go sum(s[:N/2], c) 

	// 2. Concurrently sum the second half of the slice (using a Goroutine)
	// The result is also sent to the channel 'c'.
	go sum(s[N/2:], c)

	// 3. Receive the results from the channel in the main Goroutine.
	// This ensures both worker Goroutines have completed.
	// The order of reception is not guaranteed, but we receive two values.
	x, y := <-c, <-c // Blocking operation: wait for two values

	duration := time.Since(start)

	fmt.Println("\n--- Go Concurrency Results ---")
	fmt.Printf("Sub-Sum 1 (x): %d\n", x)
	fmt.Printf("Sub-Sum 2 (y): %d\n", y)
	fmt.Printf("Total Sum: %d\n", x + y)
	fmt.Printf("Total Time: %s\n", duration)
}