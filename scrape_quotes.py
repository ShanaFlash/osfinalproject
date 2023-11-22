import multiprocessing
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import threading
import requests

# Function to scrape quotes from a website
def scrape_quotes(page_num):
    url = f'http://quotes.toscrape.com/page/{page_num}/'
    headers = {
        'User-Agent': 'Your User Agent String'  # Update with your User Agent
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Example: Scraping quotes
        quotes = soup.find_all('span', class_='text')  # Adjust class names as per the website
        quote_texts = [quote.get_text() for quote in quotes]
        print(f"Page {page_num} Quotes:")
        print(quote_texts)
    else:
        print(f"Failed to fetch data from page {page_num}")

# Define the number of pages to scrape
num_pages = 5  # Scraping five pages

# Create and start threads for each page
threads = []
for page in range(1, num_pages + 1):
    thread = threading.Thread(target=scrape_quotes, args=(page,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All pages scraped.")