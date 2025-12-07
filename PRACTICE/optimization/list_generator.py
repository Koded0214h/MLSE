import time

# List comprehension:
# Memory Cost: High. If $N$ is the size of the sequence (e.g., $10^6$ elements), 
# the list comprehension will require memory proportional to $O(N)$ to store the entire result list at once.

def list_comprehension(x):
    
    print("--- List Comprehension ---")
    start_time = time.perf_counter()
    
    squares = [x*x for x in range(10**6)]
    
    end_time = time.perf_counter()
    duration = end_time - start_time
    
    print(f"Time Spent: {duration:.4f}")

# Generaor Expression(Lazy Evaluation):
# When to Use: When you only need to process the data one item at a time (e.g., streaming data, or using the result once in a for loop).
# Mechanism: Values are calculated on-demand only when the iterator's next() method (or a loop) explicitly requests them.
# Once yielded, the previous value is typically discarded.Example: squares_gen = (x*x for x in range(10**6))
# Memory Cost: Low. The generator only holds the current state of the iteration, 
# resulting in a memory cost proportional to O(1) (constant space), regardless of the sequence size.
def generator_expression(x):
    print("--- Generator Expression (Corrected) ---")
    start_time = time.perf_counter()
    
    # The actual calculation happens inside the sum() or a for loop
    squares_gen = (i*i for i in range(10**6))
    sum(squares_gen) # Forces full iteration and calculation
    
    end_time = time.perf_counter()
    duration = end_time - start_time
    
    print(f"Time Spent: {duration:.4f}")

x = [1, 2, 3, 4, 5, 6, 10]

list_comprehension(x)
generator_expression(x)

