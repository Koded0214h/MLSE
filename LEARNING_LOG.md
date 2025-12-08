# My Learning Log

#### Projects & Practice @ 23:24
*   Worked on concurrency with Go(Goroutines & channels),
    Rust(optimization -- math & iterations),
    TypeScript(optimization -- linear code)

*   Started the first set of projects for Language Deep Dive.
    1. API and Data Transformation Service with FastAPI -- python
    * a lightweight web service with endpoint `POST /api/convert`
    * Challenge Focus API design, data manipulation/parsing (using the built-in csv module or pandas if desired),
    * error handling for bad user input, and JSON serialization.

*   2. Resilent Asynchronous Data Processing -- rust
    * a command-line application for a simple highly-reliable log aggregation service
    * Challenge Focus: Error handling `(Result<T, E>)`,
    * asynchronous I/O (async/await), and thread-safe data transfer (channels).

*   3. Scalable Concurrent Web Scraper -- go
    * a command-line tool that performs a health check on a list of URLs by fetching them concurrently
    * Challenge Focus: Limiting concurrency with a Goroutine pool,
    * using channels for job distribution and result collection, and error management (Go's error interface).

#### Projects @ 11:08
*   I renamed the projects in Lnaguage Deep Dive after their respective languages

*   Project
*   1. Concurrent Web Scraper and Data Analyzer (Python OOD):
    ObjectiveDesign and implement a robust, object-oriented Python application to concurrently scrape product titles and prices from a list of URLs and then analyze the collected data. This project must clearly demonstrate and address the limitations imposed by the Python GIL.
    Phase 1: Object-Oriented Design (OOD): Product Scraper, Data Analyzer, ConcurrentManager
    Phase 2: GIL Demonstartion & Testing

*   2. Updated the ThreadPoolExecutor and ProcessPoolExecutor to use the I/O Threads
*   3. Updated the  ConcurrentManager to use heavy-bound CPU tasks and processes instead of just `numpy` functions
