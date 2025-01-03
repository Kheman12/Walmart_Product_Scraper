import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import json
import os

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("start-maximized")

# Set a custom User-Agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")

# Set up undetected-chromedriver with the correct driver using webdriver-manager
service = Service(ChromeDriverManager().install())
driver = uc.Chrome(service=service, options=chrome_options)
driver.get("https://www.walmart.com/search?q=snacks&typeahead=sn")  # Replace with the target URL

def scrape_items(driver):
    data = []
    
    # Wait for the page to load and ensure product elements are present
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='group']")))

    # Scroll down the page to ensure all products load
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for more products to load
        
        # Check if the height has increased, indicating more products loaded
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    # Get all product elements on the page
    items = driver.find_elements(By.CSS_SELECTOR, "div[role='group']")
    
    if not items:
        print("No products found on this page.")
        return data  # Return empty data if no products are found
    
    for item in items:
        try:
            # Extract product name and price using CSS Selectors
            name = item.find_element(By.CSS_SELECTOR, "span[data-automation-id='product-title']").text
            price = item.find_element(By.CSS_SELECTOR, "div.flex.flex-wrap.justify-start.items-center.lh-title.mb1 span.w_iUH7").text

            data.append({"Product Name": name, "Price": price})
        except Exception as e:
            print(f"Error extracting data for item: {e}")
    
    # Save the scraped data to a JSON file
    try:
        output_file = 'walmart_products.json'
        
        # If the file exists, append new data
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                existing_data = json.load(f)
            existing_data.extend(data)
            data = existing_data
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {output_file}")
        
    except PermissionError as e:
        print(f"Permission error while writing to file: {e}")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")
    
    return data  # Return scraped data

# Scrape the first page and navigate to the next page
# Scrape the first page and navigate to the next page
try:
    while True:
        # Scrape items on the current page
        scrape_items(driver)
        
        # Try to find and click the "Next" button to navigate to the next page
        try:
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="NextPage"]'))
            )
            
            # Scroll the "Next Page" button into view
            driver.execute_script("arguments[0].scrollIntoView();", next_button)
            
            # Wait to ensure it's fully in view
            time.sleep(1)
            
            # Use JavaScript to click the "Next" button
            driver.execute_script("arguments[0].click();", next_button)
            print("Navigating to the next page...")
            time.sleep(5)  # Allow time for the next page to load
            
        except Exception as e:
            print(f"Error navigating to next page: {e}")
            break  # Stop if no "Next" button is found or an error occurs
    
finally:
    # Ensure the driver is properly quit when done
    try:
        driver.quit()
    except Exception as e:
        print(f"Error quitting driver: {e}")



