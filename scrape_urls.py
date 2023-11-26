from bs4 import BeautifulSoup
import threading
import requests
import csv
import sys
import os

visited_urls = set()
lock = threading.Lock()
urls_to_crawl = []
terminate_flag = False
file_name = 'scraped_urls.csv'

def fetch_url(url, thread_id):
    global visited_urls, urls_to_crawl, terminate_flag
    headers = {
        'User-Agent': 'Your User Agent String'
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"Thread {thread_id} - Scraped URL: {url}")
            
            # Extract new URLs dynamically and add them to urls_to_crawl
            new_urls = [link['href'] for link in soup.find_all('a', href=True)]
            for new_url in new_urls:
                if new_url not in visited_urls and new_url not in urls_to_crawl:
                    urls_to_crawl.append(new_url)
            
            # Add the URL to the visited set
            with lock:
                visited_urls.add(url)
        else:
            print(f"Thread {thread_id} - Failed to fetch data from URL: {url}")
    except Exception as e:
        print(f"Thread {thread_id} - Error fetching URL {url}: {e}")

def get_latest_valid_url(file_name):
    latest_url = None
    try:
        with open(file_name, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)  # Read all rows into a list
            for row in reversed(rows):  # Traverse rows in reverse order
                url = row[0]
                if url.startswith('https://') and not (url.endswith('.pdf') or url.endswith('.doc') or url.startswith('https://us06web.zoom.us')):
                    latest_url = url
                    break  # Found the latest valid URL, no need to continue
    except FileNotFoundError:
        pass  # File not found, no need to resume, start from scratch
    
    # print('Latest url:', latest_url)
    
    return latest_url


def crawl(start_url, thread_id):
    global file_name
    urls_to_crawl.append(start_url)
    
    if file_name != 'scraped_urls.csv':
        latest_url = get_latest_valid_url(file_name)
        if latest_url:
            urls_to_crawl.append(latest_url)

    while urls_to_crawl and not terminate_flag:
        current_url = urls_to_crawl.pop(0)
        if current_url not in visited_urls:
            fetch_url(current_url, thread_id)
            if file_name.startswith('scraped_urls_'):
                with lock:
                    with open(file_name, 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([current_url])
            else:
                with lock:
                    with open(file_name, 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow([current_url])

def get_latest_scraped_file():
    # print("test")
    latest_file = 'scraped_urls.csv'
    file_numbers = []
    for file in os.listdir():
        if file.startswith('scraped_urls_') and file.endswith('.csv'):
            parts = file.split('_')
            if len(parts) == 3 and parts[2].split('.')[0].isdigit():
                file_numbers.append(int(parts[2].split('.')[0]))
    if file_numbers:
        latest_file_number = max(file_numbers)
        latest_file = f'scraped_urls_{latest_file_number}.csv'
    # print("latest file:", latest_file)
    return latest_file



def resume_or_start():
    try:
        choice = int(input("Enter '1' to resume from the last session or '2' to start a new session: "))
        if choice == 1:
            return get_latest_scraped_file(), get_latest_valid_url(get_latest_scraped_file())
        elif choice == 2:
            file_number = 1
            while os.path.exists(f'scraped_urls_{file_number}.csv'):
                file_number += 1
            new_file_name = f'scraped_urls_{file_number}.csv'
            return new_file_name, input("Enter the starting URL: ")
        elif choice == 0:
            return None, None
        else:
            print("Invalid choice.")
            return None, None
    except ValueError:
        print("Invalid input.")
        return None, None

# Asking for user input
start_url = None
while start_url is None:
    file_name, start_url = resume_or_start()
    if file_name is None:
        terminate_flag = True
        break

if not terminate_flag:
    NUM_THREADS = 5
    threads = []
    for i in range(NUM_THREADS):
        thread = threading.Thread(target=crawl, args=(start_url, i + 1))
        threads.append(thread)
        thread.start()

    try:
        while True:
            command = input("Press '0' to terminate: ")
            if command == '0':
                terminate_flag = True
                break
    except KeyboardInterrupt:
        terminate_flag = True

    for thread in threads:
        thread.join()

print("All pages scraped.")