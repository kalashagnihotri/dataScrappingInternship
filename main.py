from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode

# Set up the Chrome driver
executable_path = r'C:\src\things\chromedriver-win64\chromedriver-win64\chromedriver.exe'
service = Service(executable_path=executable_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Base URL of the Amazon page
def get_amazon_data(url):
    driver.get(url)
    time.sleep(5)  # Allow page to load
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

# Extract rating from class name
def extract_rating(class_name):
    if not class_name:
        return "No Rating"
    for cls in class_name:
        if 'a-star-small-' in cls:
            return cls.replace('a-star-small-', '').replace('-', '.')
    return "No Rating"

# Extract seller name from product page
def get_seller_name(product_url):
    try:
        driver.get(product_url)
        time.sleep(3)  # Allow page to load
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        seller_element = soup.find('a', {'id': 'sellerProfileTriggerId'})
        return seller_element.text.strip() if seller_element else "Unknown Seller"
    except Exception as e:
        print(f"Error getting seller: {e}")
        return "Unknown Seller"

# List to store all product details
product_details = []

# Initial URL
base_url = "https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar"

# Determine the number of pages dynamically
soup = get_amazon_data(base_url)
pagination = soup.find('span', {'class': 's-pagination-item s-pagination-disabled'})

# if you want to use max pages then just put it in the range
max_pages = int(pagination.text) if pagination else 1

# Loop through specific pages that you will input
for page in range(1, 2):  # Change the range to scrape more pages
    print(f"Scraping page {page}...")
    soup = get_amazon_data(base_url + f'&page={page}')
    
    # Find all product containers
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for product in products:
        try:
            # Extract product name
            name = product.find('h2', {'class': 'a-size-base-plus a-spacing-none a-color-base a-text-normal'}).text.strip()
            
            # Extract price
            price_element = product.find('span', {'class': 'a-price-whole'})
            price = price_element.text.strip() if price_element else 'Out of Stock'
            
            # Extract rating
            rating_element = product.find('i', {'class': 'a-icon-star-small'})
            rating_class = rating_element.get('class') if rating_element else None
            rating = extract_rating(rating_class)
            
            # Extract product URL
            product_link_element = product.find('a', {'class': 'a-link-normal s-no-outline'})
            product_url = "https://www.amazon.in" + product_link_element['href'] if product_link_element else None
            
            # Extract seller name if product URL is available
            seller_name = get_seller_name(product_url) if product_url else "Unknown Seller"
            
            # Append the details to the list
            product_details.append([name, price, rating, seller_name])
            
            # Print the extracted data to the terminal
            print(f"Product Name: {name}")
            print(f"Price: {price}")
            print(f"Rating: {rating}")
            print(f"Seller: {seller_name}")
            print("-" * 50)  # Separator for readability
        except AttributeError as e:
            print(f"Skipping a product due to error: {e}")
            continue

# Close the browser
driver.quit()

# Save to CSV
with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product Name', 'Price', 'Rating', 'Seller'])
    writer.writerows(product_details)

print("Scraping completed and data saved to 'amazon_products.csv'")