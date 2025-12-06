import time
import threading
import os

# Step 1: The base or helper funciton that I am going to concuritize

def sum_of_squares(n):
    """Calculate the number of suares up to n"""
    result = 0
    for i in range(1, n+1):
        result += i * i
        
    return result
    
    
# Step 2: The execution -- the baseline, how long teh task will take

def sequential_execution(data):
    start_time = time.perf_counter()
    results = []
    
    print("--- Starting Sequential Execution ---")
    
    for num in data:
        res = sum_of_squares(num)
        results.append(res)
        
    end_time = time.perf_counter()
    
    print(f"Sequential took: {end_time - start_time :.4f} seconds")
    return results

# Step 3: concurrent threading..

def concurrent_execution(data):
    start_time = time.perf_counter()
    threads = []
    results = []
    
    print(" --- Starting Concurrent Execution (Threading) ---")
    
    # simple function to append the result to teh shared list
    
    def worker(n, result_list):
        res = sum_of_squares(n)
        result_list.append(res)
        
    # creating a thread for each task
    
    for nums in data:
        t = threading.Thread(target=worker, args=(nums, results))
        threads.append(t)
        t.start()
    
    # wait for all threads to finish
    
    for t in threads:
        t.join()
        
        end_time = time.perf_counter()
        
    print(f"Concurrent took: {end_time - start_time :.4f} seconds")
    
    return results
        

# Step 4: Parallel execution -- usign multiprocessing

import multiprocessing

def parallel_execution(data):
    start_time = time.perf_counter()
    
    num_cores = os.cpu_count()
    print(f"    (Using {num_cores} cores)")
    
    print("--- Starting Parallel Execution (Multiprocessing) ---")
    
    # create a pool of worker processes, 
    # a context manager `with` handles process shutdown automatically
    
    with multiprocessing.Pool(processes=num_cores) as pool:
        # map number of squares to the input data
        results = pool.map(sum_of_squares, data)
        
    end_time = time.perf_counter()
    
    print(f"Parallel took {end_time - start_time :.4f} seconds")
    return results


if __name__ == '__main__':
    # Define the workload: four tasks, each is a CPU-heavy calculation
    NUMBERS_TO_PROCESS = [5_000_000] * 4 

    # 1. Sequential Run (Baseline)
    sequential_execution(NUMBERS_TO_PROCESS)

    print("-" * 40)
    
    # 2. Concurrent Run (Threading - Expected to be similar or slightly slower due to GIL)
    concurrent_execution(NUMBERS_TO_PROCESS) 

    print("-" * 40)

    # 3. Parallel Run (Multiprocessing - Expected to be significantly faster)
    parallel_execution(NUMBERS_TO_PROCESS)