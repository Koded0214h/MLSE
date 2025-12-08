# Project: Concurrent Web Scraper and Data Analyzer (Python OOD) 
# ObjectiveDesign and implement a robust, object-oriented Python application to concurrently scrape product titles and prices from a list of URLs 
# and then analyze the collected data. This project must clearly demonstrate and address the limitations imposed by the Python GIL.

# Technical RequirementsLanguage & Libraries: Python 3.9+, standard libraries (requests, concurrent.futures, multiprocessing), 
# and OOD principles.Design Paradigm: Strict adherence to Object-Oriented Programming (OOP) using classes for Scraper, Analyzer, and the overall Manager.

import time
import requests
import numpy
from typing import List, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from bs4 import BeautifulSoup
import multiprocessing
import json

# i need to first learn how to use the requests library

# A get request to 'https://w3schools.com/python/demopage.htm'
x = requests.get('https://w3schools.com/python/demopage.htm')
print(f"Text: {x.text} \n Status: {x.status_code} \n JSON: {x.json}")

jumia = requests.get('https://www.jumia.com.ng/televisions/#catalog-listing')

print("=" * 40)

# The syntax: "requests.methodname(params)"
# Method	                    |  Description
# delete(url, args)	            |  Sends a DELETE request to the specified url
# get(url, params, args)	    |  Sends a GET request to the specified url
# head(url, args)	            |  Sends a HEAD request to the specified url
# patch(url, data, args)	    |  Sends a PATCH request to the specified url
# post(url, data, json, args)	|  Sends a POST request to the specified url
# put(url, data, args)	        |  Sends a PUT request to the specified url
# request(method, url, args)	|  Sends a request of the specified method to the specified url

# I need to learn how to use beautifulsoup4

# A simple soup instance for web scrapping
soup = BeautifulSoup(jumia.text, 'html.parser')

products = []

# Get ALL product elements first
all_products = soup.find_all('article', class_='prd _box _hvr')  # Adjust selector based on actual HTML

limit = 10  # Show only first 10 products
limited_products = all_products[:limit]

print(f"Found {len(all_products)} total products, showing {len(limited_products)}")

# Debug: Check what attributes the core link has
if limited_products:
    first_core_link = limited_products[0].find('a', class_='core')
    if first_core_link:
        print("\n=== DEBUG: CORE LINK ATTRIBUTES ===")
        print(f"Tag: {first_core_link.name}")
        print(f"All attributes: {first_core_link.attrs}")
        print(f"Has 'href'? {'href' in first_core_link.attrs}")
        
        # Check all attributes that might contain a link
        for attr_name, attr_value in first_core_link.attrs.items():
            print(f"  {attr_name}: {attr_value}")

print("\n=== EXTRACTED PRODUCTS ===")
for i, product in enumerate(limited_products, 1):
    # Find the <a class="core"> element inside the product
    core_link = product.find('a', class_='core')
    
    # Extract name from data attribute
    if core_link:
        name = core_link.get('data-ga4-item_name', 'No name found')
        # Try to get the link - check the 'href' attribute
        link = core_link.get('href', 'No link found')
    else:
        name = "No name found"
        link = "No link found"
    
    # Extract price
    product_price_element = product.find("div", class_="prc")
    price = product_price_element.text.strip() if product_price_element else "No price found"
    
    # Also try finding ANY link in the product
    if link == "No link found":
        any_link = product.find('a')
        if any_link:
            link = any_link.get('href', 'No link found')
    
    print(f"{i}. Name: {name}")
    print(f"   Price: {price}")
    print(f"   Link: {link}")
    print("-" * 40)

print("=" * 40)

# PROJECT: Concurrent Web Scraper and Data Analyzer (Python OOD)

# ProductScraper Class (The Worker)
# Purpose: Handles the I/O-bound task of fetching a single URL.
# Methods:
# __init__(self, url_list): Stores the list of URLs to scrape.
# fetch_data(self, url): A method that takes a single URL, uses requests to fetch the HTML, and extracts two pieces of simulated data 
# (e.g., "Product Title" and "Price"). 
# It should include a simulated network delay (e.g., time.sleep(1)).
# Crucial Design Point: This class's primary method should be designed to run efficiently under multithreading because network I/O releases the GIL.


@dataclass
class ProductData:
    """Data class to hold product information"""
    title: str
    price: float
    url: str

class ProductScrapper():
    def __init__(self, url_list: List[str]):
        # i feel like i should have used BaseModel to handle this thing, but lets keep going..
        self.url_list = url_list
    
    def fetch_data(self, url: str) -> Optional[List[ProductData]]:
        """Fetch data from a single URL"""
        try:
            response = requests.get(url, timeout=5)
            time.sleep(1)
            response.raise_for_status() # raise exception for bad status codes
            
            # Previously mocked the data, now lets fetch real data..
            
            # return ProductData(
            #     title="Sample Product",
            #     price=99.99,
            #     url=url
            # )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            products_data = []

            # Get ALL product elements first
            all_products = soup.find_all('article', class_='prd _box _hvr')  # Adjust selector based on actual HTML

            limit = 10  # Show only first 10 products
            limited_products = all_products[:limit]

            print(f"Found {len(all_products)} total products, showing {len(limited_products)}")
            
            for i, product in enumerate(limited_products, 1):
                # Find the <a class="core"> element inside the product
                core_link = product.find('a', class_='core')
                
                # Method 1: Get name & link from data attribute (already a string)
                if core_link:
                    name = core_link.get('data-ga4-item_name', 'No name found')
                    relative_link = core_link.get('href', '')
                    full_link = f"https://www.jumia.com.ng{relative_link}" if relative_link else url
                else:
                    name = "No name found"
                    full_link = url
                    
                # Method 2: Clean up the price (extract text from element)
                product_price_element = product.find("div", class_="prc")
                price = product_price_element.text.strip() if product_price_element else "No price found"
                
                # Convert price text to float (remove currency symbols and commas)
                try:
                    # Extract numbers from price string like "₦ 129,000"
                    price_value = float(price.replace('₦', '').replace(',', '').strip())
                except (ValueError, AttributeError):
                    price_value = 0.0
                
                
                print(f"{i}. Name: {name}")
                print(f"   Price: {price_value}")
                
                # Create ProductData object for each product
                product_data = ProductData(
                    title=name,
                    price=price_value,
                    url=full_link
                )
                products_data.append(product_data)
                
                print(f"[Scraper] {i}. {name[:50]}... - ₦{price_value:,.2f}")
            
            return products_data  # Return list of products
            
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
        
# DataAnalyzer Class (The CPU Hog)
# Purpose: Handles the CPU-bound task of processing raw scraped data.
#  Methods:
# __init__(self, data): Initializes with the list of scraped dictionaries.
# calculate_statistics(self): A CPU-intensive method that iterates through the entire dataset to calculate complex statistics ,
# Simulate CPU work by performing many mathematical operations or running a non-releasing function (like a dense loop).
# Crucial Design Point: This class's primary method should be designed to run under multiprocessing because heavy calculation will not release the GIL.
        
class DataAnalyzer():
    def __init__(self, data:List[str]):
        self.data = data
    
    
    # Corrected: in order to use the GIL, replaced with Heavy-bound CPU tasks
    # Inside DataAnalyzer class
    def calculate_statistics(self):
        print(f"[Analyzer] Starting heavy CPU work on {len(self.data)} items...")
        
        # --- SIMULATE HEAVY CPU-BOUND WORK THAT HOLDS THE GIL ---
        start = time.perf_counter()
        # A dense loop is excellent for holding the GIL
        n = 200_000_000  # Adjust based on your CPU speed (aim for ~5-10 seconds)
        x = 0
        for i in range(n):
            x = i * i / 2.71828 # Complex math operation
        end = time.perf_counter()
        print(f"[Analyzer] Pure Python Calculation took: {end - start:.4f}s")
        # --------------------------------------------------------

        prices = [p.price for p in self.data if p.price > 0] # Filter out 0.0 prices

        if not prices:
            return {"Mean": 0, "Median": 0, "SD": 0}
            
        # Standard numpy calls are fast; the loop above is the real demo
        mean_price = numpy.mean(prices)
        median_price = numpy.median(prices)
        sd_price = numpy.std(prices)
        
        stats = {
            "Mean": mean_price, 
            "Median": median_price, 
            "SD": sd_price
        }
        return stats
       
       
# ConcurrentManager Class (The Orchestrator)
# Purpose: Manages the flow, decides on the concurrency model, and collects results.
# Methods:run_scraper(self, urls): Uses concurrent.futures.ThreadPoolExecutor to execute the ProductScraper.fetch_data method for all URLs concurrently.
# run_analyzer(self, data): Uses concurrent.futures.ProcessPoolExecutor or the multiprocessing module to run the DataAnalyzer.calculate_statistics method.
# main(self, urls): The entry point that orchestrates the entire flow: Scrape -> Analyze -> Report. 

MAX_WORKERS = 5

class ConcurrentManager():
    def __init__(self, urls: List[str]):
        self.urls = urls
        
    # Corrected with actual ThreadPoolExecutor
    def run_scraper(self):
        start_time = time.perf_counter()
        scraper = ProductScrapper([]) # Initialize Scrapper to get the method
        all_results = []
        
        # Use the Executor via a 'with' statement for proper resource management
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # executor.map() applies the function (scraper.fetch_data) to every iterable (self.urls)
            # The first argument (scraper.fetch_data) must be a callable
            # The results are yielded in the order the calls were submitted
            futures = executor.map(scraper.fetch_data, self.urls)
            
            # Collect results from the futures
            for products_list in futures:
                if products_list:
                    all_results.extend(products_list)
                    
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"[TEST 1: I/O (Threads)] Scraped {len(all_results)} products in {duration:.4f}s")
        return all_results
            
    # Corrected with actual ProcessPoolExecutor            
    # Inside ConcurrentManager class
    def run_analyzer(self, data: List[ProductData], executor_type='Process'):
        # We must pass the data *to* the pool to be worked on.
        analyzer = DataAnalyzer(data)
        
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
            
    def main(self, urls:List[str]):
        self.run_scraper()
        self.run_analyzer()
        
        
# Refactored __main__ 
if __name__ == "__main__":
    test_urls = [
        "https://www.jumia.com.ng/televisions/#catalog-listing"
        # Add more URLs if you can find them to increase I/O load
    ] * 2 # Duplicate to increase load for better threading demo

    # Initialize Manager
    manager = ConcurrentManager(test_urls)

    # =========================================================================
    # TEST 1: I/O BOUND TASK with THREADS (Expected: FAST - GIL is released)
    # =========================================================================
    print("\n--- RUNNING TEST 1: I/O (Scraper) with THREADS ---")
    all_products = manager.run_scraper()
    
    if not all_products:
        print("ERROR: Scraper failed to fetch data. Cannot proceed with analysis tests.")
        exit()

    print(f"\nTOTAL PRODUCTS COLLECTED: {len(all_products)}")
    print("-" * 60)

    # =========================================================================
    # TEST 2: CPU BOUND TASK with PROCESSES (Expected: FAST - GIL is bypassed)
    # =========================================================================
    print("\n--- RUNNING TEST 2: CPU (Analyzer) with PROCESSES ---")
    duration_process = manager.run_analyzer(all_products, executor_type='Process')

    # =========================================================================
    # TEST 3: CPU BOUND TASK with THREADS (Expected: SLOW - GIL holds one core)
    # =========================================================================
    print("\n--- RUNNING TEST 3: CPU (Analyzer) with THREADS (GIL Demo) ---")
    duration_thread = manager.run_analyzer(all_products, executor_type='Thread')

    # =========================================================================
    # CONCLUSION
    # =========================================================================
    print("\n" + "=" * 60)
    print("                 GIL DEMONSTRATION RESULTS")
    print("=" * 60)
    print(f"Analyzer (Processes): {duration_process:.4f}s (Bypassed GIL)")
    print(f"Analyzer (Threads):   {duration_thread:.4f}s (Limited by GIL)")
    
    if duration_thread > duration_process * 0.9: # Simple check
        print("\n✅ **DEMONSTRATION SUCCESSFUL**")
        print("The thread duration is significantly longer because the GIL prevented true parallel execution on the CPU-bound task.")
    else:
        print("\n⚠️ **DEMONSTRATION FAILED**")
        print("The CPU-bound work in the Analyzer needs to be made much more intensive (increase 'n' in the loop) to hold the GIL for longer.")