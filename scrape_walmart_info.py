from bs4 import BeautifulSoup
import threading
import requests

visited_urls = set()
lock = threading.Lock()
urls_to_crawl = []
max_threads = 5  # Number of threads to use for scraping
total_pages = int(input('Enter the number of pages to scrape (up to 25): '))  # Number of pages to scrape


def fetch_url(url):
    global visited_urls
    headers = {
        'User-Agent': 'Your User Agent String'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Example: Scraping products and prices
            products = soup.find_all('span', {'data-automation-id': 'product-title'})
            product_texts = [product.get_text() for product in products]
            print(product_texts)
            prices = soup.find_all('div', {'data-automation-id': 'product-price'})
            price_texts = []
            for price in prices:
                dollar_sign = price.find('span', class_='f6 f5-l').get_text() if price.find('span', class_='f6 f5-l') else ''
                dollars = price.find('span', class_='f2').get_text() if price.find('span', class_='f2') else ''
                cents = price.find('span', class_='f6 f5-l', style="vertical-align:0.75ex").get_text() if price.find('span', class_='f6 f5-l', style="vertical-align:0.75ex") else ''
                price_text = f"{dollar_sign}{dollars}.{cents}"
                price_texts.append(price_text)

            print(f"Scraped URL: {url}")
            print("Page Products:")
            for i in range(len(product_texts)):
                print(f"Product: {product_texts[i]}")
                print(f"Price: {price_texts[i]}")
            print('\n')
            # Add the URL to the visited set
            with lock:
                visited_urls.add(url)
        else:
            print(f"Failed to fetch data from URL: {url}")
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")

def crawl(thread_label):
    global urls_to_crawl
    while True:
        with lock:
            if not urls_to_crawl:
                break
            current_url = urls_to_crawl.pop(0)
        if current_url not in visited_urls:
            fetch_url(current_url)
            print(f"{thread_label} is processing URL: {current_url}")

def generate_urls(base_url):
    if not base_url.endswith('?page='):
        base_url = base_url + '?page='

    for page_number in range(1, total_pages + 1):
        url = f"{base_url}{page_number}"
        urls_to_crawl.append(url)

# Asking for user input and storing it in a variable
# start_url = input("Enter the base url to start from: ")

# base_url = 'https://www.walmart.com/browse/electronics/shop-all-headphones-by-type/3944_133251_1095191_1230614_4480?page='
base_url = 'https://www.walmart.com/browse/home/shop-microwaves/4044_90548_90546_132950_8874548'
generate_urls(base_url)

threads = []
for i in range(max_threads):
    thread = threading.Thread(target=crawl, args=(f"Thread {i+1}",))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("All pages scraped.")
