import sys
import os
sys.path.append(os.path.dirname(__file__))  # Ensure price_tracker.py can be imported from the same directory

from price_tracker import USPSScraper, DatabaseHandler, PriceComparator, GoogleSheetsHandler
import pandas as pd

def main():
    # Step 1: Scrape current prices
    scraper = USPSScraper()
    current_records = scraper.scrape()
    
    # Step 2: Store in database
    db_handler = DatabaseHandler(db_path='example_price_tracker.db')
    db_handler.store_results(current_records)
    
    # Step 3: Load baseline from a mock Google Sheets (using a placeholder; in real use, provide credentials)
    # For simulation, we'll create a mock baseline DataFrame instead of connecting to Google Sheets
    mock_baseline = pd.DataFrame({
        'product_name': ['Priority Mail Flat Rate Box - Small', 'Priority Mail Flat Rate Box - Medium'],
        'price': [8.50, 14.50]  # Mock baseline prices
    })
    
    # Step 4: Compare current with baseline
    comparison_df = PriceComparator.compare(current_records, mock_baseline)
    
    # Step 5: Generate and print a report
    report = PriceComparator.generate_report(comparison_df)
    print("Full Workflow Report:")
    print(report)

if __name__ == "__main__":
    main()
