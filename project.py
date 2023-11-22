import multiprocessing
from bs4 import BeautifulSoup
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse
import threading
import requests

# Function to scrape headlines from Google News
def scrape_google_news():
    url = 'https://news.google.com/'
    headers = {
        'User-Agent': 'Your User Agent String'  # Update with your User Agent
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Example: Scraping headlines
        headlines = soup.find_all('h4', {'class': ['gPFEn', 'JtKRv', 'JtKRv vDXQhc']})
        news_headlines = [headline.get_text() for headline in headlines]
        print("Headlines:")
        print(news_headlines)
    else:
        print("Failed to fetch data from Google News")

# Define the number of threads (pages) to scrape
num_threads = 3

# Create and start threads
threads = []
for _ in range(num_threads):
    thread = threading.Thread(target=scrape_google_news)
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All threads completed.")