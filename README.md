# Walmart_Product_Scraper
Walmart Product Scraper
This project is a Python-based web scraper that uses Selenium and undetected-chromedriver to scrape product information from Walmart's online store. The scraper collects product details like name and price and saves the data to a JSON file. It also handles pagination to scrape multiple pages of products.

Features
Scrapes product names and prices from Walmart's search results.
Automatically scrolls the page to load more products.
Handles pagination and navigates to the next page of results.
Saves the scraped data in a structured JSON file.
Uses undetected-chromedriver to bypass detection mechanisms, ensuring a smooth scraping experience.
Prerequisites
To run this scraper, you need:

Python 3.x
Chrome Browser (latest version)
pip to install Python dependencies
Installation
Clone this repository to your local machine:

Install the required Python libraries using pip:

pip install -r requirements.txt

The required libraries include undetected-chromedriver, selenium, webdriver-manager, json, time, and os.

Usage
Open the walmart_product_scraper.py script.

Replace the target URL in driver.get("https://www.walmart.com/search?q=snacks&typeahead=sn") with the Walmart search URL you want to scrape.

Run the script:

python walmart_product_scraper.py

The script will start scraping products, saving the product names and prices to a walmart_products.json file.

It will continue scraping through multiple pages (pagination) until there are no more pages or an error occurs.

Scraping Flow
The script starts by scraping the current page for product information. It waits for the "Next Page" button to become clickable. Once the button is clickable, it scrolls the button into view and clicks it to navigate to the next page. The process repeats until there are no more pages to scrape.

Notes:
The scraper uses undetected-chromedriver to avoid being blocked by Walmart's anti-scraping mechanisms.
The script uses an explicit wait to ensure that the next page button is visible and clickable before proceeding.
Troubleshooting
element click intercepted error: This typically happens when another element (like the search bar) is blocking the "Next Page" button. The script now handles this by scrolling the button into view and clicking it using JavaScript.
No more products to scrape: If the script cannot find any more products or fails to navigate to the next page, it will stop scraping.


This version is in plain text for easy copy-pasting to your GitHub repository.
