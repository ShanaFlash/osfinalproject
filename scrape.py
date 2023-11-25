from bs4 import BeautifulSoup
import threading
import requests

visited_urls = set()
lock = threading.Lock()
urls_to_crawl = []

def fetch_url(url):
    global visited_urls, urls_to_crawl
    headers = {
        'User-Agent': 'Your User Agent String'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Example: Scraping products
            products = soup.find_all('span', {'data-automation-id': 'product-title'})
            product_texts = [product.get_text() for product in products]
            print(f"Scraped URL: {url}")
            print("Page Products:")
            print(product_texts)
            
            # Extract new URLs dynamically and add them to urls_to_crawl
            new_urls = [link['href'] for link in soup.find_all('a', href=True)]
            for new_url in new_urls:
                if new_url not in visited_urls and new_url not in urls_to_crawl:
                    urls_to_crawl.append(new_url)
            
            # Add the URL to the visited set
            with lock:
                visited_urls.add(url)
        else:
            print(f"Failed to fetch data from URL: {url}")
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")

def crawl(start_url):
    global urls_to_crawl
    urls_to_crawl.append(start_url)
    
    while urls_to_crawl:
        current_url = urls_to_crawl.pop(0)
        if current_url not in visited_urls:
            fetch_url(current_url)

# Asking for user input and storing it in a variable
start_url = input("Enter the url to start from: ")

# start_url = 'https://www.walmart.com/browse/electronics/apple-airpods/3944_133251_1095191_1231498_2452446??page=1'
crawl(start_url)
print("All pages scraped.")

