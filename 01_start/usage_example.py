"""
Price Tracker Usage Examples
Complete examples showing how to use the price tracker tool
"""

from price_tracker import (
    USPSScraper, 
    GenericHTMLScraper,
    GoogleSheetsHandler,
    PriceComparator,
    PriceRecord
)
import pandas as pd
from datetime import datetime


# ============================================================================
# EXAMPLE 1: Basic USPS Price Scraping
# ============================================================================

def example_1_basic_scraping():
    """Simple example: scrape USPS and display results"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Price Scraping")
    print("=" * 60)
    
    # Create scraper
    scraper = USPSScraper()
    
    # Scrape current prices
    current_prices = scraper.scrape()
    
    # Display results
    print(f"\nFound {len(current_prices)} pricing records:\n")
    for record in current_prices:
        print(f"  {record.product_name:45} ${record.price:7.2f}")


# ============================================================================
# EXAMPLE 2: Full Workflow with Google Sheets
# ============================================================================

def example_2_full_workflow():
    """Complete workflow: scrape, compare, report, and save"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Complete Workflow with Google Sheets")
    print("=" * 60)
    
    # Step 1: Scrape current prices
    print("\n[1] Scraping current prices from USPS...")
    scraper = USPSScraper()
    current_prices = scraper.scrape()
    print(f"    ✓ Found {len(current_prices)} records")
    
    # Step 2: Connect to Google Sheets
    print("\n[2] Connecting to Google Sheets...")
    sheets_handler = GoogleSheetsHandler(
        credentials_file='credentials.json',  # Update this path
        sheet_url='YOUR_SHEET_URL_HERE'       # Update this URL
    )
    sheets_handler.connect()
    print("    ✓ Connected successfully")
    
    # Step 3: Read baseline data
    print("\n[3] Reading baseline pricing data...")
    baseline_df = sheets_handler.read_baseline()
    print(f"    ✓ Loaded {len(baseline_df)} baseline records")
    
    # Step 4: Compare prices
    print("\n[4] Comparing current vs baseline prices...")
    comparison = PriceComparator.compare(current_prices, baseline_df)
    print("    ✓ Comparison complete")
    
    # Step 5: Generate report
    print("\n[5] Generating change report...")
    report = PriceComparator.generate_report(comparison)
    print(report)
    
    # Step 6: Save results to Google Sheets
    print("\n[6] Saving results to Google Sheets...")
    sheets_handler.write_comparison(
        comparison, 
        worksheet_name=f"Comparison_{datetime.now().strftime('%Y%m%d')}"
    )
    print("    ✓ Results saved")
    
    return comparison


# ============================================================================
# EXAMPLE 3: Manual Baseline (No Google Sheets Required)
# ============================================================================

def example_3_manual_baseline():
    """Use manual baseline data instead of Google Sheets"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Comparison with Manual Baseline")
    print("=" * 60)
    
    # Create manual baseline data
    baseline_data = pd.DataFrame([
        {
            'product_name': 'USPS Small Flat Rate Box (Retail)',
            'size': '8-11/16 × 5-7/16 × 1-3/4 in',
            'baseline_price': 10.25,  # Old price
            'carrier': 'USPS'
        },
        {
            'product_name': 'USPS Medium Flat Rate Box (Retail)',
            'size': '11-1/4 × 8-3/4 × 6 in',
            'baseline_price': 17.20,  # Old price
            'carrier': 'USPS'
        },
        {
            'product_name': 'USPS Large Flat Rate Box (Retail)',
            'size': '12 × 12-1/4 × 6 in',
            'baseline_price': 24.70,  # Old price
            'carrier': 'USPS'
        }
    ])
    
    # Scrape current prices
    scraper = USPSScraper()
    current_prices = scraper.scrape()
    
    # Filter to retail only for this example
    retail_prices = [p for p in current_prices if 'Retail' in p.product_name]
    
    # Compare
    comparison = PriceComparator.compare(retail_prices, baseline_data)
    
    # Generate and print report
    report = PriceComparator.generate_report(comparison)
    print(report)
    
    # Show detailed comparison
    print("\n\nDetailed Comparison:")
    print(comparison[['product_name', 'baseline_price', 'current_price', 
                     'price_diff', 'price_diff_pct', 'status']].to_string())


# ============================================================================
# EXAMPLE 4: Custom Website Scraper Configuration
# ============================================================================

def example_4_custom_scraper():
    """Configure scraper for a custom website"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Custom Website Scraper")
    print("=" * 60)
    
    # Example: Scraping a hypothetical shipping company website
    # You would customize these selectors based on the actual website structure
    
    custom_scraper = GenericHTMLScraper(
        url='https://example-shipping.com/rates',
        selectors={
            'container': 'div.rate-card',           # Container for each product
            'product_name': 'h3.service-name',      # Product/service name
            'price': 'span.price-amount',           # Price element
            'size': 'div.dimensions'                # Size/dimensions (optional)
        }
    )
    
    print("\nScraper configured for: https://example-shipping.com/rates")
    print("\nSelectors:")
    print("  • Container: div.rate-card")
    print("  • Product:   h3.service-name")
    print("  • Price:     span.price-amount")
    print("  • Size:      div.dimensions")
    
    # To actually scrape (uncomment when using a real website):
    # prices = custom_scraper.scrape()
    # for record in prices:
    #     print(f"  {record.product_name}: ${record.price:.2f}")


# ============================================================================
# EXAMPLE 5: Multi-Carrier Comparison
# ============================================================================

def example_5_multi_carrier():
    """Compare prices across multiple carriers"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Multi-Carrier Price Comparison")
    print("=" * 60)
    
    # Scrape USPS
    usps_scraper = USPSScraper()
    usps_prices = usps_scraper.scrape()
    
    # In a real implementation, you would also scrape FedEx and UPS
    # For demonstration, creating sample data
    
    fedex_prices = [
        PriceRecord("FedEx Small Box", "12 × 10 × 2 in", 9.95, "FedEx"),
        PriceRecord("FedEx Medium Box", "13 × 11 × 3 in", 15.50, "FedEx"),
        PriceRecord("FedEx Large Box", "18 × 12 × 3 in", 22.00, "FedEx"),
    ]
    
    ups_prices = [
        PriceRecord("UPS Small", "12 × 9 × 6 in", 11.25, "UPS"),
        PriceRecord("UPS Medium", "16 × 12 × 8 in", 18.50, "UPS"),
        PriceRecord("UPS Large", "20 × 16 × 12 in", 26.75, "UPS"),
    ]
    
    # Combine all prices
    all_prices = usps_prices + fedex_prices + ups_prices
    
    # Create comparison DataFrame
    df = pd.DataFrame([
        {
            'Carrier': r.source.split()[0],
            'Service': r.product_name,
            'Size': r.size,
            'Price': r.price
        } for r in all_prices
    ])
    
    # Group by approximate size category
    print("\nPrice Comparison by Size:\n")
    
    # Small boxes
    print("SMALL BOXES (~12×9×6 in):")
    small = df[df['Service'].str.contains('Small', case=False)]
    for _, row in small.iterrows():
        print(f"  {row['Carrier']:6} {row['Service']:40} ${row['Price']:7.2f}")
    
    # Medium boxes
    print("\nMEDIUM BOXES (~16×12×8 in):")
    medium = df[df['Service'].str.contains('Medium', case=False)]
    for _, row in medium.iterrows():
        print(f"  {row['Carrier']:6} {row['Service']:40} ${row['Price']:7.2f}")
    
    # Large boxes
    print("\nLARGE BOXES (~20×16×12 in):")
    large = df[df['Service'].str.contains('Large', case=False)]
    for _, row in large.iterrows():
        print(f"  {row['Carrier']:6} {row['Service']:40} ${row['Price']:7.2f}")


# ============================================================================
# EXAMPLE 6: Automated Monitoring Script
# ============================================================================

def example_6_monitoring_script():
    """Example of automated daily monitoring"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Automated Monitoring Script")
    print("=" * 60)
    
    print("""
This example shows how to set up automated monitoring.
You would run this as a scheduled job (cron, Task Scheduler, etc.)

Sample cron job (runs daily at 6 AM):
    0 6 * * * /usr/bin/python3 /path/to/monitor_prices.py

Script structure:
""")
    
    monitoring_code = '''
#!/usr/bin/env python3
import sys
from datetime import datetime
from price_tracker import *

def monitor_prices():
    try:
        # Scrape current prices
        scraper = USPSScraper()
        current = scraper.scrape()
        
        # Load baseline
        sheets = GoogleSheetsHandler('creds.json', 'SHEET_URL')
        baseline = sheets.read_baseline()
        
        # Compare
        comparison = PriceComparator.compare(current, baseline)
        
        # Check for changes
        changes = comparison[comparison['status'] != 'UNCHANGED']
        
        if not changes.empty:
            # Generate alert
            report = PriceComparator.generate_report(comparison)
            
            # Send email notification (pseudo-code)
            send_email(
                to='admin@company.com',
                subject=f'Price Alert: {len(changes)} changes detected',
                body=report
            )
            
            # Update Google Sheets
            sheets.write_comparison(comparison, 
                f"Alert_{datetime.now().strftime('%Y%m%d_%H%M')}")
        
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(monitor_prices())
'''
    
    print(monitoring_code)


# ============================================================================
# MAIN: Run All Examples
# ============================================================================

def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "    PRICE TRACKER - COMPREHENSIVE USAGE EXAMPLES    ".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Example 1: Basic scraping
    example_1_basic_scraping()
    
    # Example 2: Full workflow (requires Google Sheets setup)
    # Uncomment when you have Google Sheets configured:
    # example_2_full_workflow()
    
    # Example 3: Manual baseline (no Google Sheets needed)
    example_3_manual_baseline()
    
    # Example 4: Custom scraper
    example_4_custom_scraper()
    
    # Example 5: Multi-carrier comparison
    example_5_multi_carrier()
    
    # Example 6: Monitoring script template
    example_6_monitoring_script()
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Set up Google Sheets with baseline data")
    print("2. Configure Google Sheets API credentials")
    print("3. Customize scrapers for additional carriers (FedEx, UPS)")
    print("4. Set up automated monitoring")
    print("5. Add email/Slack notifications for price changes")


if __name__ == "__main__":
    main()
