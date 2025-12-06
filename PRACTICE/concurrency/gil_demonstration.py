import time
import threading
import multiprocessing

# --- Configuration ---
# You can change this number. A larger number means more calculations,
# making the difference between threads and processes clearer.
NUM_ITERATIONS = 500_000_000
NUM_WORKERS = 4 # Number of threads/processes to create

# ----------------------------------------------------
# 1. CPU-BOUND TASK FUNCTION
# This task involves heavy calculation and NO waiting (I/O).
# ----------------------------------------------------
def cpu_heavy_task(n):
    """Performs a long, CPU-intensive calculation."""
    count = 0
    # A simple loop that forces the CPU to work
    while n > 0:
        n -= 1
        count += 1
    # print(f"Worker finished calculation: {count}")

# ----------------------------------------------------
# 2. THREADING TEST (Limited by the GIL)
# ----------------------------------------------------
def test_threading():
    print(f"\n--- Testing THREADING (Limited by the GIL) ---")
    threads = []
    start_time = time.perf_counter()

    # Divide the work among the threads
    work_per_thread = NUM_ITERATIONS // NUM_WORKERS

    for i in range(NUM_WORKERS):
        # Create a new thread for the CPU task
        t = threading.Thread(target=cpu_heavy_task, args=(work_per_thread,))
        threads.append(t)
        t.start()
        
    # Wait for all threads to finish their work
    for t in threads:
        t.join()

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Total Threads: {NUM_WORKERS}")
    print(f"Total Time: {duration:.4f} seconds (Expected to be slow)")
    return duration

# ----------------------------------------------------
# 3. MULTIPROCESSING TEST (Bypassing the GIL)
# ----------------------------------------------------
def test_multiprocessing():
    print(f"\n--- Testing MULTIPROCESSING (Bypassing the GIL) ---")
    processes = []
    start_time = time.perf_counter()

    # Divide the work among the processes
    work_per_process = NUM_ITERATIONS // NUM_WORKERS

    for i in range(NUM_WORKERS):
        # Create a new process for the CPU task
        # Each process gets its OWN Python interpreter and OWN GIL
        p = multiprocessing.Process(target=cpu_heavy_task, args=(work_per_process,))
        processes.append(p)
        p.start()

    # Wait for all processes to finish their work
    for p in processes:
        p.join()

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Total Processes: {NUM_WORKERS}")
    print(f"Total Time: {duration:.4f} seconds (Expected to be fast)")
    return duration

# ----------------------------------------------------
# 4. RUN COMPARISON
# ----------------------------------------------------
if __name__ == "__main__":
    
    # 1. First, run the threading test
    thread_time = test_threading()
    
    print("=" * 40)
    
    # 2. Then, run the multiprocessing test
    process_time = test_multiprocessing()

    # 3. Final Comparison
    print("\n" + "=" * 40)
    print(f"--- CONCLUSION: ---")
    
    if process_time < thread_time:
        speed_up = thread_time / process_time
        print(f"Multiprocessing was {speed_up:.2f}x faster than Threading.")
        print(f"This is the effect of the GIL on CPU-bound tasks!")
    else:
        print("The difference was negligible, but Multiprocessing should still be slightly faster.")
    
    print("=" * 40)