use std::time::Instant;

const N: u32 = 100_000_000;

fn manual_loop_sum(numbers: &Vec<u32>) -> u64 {
    let mut sum: u64 = 0;
    for &num in numbers { // &num is an immutable borrow (read-only)
        if num % 2 == 0 { // Check if even
            sum += (num as u64) * 2; // Double and sum
        }
    }
    sum
}

fn zero_cost_iterator_sum(numbers: &Vec<u32>) -> u64 {
    numbers
        .iter() // Get an iterator over immutable references
        .filter(|&num| num % 2 == 0) // Filter: Keep only even numbers
        .map(|&num| (num as u64) * 2) // Map: Double the number
        .sum() // Sum: Calculate the total
}

fn main() {
    println!("Preparing vector with {} elements...", N);
    
    // Create a vector (heap-allocated collection) from 1 to N
    // This is the setup cost, not the benchmark cost.
    let numbers: Vec<u32> = (1..=N).collect(); 
    println!("Vector ready.");

    // --- 1. Manual Loop Benchmark ---
    let start_time_loop = Instant::now();
    let sum_loop = manual_loop_sum(&numbers);
    let duration_loop = start_time_loop.elapsed();

    // --- 2. Iterator Chain Benchmark ---
    let start_time_iter = Instant::now();
    let sum_iter = zero_cost_iterator_sum(&numbers);
    let duration_iter = start_time_iter.elapsed();

    println!("\n--- Zero-Cost Abstraction Results ---");
    println!("Manual Loop Result:   {} (Time: {:?})", sum_loop, duration_loop);
    println!("Iterator Chain Result: {} (Time: {:?})", sum_iter, duration_iter);
    
    if sum_loop == sum_iter {
        println!("\n✅ Results match! Times should be very close, proving zero-cost abstraction.");
    }
}