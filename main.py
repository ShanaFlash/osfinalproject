def option_one():
    print("Option 1 - Running scrape_walmart_info.py")
    import scrape_walmart_info  # Import code from scrape_walmart_info.py

def option_two():
    print("Option 2 - Running scrape_urls.py")
    import scrape_urls  # Import code from scrape_urls.py

def main():
    while True:
        print("Choose an option:")
        print("1. Scrape prices")
        print("2. Scrape urls")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            option_one()  # Call function for option one (run scrape.py)
            break
        elif choice == '2':
            option_two()  # Call function for option two (run scrape_urls.py)
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
