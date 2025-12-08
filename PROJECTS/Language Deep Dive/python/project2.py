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
    
    def calculate_statistics(self):
        # 1. I need to first iterate through the entire scraped dataset
        
        prices = 0
        
        for product in self.data:
            # I need to begin calculating statistics like: mean price, median price, price standard deviation
            prices += product.price
            
        # Mean Price:
        mean_price = numpy.mean(prices)

        # Median Price:
        median_price = numpy.median(prices)
        
        # Price Standard Deviation:
        sd_price = numpy.std(prices)
        
        
        print(f"Mean Prices: {mean_price}")
        print(f"Median Prices: {median_price}")
        print(f"Prices Standard Deviation: {sd_price}")
       
       
# ConcurrentManager Class (The Orchestrator)
# Purpose: Manages the flow, decides on the concurrency model, and collects results.
# Methods:run_scraper(self, urls): Uses concurrent.futures.ThreadPoolExecutor to execute the ProductScraper.fetch_data method for all URLs concurrently.
# run_analyzer(self, data): Uses concurrent.futures.ProcessPoolExecutor or the multiprocessing module to run the DataAnalyzer.calculate_statistics method.
# main(self, urls): The entry point that orchestrates the entire flow: Scrape -> Analyze -> Report. 

MAX_WORKERS = 5

class ConcurrentManager():
    def __init__(self, urls: List[str]):
        self.urls = urls
        
    def run_scraper(self, url:List[str]):
        start_time = time.perf_counter()
        ThreadPoolExecutor(MAX_WORKERS, "Product scraper", ProductScrapper.fetch_data(url))
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"Ran scraper for {duration:.4f}s")
            
    def run_analyzer(self, data:List[str]):
        start_time = time.perf_counter()
        ProcessPoolExecutor(MAX_WORKERS, initializer=DataAnalyzer.calculate_statistics())
        end_time = time.perf_counter()
        duration = end_time - start_time
        print(f"Ran analyzer for {duration:.4f}s")
        
    def main(self, urls:List[str]):
        self.run_scraper()
        self.run_analyzer()
        
        
if __name__ == "__main__":
    # Create a list of URLs to scrape
    test_urls = [
        "https://www.jumia.com.ng/televisions/#catalog-listing",
    ]
    
    scraper = ProductScrapper(test_urls)
    all_products = []  # Collect all products from all URLs
    
    for url in test_urls:
        products_data = scraper.fetch_data(url)  # Now returns a list
        if products_data:
            all_products.extend(products_data)
            print(f"\n[Main] Scraped {len(products_data)} products from {url}")
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"TOTAL PRODUCTS COLLECTED: {len(all_products)}")
    print(f"{'='*60}")
    
    # Show first few products
    for i, product in enumerate(all_products[:5], 1):
        print(f"{i}. {product.title[:60]}...")
        print(f"   Price: ₦{product.price:,.2f}")
        print(f"   URL: {product.url[:80]}...")
        print("=" * 40)

    scraped = DataAnalyzer(data=all_products)
    print(scraped.calculate_statistics())