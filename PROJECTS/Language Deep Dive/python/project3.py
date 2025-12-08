# 🧠 Project: Concurrent File Processor & Task Scheduler
# This project separates the I/O-bound (reading files) and CPU-bound (processing data) components into distinct, measurable tasks, allowing you to explicitly choose the optimal concurrency model for each.

# III. 📝 Required Class Methods
# 1. FileGenerator (Setup): generate_dummy_files(count: int, size_mb: int) -> List[str]: Creates the required number of files of a specified size in a temporary directory and returns a list of their paths.

# IN order to do this i need to undetstand file handlign better

# There are four different methods (modes) for opening a file:
# "r" - Read - Default value. Opens a file for reading, error if the file does not exist
# "a" - Append - Opens a file for appending, creates the file if it does not exist
# "w" - Write - Opens a file for writing, creates the file if it does not exist
# "x" - Create - Creates the specified file, returns an error if the file exists
# In addition you can specify if the file should be handled as binary or text mode
# "t" - Text - Default value. Text mode
# "b" - Binary - Binary mode (e.g. images)

def read_file():
    """For modularity of code"""
    
    # using the with keyword
    
    with open("files/demofile.txt") as f:
        file = f.read()
        

f = open("files/demofile.txt")

print(f.read())

f.close() # must always close files if using without `with`

print("=" * 20)
    
with open("files/demofile.txt", "a") as f:
    f.write("Now the file has more content!") 
    
    
# creating a new file
# f = open("files/newFile.txt", "x")

# =========================================================
# BACK TO THE PROJECT
# =========================================================

import os
import time
import shutil
import random
from typing import List, Tuple, Callable, Any
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# --- CONFIGURATION ---
NUM_FILES = 10
FILE_SIZE_KB = 5 # 5 KB per file for a quick I/O read
MAX_WORKERS = 4
TEMP_DIR = "temp_data_files"
# ---------------------

class FileGenerator:
    """Creates dummy files for I/O testing."""
    def __init__(self, directory: str):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)
        
    def generate_dummy_files(self, count: int, size_kb: int) -> List[str]:
        """Creates 'count' files of 'size_kb' KB each."""
        created_files = []
        size_bytes = size_kb * 1024
        
        # Use random data for better file I/O simulation
        dummy_content = os.urandom(1024) # 1KB of random bytes
        
        for i in range(count):
            file_path = os.path.join(self.directory, f"dummy_{i+1}.bin")
            
            with open(file_path, "wb") as f:
                bytes_written = 0
                while bytes_written < size_bytes:
                    bytes_to_write = min(len(dummy_content), size_bytes - bytes_written)
                    f.write(dummy_content[:bytes_to_write])
                    bytes_written += bytes_to_write
            
            created_files.append(file_path)
        
        print(f"✅ Generated {len(created_files)} dummy files in '{self.directory}' ({size_kb} KB each).")
        return created_files

    def cleanup(self):
        """Removes the temporary directory and all its contents."""
        try:
            shutil.rmtree(self.directory)
            print(f"🧹 Cleaned up directory '{self.directory}'.")
        except OSError as e:
            print(f"Error during cleanup: {e}")


class TaskProcessor:
    """Performs and measures concurrent I/O and CPU tasks."""
    
    # ----------------------------------------------------
    # STAGE 1: I/O-Bound Task (Threads should be faster)
    # ----------------------------------------------------
    def io_task(self, file_path: str) -> int:
        """Reads the file content and returns its byte size."""
        # The GIL is released during this operation
        with open(file_path, 'rb') as f:
            data = f.read()
        return len(data)

    # ----------------------------------------------------
    # STAGE 2: CPU-Bound Task (Processes should be faster)
    # ----------------------------------------------------
    def cpu_task(self, data_size: int) -> float:
        """Performs a heavy, GIL-holding calculation."""
        
        # Scale the calculation based on file size, but keep the base high
        # A dense Python loop that holds the GIL
        n = 200_000_000 # Base number of iterations (Adjust if test is too short/long)
        
        x = 0
        for i in range(n):
            # Complex, non-releasing Python calculation
            x = (x + i * random.random()) / 1.618
            
        # Returning a final value to prove work was done
        return x

    # ----------------------------------------------------
    # ORCHESTRATION METHOD (The crucial part)
    # ----------------------------------------------------
    def run_test(self, task: Callable, args_list: List[Any], pool_type: str) -> float:
        """
        Runs a list of tasks concurrently using the specified pool type.
        
        :param task: The function to execute (io_task or cpu_task).
        :param args_list: A list of arguments for each call to the task function.
        :param pool_type: 'Thread' or 'Process'.
        :return: Total execution time.
        """
        if pool_type == 'Thread':
            Pool = ThreadPoolExecutor
            description = "ThreadPoolExecutor (Threads)"
        elif pool_type == 'Process':
            Pool = ProcessPoolExecutor
            description = "ProcessPoolExecutor (Processes)"
        else:
            raise ValueError("pool_type must be 'Thread' or 'Process'")

        print(f"\n--- Running: {task.__name__} with {description} ({len(args_list)} tasks) ---")
        start_time = time.perf_counter()
        
        results = []
        with Pool(max_workers=MAX_WORKERS) as executor:
            # executor.map is simple and efficient for this use case
            # It maps the callable (task) to every item in the iterable (args_list)
            futures = executor.map(task, args_list)
            
            # Convert map iterator to list to force completion and collect results
            results.extend(list(futures))

        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"Completed {len(results)} tasks in {duration:.4f}s.")
        return duration


if __name__ == "__main__":
    
    # --- SETUP: Generate Files ---
    file_generator = FileGenerator(TEMP_DIR)
    file_paths = file_generator.generate_dummy_files(NUM_FILES, FILE_SIZE_KB)
    
    processor = TaskProcessor()
    
    # --- GET ARGUMENTS FOR EACH STAGE ---
    # For Stage 1 (I/O), the arguments are the file paths
    io_args = file_paths 
    
    # For Stage 2 (CPU), we use a placeholder size for each core (e.g., 4 tasks)
    # We use a list of sizes to ensure each worker is given an independent, heavy task.
    cpu_args = [FILE_SIZE_KB] * MAX_WORKERS 

    # =========================================================================
    # PART 1: I/O-BOUND TESTS (Reading Files)
    # =========================================================================
    
    # TEST 1 (Optimal I/O): I/O Task with Threads
    time_io_thread = processor.run_test(
        processor.io_task, io_args, 'Thread'
    )

    # TEST 2 (Suboptimal I/O): I/O Task with Processes
    time_io_process = processor.run_test(
        processor.io_task, io_args, 'Process'
    )
    
    # =========================================================================
    # PART 2: CPU-BOUND TESTS (Heavy Calculation)
    # =========================================================================
    
    # TEST 3 (Optimal CPU): CPU Task with Processes
    time_cpu_process = processor.run_test(
        processor.cpu_task, cpu_args, 'Process'
    )

    # TEST 4 (Suboptimal CPU): CPU Task with Threads (The GIL Demo)
    time_cpu_thread = processor.run_test(
        processor.cpu_task, cpu_args, 'Thread'
    )

    # =========================================================================
    # CONCLUSION: GIL DEMONSTRATION SUMMARY
    # =========================================================================
    print("\n" + "=" * 60)
    print("        CONCURRENCY MODEL PERFORMANCE SUMMARY")
    print("=" * 60)
    
    print("\n--- I/O-BOUND TASK (File Reading) ---")
    print(f"Threads (Optimal):  {time_io_thread:.4f}s")
    print(f"Processes:          {time_io_process:.4f}s")
    print(f"Result: Threads are typically faster due to lower setup overhead.")
    
    print("\n--- CPU-BOUND TASK (GIL Demo) ---")
    print(f"Processes (Optimal): {time_cpu_process:.4f}s")
    print(f"Threads (GIL Bottleneck): {time_cpu_thread:.4f}s")
    
    if time_cpu_thread > time_cpu_process * 1.5: # Threads should be significantly slower
        print("✅ **GIL DEMONSTRATION SUCCESSFUL**")
        print("Threads took significantly longer on the CPU task because the **Python GIL** prevented true parallel execution across multiple cores. Processes bypassed the GIL.")
    else:
        print("⚠️ **GIL DEMONSTRATION MAY REQUIRE TUNING**")
        print("The CPU task (threads) was not significantly slower than processes. You may need to increase the 'n' value in `TaskProcessor.cpu_task` to make the calculation heavy enough.")
        
    print("=" * 60)
    
    # --- CLEANUP ---
    file_generator.cleanup()