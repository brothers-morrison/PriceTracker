import sys
import os
sys.path.append(os.path.dirname(__file__))  # Ensure price_tracker.py can be imported from the same directory

from price_tracker import GenericHTMLScraper

def main():
    # Define a hypothetical URL and selectors for a custom website (e.g., a shipping site)
    url = "https://example-shipping-site.com/prices"  # Replace with a real URL in practice
    selectors = {
        "product_container": ".product-item",  # CSS selector for product containers
        "product_name": ".product-name",       # Selector for product name within container
        "price": ".price"                     # Selector for price within container
    }
    
    # Create the custom scraper
    scraper = GenericHTMLScraper(url=url, selectors=selectors)
    
    # Scrape the prices
    records = scraper.scrape()
    
    # Print the results
    print("Scraped Custom Website Pricing:")
    for record in records:
        print(f"- {record.product_name}: ${record.price}")

if __name__ == "__main__":
    main()
