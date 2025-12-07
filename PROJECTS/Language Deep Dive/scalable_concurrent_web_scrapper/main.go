package main

import (
	"fmt"
	"net/http"
	"time"
	"sync"
)

// Define the concurrency limit
const MAX_CONCURRENCY = 10 

// --- Data Structure ---
type HealthCheckResult struct {
	URL    string
	Status string
	Time   time.Duration
}

// --- 1. Worker Function (The Goroutine Task) ---
func worker(id int, jobs <-chan string, results chan<- HealthCheckResult) {
	fmt.Printf("Worker %d started\n", id)
	
	// The 'range jobs' loop blocks until a job is available or the channel is closed.
	for url := range jobs {
		start := time.Now()
		var status string
		
		// Set a short timeout for the HTTP request
		client := http.Client{Timeout: 5 * time.Second}
		resp, err := client.Get(url)
		
		if err != nil {
			status = fmt.Sprintf("Error: %v", err)
		} else {
			status = resp.Status
			resp.Body.Close()
		}
		
		duration := time.Since(start)
		
		// Send the result back on the results channel
		results <- HealthCheckResult{
			URL:    url,
			Status: status,
			Time:   duration,
		}
	}
	fmt.Printf("Worker %d shut down\n", id)
}

func main() {
	urls := []string{
		"http://google.com", "http://github.com", "http://fastapi.tiangolo.com",
		"http://golang.org", "http://rust-lang.org", "http://typescriptlang.org",
		"http://bad-url-1234567.com", "http://example.com/status", 
	}
	// Create 100 jobs by duplicating the array
	for i := 0; i < 4; i++ {
		urls = append(urls, urls...) 
	}
	numJobs := len(urls)
	fmt.Printf("Total jobs to process: %d\n", numJobs)

	// Create buffered channels for input and output
	jobs := make(chan string, numJobs)
	results := make(chan HealthCheckResult, numJobs)

	var wg sync.WaitGroup // WaitGroup ensures the main function waits for workers

	// 2. Start the worker pool (MAX_CONCURRENCY Goroutines)
	for w := 1; w <= MAX_CONCURRENCY; w++ {
		wg.Add(1) // Add one counter for the worker
		// Use an anonymous function to pass the worker ID safely
		go func(wID int) {
			defer wg.Done() // Decrement counter when worker exits
			worker(wID, jobs, results)
		}(w)
	}

	// 3. Send jobs to the workers
	for _, url := range urls {
		jobs <- url
	}
	close(jobs) // Crucial: Close the jobs channel to stop the workers' 'range' loop

	// 4. Wait for all workers to be done in a separate Goroutine
	go func() {
		wg.Wait()
		close(results) // Close results channel after all results have been sent
	}()

	// 5. Collect and print all results
	fmt.Println("\n--- Collecting Results ---")
	allResults := []HealthCheckResult{}
	for r := range results {
		allResults = append(allResults, r)
		// Only print a sample of results to avoid excessive output
		if len(allResults) <= 20 {
		    fmt.Printf("Result from %s: %s (took %s)\n", r.URL, r.Status, r.Time)
		}
	}

	fmt.Printf("\n--- Summary ---\nTotal URLs checked: %d\n", len(allResults))
}