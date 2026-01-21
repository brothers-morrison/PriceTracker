import sys
import os
sys.path.append(os.path.dirname(__file__))  # Ensure price_tracker.py can be imported from the same directory

from price_tracker import USPSScraper

def main():
    # Create an instance of the USPS scraper
    scraper = USPSScraper()
    
    # Scrape the prices
    records = scraper.scrape()
    
    # Print the results
    print("Scraped USPS Flat Rate Pricing:")
    for record in records:
        print(f"- {record.product_name}: ${record.price}")

if __name__ == "__main__":
    main()
