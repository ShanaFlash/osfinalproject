# osfinalproject
Project demo: 
https://docs.google.com/presentation/d/1im-X7AcmUpr7kQz1RLnEaNOyPpzcsM2KTWoiW4Vrm0Q/edit?usp=sharing

How to Run?
1.Prefer Run it at Replit: https://replit.com/@JeniferNguyen/osproject#main.py

2.Run it at VSCode, but need to configure required library first.

Project name:
Multithreaded Web Crawler for Price-Monitoring
explain the project in one paragraph
Our project is a Python-based web crawler designed for efficient price monitoring on e-commerce sites. It employs multithreading and concurrent execution to navigate through product pages and extract price information. This tool can be used by both consumers and businesses. Consumers will be able to get real-time insight into product pricing to make informed decisions about their purchases, while e-commerce businesses can utilize this web crawler to get insights into their competitors' pricing strategies to make adjustments to their own business strategies.

What is input and output?
The input for our web crawler is a seed URL of an e-commerce site. The web crawler explores the site to extract URLs of product pages and parses the HTML content. The input is also the option that the user chooses, like the user presses 1 to resume the last session, 2 to start a new session, at which point, the program asks for a starting url, or the program will listen for the user to enter 0 to terminate the program.
The expected output is the product names, their current prices, a csv file with the information, and another csv file with all of the urls that were scraped. 
What is the current status of progress on your project? and How far along are you in completing your project?
We currently have a functional base code for our project. We utilized ThreadPoolExecutor for concurrent execution and BeautifulSoup to streamline web crawling and ensure responsiveness. The web crawler also populates a set of scraped pages to avoid redundant processing, enhancing efficiency in subsequent runs. The team is currently focused on testing, debugging, and refining the code.
The code can remember urls by putting visited urls into a csv file and continuing on from the last line by reading the latest csv file made. However, while dynamically scraping urls off of the site, starting from the given page, pages on the site that don’t have products and prices, like the Careers page, also get scraped and checked for prices. So this bug needs to be fixed.
We are also about to test out how to put the product names and prices into the csv file.

