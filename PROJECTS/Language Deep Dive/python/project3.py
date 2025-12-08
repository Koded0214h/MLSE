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
from typing import List ,Tuple, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor
import threading

MAX_WORKERS = 5

class FileGenerator():
    def __init__(self, count: int, size_kb: int):
        self.count = count
        self.size_kb = size_kb

    def generateDummy(self) -> List[str]:
        """Generate dummy files of specified size in MB"""
        created_files = []
        
        # Create files directory if it doesn't exist
        os.makedirs("files", exist_ok=True)
        
        # Calculate size in bytes
        size_bytes = self.size_kb * 1024
        
        for i in range(self.count):
            file_name = f"files/dummy{i+1}.txt"
            
            # Generate content - you can use different patterns:
            
            # Method 1: Repeat a pattern
            chunk = "K" * 1024  # 1KB chunk
            with open(file_name, "wb") as f:  # Use binary mode for large files
                bytes_written = 0
                while bytes_written < size_bytes:
                    bytes_to_write = min(len(chunk), size_bytes - bytes_written)
                    f.write(chunk[:bytes_to_write].encode('utf-8'))
                    bytes_written += bytes_to_write
            
            # Verify file size
            actual_size = os.path.getsize(file_name)
            print(f"Created {file_name}: {actual_size / (1024):.2f} KB")
            
            created_files.append(file_name)
        
        return created_files
    
    

    
class TaskProcessor():
    def __init__(self):
        self.total_size = 0
        self.processed_count = 0
    
    def io_task(self, file_path: str) -> Tuple[str, int]:
        """Calculate file size - what each thread executes"""
        start_time = time.time()
        
        try:
            if not os.path.exists(file_path):
                return (file_path, 0)
            
            size = os.path.getsize(file_path)
            elapsed = time.time() - start_time
            
            print(f"✓ Thread processed {os.path.basename(file_path)}: "
                  f"{size:,} bytes in {elapsed:.3f}s")
            
            return (file_path, size)
            
        except Exception as e:
            print(f"✗ Error with {file_path}: {e}")
            return (file_path, 0)
    
    def analyze_files(self, file_paths: List[str], max_workers: int = 8) -> Dict:
        """Main method to analyze files concurrently"""
        print(f"\n{'='*60}")
        print(f"Starting concurrent file analysis")
        print(f"Files to process: {len(file_paths)}")
        print(f"Thread pool size: {max_workers}")
        print(f"{'='*60}")
        
        total_start = time.time()
        results = {}
        
        # Submit tasks to thread pool
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all files for processing
            future_to_file = {
                executor.submit(self.io_task, file_path): file_path 
                for file_path in file_paths
            }
            
            # Process results as they complete
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    filename, size = future.result()
                    results[filename] = size
                    self.processed_count += 1
                    self.total_size += size
                except Exception as e:
                    print(f"Failed to get result for {file_path}: {e}")
        
        total_time = time.time() - total_start
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"ANALYSIS COMPLETE")
        print(f"{'='*60}")
        print(f"Total files processed: {self.processed_count}")
        print(f"Total size: {self.total_size:,} bytes "
              f"({self.total_size/(1024*1024):.2f} MB)")
        print(f"Total time: {total_time:.3f} seconds")
        print(f"Average time per file: {total_time/len(file_paths):.3f} seconds")
        
        return results
    
    def cpu_task(self, data_size: int) -> float:
        
        # --- SIMULATE HEAVY CPU-BOUND WORK THAT HOLDS THE GIL ---
        start = time.perf_counter()
        # A dense loop is excellent for holding the GIL
        n = 200_000_000_000  # Adjust based on your CPU speed (aim for ~5-10 seconds)
        x = 0
        for i in range(n):
            x = i * i / 2.71828 # Complex math operation
        end = time.perf_counter()
        print(f"[Analyzer] Pure Python Calculation took: {end - start:.4f}s")
        
    
    def run_analyzer(self, data: List[ProductData], executor_type='Process'):
        # We must pass the data *to* the pool to be worked on.
        analyzer = self.cpu_task(data)
        
        # Define which executor to use based on the test
        if executor_type == 'Process':
            Pool = ProcessPoolExecutor
            print(f"[TEST 2: CPU (Processes)] Starting analysis...")
        elif executor_type == 'Thread':
            Pool = ThreadPoolExecutor
            print(f"[TEST 3: CPU (Threads - GIL Demo)] Starting analysis...")
        else:
            return # Handle error
            
        start_time = time.perf_counter()
        
        with Pool(max_workers=MAX_WORKERS) as executor:
            # .submit() returns a Future object immediately
            future = executor.submit(analyzer.calculate_statistics)
            # .result() blocks until the task is complete and returns the result
            stats = future.result() 

        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"[{executor_type}] Analysis completed in {duration:.4f}s")
        return duration
        
# Usage
if __name__ == "__main__":
    
    generator = FileGenerator(10, 2)
    
    files = generator.generateDummy() 
    print(f"\nCreated {len(files)} files")
    
    analyzer = TaskProcessor()
    results = analyzer.analyze_files(files, max_workers=4)
    
    