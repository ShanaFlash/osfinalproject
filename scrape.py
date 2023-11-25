import multiprocessing
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import threading
import requests

def scrape_products(page_num):
    # Example HTML content (replace this with your actual HTML content)
    url = f'https://www.walmart.com/browse/electronics/apple-airpods/3944_133251_1095191_1231498_2452446??page={page_num}'

    headers = {
        'User-Agent': 'Your User Agent String'  # Update with your User Agent
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Example: Scraping quotes
        products = soup.find_all('span', {'data-automation-id': 'product-title'})  # Adjust class names as per the website
        product_texts = [product.get_text() for product in products]
        print(f"Page {page_num} Products:")
        print(product_texts)
    else:
        print(f"Failed to fetch data from page {page_num}")

# Extracting the dollar sign, price, and cents
# dollar_sign = soup.find('span', {'class': 'f6 f5-l'}).get_text()
# price = soup.find('span', {'class': 'f2'}).get_text()
# cents = soup.find_all('span', {'class': 'f6 f5-l'})[1].get_text()

# # Concatenating the price, cents, and dollar sign
# full_price = f"{dollar_sign}{price}{cents}"

# Extracting the product title
# title_element = soup.find('span', {'data-automation-id': 'product-title'})
# title = title_element.get_text()

# print("Full Price:", full_price)

# Create and start threads for each page
num_pages = 2
threads = []
for page in range(1, num_pages + 1):
    thread = threading.Thread(target=scrape_products, args=(page,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All pages scraped.")
# print("Title:", title)
