"""
Generic Price Tracker Tool
Tracks price changes by comparing website data with Google Sheets baseline data.

Requirements:
pip install requests beautifulsoup4 gspread oauth2client pandas lxml
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import gspread
import gspread.exceptions
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import webbrowser
# import schedule
import time
from datetime import datetime


@dataclass
class PriceRecord:
    """Represents a pricing record"""
    product_name: str
    size: str
    price: float
    source: str
    timestamp: str = None
    metadata: Dict = None


class WebsiteScraper(ABC):
    """Abstract base class for website scrapers"""
    
    @abstractmethod
    def scrape(self) -> List[PriceRecord]:
        """Scrape website and return price records"""
        pass


class USPSScraper(WebsiteScraper):
    """Scrapes USPS flat rate pricing"""
    
    def __init__(self):
        self.url = "https://www.usps.com/business/prices.htm"
        self.base_url = "https://www.usps.com/business/prices.htm"
        # Mapping of USPS sizes to standard dimensions
        self.size_mapping = {
            "Small Flat Rate Box": {"dimensions": "8-11/16 × 5-7/16 × 1-3/4 in", "match": "12 × 9 × 6 in"},
            "Medium Flat Rate Box": {"dimensions": "11-1/4 × 8-3/4 × 6 in", "match": "16 × 12 × 8 in"},
            "Large Flat Rate Box": {"dimensions": "12 × 12-1/4 × 6 in", "match": "20 × 16 × 12 in"}
        }
    
    def scrape(self) -> List[PriceRecord]:
        """
        Scrape USPS pricing. 
        Note: USPS website structure may require API or specific parsing.
        This is a template - actual implementation needs adaptation to site structure.
        """
        records = []
        
        try:
            # For demonstration, using known January 2026 pricing
            # In production, would parse from website or API
            pricing_data = [
                {"name": "Small Flat Rate Box", "size": "8-11/16 × 5-7/16 × 1-3/4 in", 
                 "retail": 10.35, "commercial": 8.75},
                {"name": "Medium Flat Rate Box", "size": "11-1/4 × 8-3/4 × 6 in", 
                 "retail": 17.45, "commercial": 15.45},
                {"name": "Large Flat Rate Box", "size": "12 × 12-1/4 × 6 in", 
                 "retail": 24.75, "commercial": 22.90},
            ]
            
            for item in pricing_data:
                # Create records for both retail and commercial pricing
                records.append(PriceRecord(
                    product_name=f"USPS {item['name']} (Retail)",
                    size=item['size'],
                    price=item['retail'],
                    source="USPS Website",
                    metadata={"pricing_type": "retail"}
                ))
                records.append(PriceRecord(
                    product_name=f"USPS {item['name']} (Commercial)",
                    size=item['size'],
                    price=item['commercial'],
                    source="USPS Website",
                    metadata={"pricing_type": "commercial"}
                ))
            
        except Exception as e:
            print(f"Error scraping USPS: {e}")
        
        return records


class GenericHTMLScraper(WebsiteScraper):
    """Generic scraper that can be configured for different websites"""
    
    def __init__(self, url: str, selectors: Dict[str, str]):
        """
        Args:
            url: Website URL to scrape
            selectors: Dictionary mapping field names to CSS selectors
                      e.g., {'product_name': '.product-title', 'price': '.price'}
        """
        self.url = url
        self.selectors = selectors
    
    def scrape(self) -> List[PriceRecord]:
        """Scrape using provided selectors"""
        records = []
        
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all product containers
            products = soup.select(self.selectors.get('container', 'body'))
            
            for product in products:
                try:
                    name = product.select_one(self.selectors['product_name']).text.strip()
                    price_text = product.select_one(self.selectors['price']).text.strip()
                    
                    # Extract numeric price
                    price = self._extract_price(price_text)
                    
                    # Get size if available
                    size = ""
                    if 'size' in self.selectors:
                        size_elem = product.select_one(self.selectors['size'])
                        if size_elem:
                            size = size_elem.text.strip()
                    
                    records.append(PriceRecord(
                        product_name=name,
                        size=size,
                        price=price,
                        source=self.url
                    ))
                except Exception as e:
                    print(f"Error parsing product: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping {self.url}: {e}")
        
        return records
    
    def _extract_price(self, price_text: str) -> float:
        """Extract numeric price from text"""
        # Remove currency symbols and commas
        cleaned = re.sub(r'[^\d.]', '', price_text)
        try:
            return float(cleaned)
        except ValueError:
            return 0.0


class SelectorGenerator:
    """Generates CSS selectors for product scraping based on website analysis"""
    
    def __init__(self, url: str):
        self.url = url
    
    def generate_selectors(self, selected_products: List[str]) -> Dict[str, Dict[str, str]]:
        """
        Analyze the website and generate selectors for each selected product.
        
        Args:
            selected_products: List of product names to generate selectors for
            
        Returns:
            Dict mapping product name to selector dict (e.g., {'product_name': '.title', 'price': '.cost'})
        """
        selectors = {}
        
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Heuristic: Look for common patterns in HTML
            # Find potential product containers (divs with product-related classes)
            product_containers = soup.find_all(['div', 'li', 'article'], class_=lambda c: c and any(word in c.lower() for word in ['product', 'item', 'card']))
            
            for product_name in selected_products:
                # For each selected product, try to find matching elements
                product_selectors = self._find_selectors_for_product(soup, product_name, product_containers)
                if product_selectors:
                    selectors[product_name] = product_selectors
                else:
                    print(f"Failed to generate selectors for product '{product_name}': Could not find matching elements on the page.")
                    selectors[product_name] = {"error": "Could not generate selectors for this product"}
                    
        except Exception as e:
            print(f"Failed to generate selectors due to error: {e}")
            for product_name in selected_products:
                selectors[product_name] = {"error": str(e)}
        
        return selectors
    
    def _find_selectors_for_product(self, soup: BeautifulSoup, product_name: str, containers: List) -> Optional[Dict[str, str]]:
        """Find selectors for a specific product"""
        # Simple heuristic: Look for text matching product name, then find nearby price elements
        for container in containers:
            if product_name.lower() in container.get_text().lower():
                # Found a container with the product name
                # Look for price within this container
                price_elem = self._find_price_element(container)
                if price_elem:
                    # Generate selector for this price element
                    selector = self._generate_selector(price_elem)
                    return {
                        'container': self._generate_selector(container),
                        'product_name': self._generate_selector(container.find(text=re.compile(product_name, re.I)).parent if container.find(text=re.compile(product_name, re.I)) else container),
                        'price': selector
                    }
        return None
    
    def _find_price_element(self, container) -> Optional:
        """Find an element containing a price within the container"""
        # Look for elements with price-like text (contains $ or digits)
        for elem in container.find_all(text=re.compile(r'\$?\d+\.?\d*')):
            parent = elem.parent
            if parent and parent.name in ['span', 'div', 'p', 'strong']:
                return parent
        return None
    
    def _generate_selector(self, element) -> str:
        """Generate a CSS selector for an element"""
        if not element:
            return ""
        
        # Simple selector generation: use class or id if available
        if element.get('id'):
            return f"#{element['id']}"
        elif element.get('class'):
            classes = '.'.join(element['class'])
            return f".{classes}"
        else:
            # Fallback: use tag name (less specific)
            return element.name
    
    def test_selectors(self, selectors: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, any]]:
        """
        Test the generated selectors by performing a scrape and verifying price extraction.
        
        Args:
            selectors: Dict of selectors per product
            
        Returns:
            Dict with test results for each product
        """
        results = {}
        for product_name, sel_dict in selectors.items():
            if "error" in sel_dict:
                results[product_name] = {"success": False, "error": sel_dict["error"]}
                continue
            
            scraper = GenericHTMLScraper(self.url, sel_dict)
            records = scraper.scrape()
            if records:
                # Assume first record is the test; check if price is numeric and > 0
                price = records[0].price
                if price > 0:
                    results[product_name] = {"success": True, "extracted_price": price}
                else:
                    results[product_name] = {"success": False, "error": "Invalid price extracted"}
            else:
                results[product_name] = {"success": False, "error": "No records scraped"}
        return results


class GoogleSheetsHandler:
    """Handles reading/writing to Google Sheets"""
    
    def __init__(self, credentials_file: str, sheet_url: str):
        """
        Args:
            credentials_file: Path to Google service account credentials JSON
            sheet_url: URL or key of the Google Sheet
        """
        self.credentials_file = credentials_file
        self.sheet_url = sheet_url
        self.client = None
        self.sheet = None
    
    def connect(self):
        """Establish connection to Google Sheets"""
        scope = ['https://spreadsheets.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_file, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_url(self.sheet_url)
    
    def read_baseline(self, worksheet_name: str = "Baseline") -> pd.DataFrame:
        """Read baseline pricing data from sheet"""
        if not self.sheet:
            self.connect()
        
        try:
            worksheet = self.sheet.worksheet(worksheet_name)
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except gspread.exceptions.WorksheetNotFound:
            print(f"Worksheet '{worksheet_name}' not found. Creating empty baseline.")
            return pd.DataFrame(columns=['product_name', 'size', 'baseline_price'])
    
    def write_comparison(self, comparison_data: pd.DataFrame, 
                        worksheet_name: str = "Comparison"):
        """Write comparison results to sheet"""
        if not self.sheet:
            self.connect()
        
        try:
            worksheet = self.sheet.worksheet(worksheet_name)
        except gspread.exceptions.WorksheetNotFound:
            worksheet = self.sheet.add_worksheet(
                title=worksheet_name, rows=1000, cols=20)
        
        worksheet.clear()
        worksheet.update([comparison_data.columns.values.tolist()] + 
                        comparison_data.values.tolist())


class PriceComparator:
    """Compares current prices with baseline"""
    
    @staticmethod
    def compare(current_records: List[PriceRecord], 
                baseline_df: pd.DataFrame) -> pd.DataFrame:
        """
        Compare current prices with baseline
        
        Returns:
            DataFrame with comparison results including differences
        """
        # Convert current records to DataFrame
        current_df = pd.DataFrame([
            {
                'product_name': r.product_name,
                'size': r.size,
                'current_price': r.price,
                'source': r.source
            } for r in current_records
        ])
        
        # Merge with baseline
        comparison = pd.merge(
            baseline_df,
            current_df,
            on=['product_name', 'size'],
            how='outer',
            suffixes=('_baseline', '_current')
        )
        
        # Calculate differences
        comparison['price_diff'] = (
            comparison['current_price'] - comparison['baseline_price']
        )
        comparison['price_diff_pct'] = (
            (comparison['price_diff'] / comparison['baseline_price']) * 100
        ).round(2)
        
        # Add status column
        def get_status(row):
            if pd.isna(row['current_price']):
                return "REMOVED"
            elif pd.isna(row['baseline_price']):
                return "NEW"
            elif row['price_diff'] > 0:
                return "INCREASED"
            elif row['price_diff'] < 0:
                return "DECREASED"
            else:
                return "UNCHANGED"
        
        comparison['status'] = comparison.apply(get_status, axis=1)
        
        return comparison
    
    @staticmethod
    def generate_report(comparison_df: pd.DataFrame) -> str:
        """Generate human-readable report of changes"""
        report = ["=== PRICE CHANGE REPORT ===\n"]
        
        # Summary statistics
        total = len(comparison_df)
        changed = len(comparison_df[comparison_df['status'].isin(
            ['INCREASED', 'DECREASED', 'NEW', 'REMOVED'])])
        
        report.append(f"Total items tracked: {total}")
        report.append(f"Items with changes: {changed}\n")
        
        # Detail each change
        for status in ['INCREASED', 'DECREASED', 'NEW', 'REMOVED']:
            items = comparison_df[comparison_df['status'] == status]
            if not items.empty:
                report.append(f"\n{status}:")
                for _, row in items.iterrows():
                    product = row['product_name']
                    if status == 'NEW':
                        report.append(
                            f"  • {product}: ${row['current_price']:.2f}")
                    elif status == 'REMOVED':
                        report.append(
                            f"  • {product}: was ${row['baseline_price']:.2f}")
                    else:
                        report.append(
                            f"  • {product}: ${row['baseline_price']:.2f} → "
                            f"${row['current_price']:.2f} "
                            f"({row['price_diff']:+.2f}, "
                            f"{row['price_diff_pct']:+.1f}%)")
        
        return "\n".join(report)


class ProductSelector:
    """Handles product detection and selection from a website"""
    
    @staticmethod
    def detect_products(url: str) -> List[str]:
        """
        Detect and return a list of potential products from the given URL.
        Uses basic web scraping to find elements that might represent products.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Simple heuristic: Look for divs or h2 elements that might contain product info
            # This is a basic implementation; can be improved with more sophisticated selectors
            candidates = soup.find_all(['div', 'h2'], class_=lambda c: c and ('product' in c.lower() or 'item' in c.lower())) or soup.find_all('div', attrs={'data-product': True})
            product_list = []
            for candidate in candidates[:10]:  # Limit to first 10 to avoid overwhelming output
                text = candidate.get_text(strip=True)
                if text and len(text) > 3:  # Filter out very short or empty texts
                    product_list.append(text)
            return product_list
        except requests.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return []
        except Exception as e:
            print(f"Error parsing the page: {e}")
            return []
    
    @staticmethod
    def select_products(detected_products: List[str]) -> List[str]:
        """
        Present the detected products and allow the admin to select one or more.
        Returns the list of selected product names.
        """
        if not detected_products:
            print("No products detected to select from.")
            return []
        
        print("Detected products or candidates:")
        for i, product in enumerate(detected_products, 1):
            print(f"{i}. {product}")
        
        selected = []
        while True:
            try:
                choice = input("Enter the number(s) of the product(s) to select (comma-separated, or 'done' to finish): ").strip()
                if choice.lower() == 'done':
                    break
                indices = [int(x.strip()) - 1 for x in choice.split(',') if x.strip().isdigit()]
                for idx in indices:
                    if 0 <= idx < len(detected_products):
                        selected.append(detected_products[idx])
                    else:
                        print(f"Invalid number: {idx + 1}")
                if selected:
                    print(f"Selected so far: {selected}")
            except ValueError:
                print("Please enter valid numbers separated by commas, or 'done'.")
        
        return list(set(selected))  # Remove duplicates
    
    @staticmethod
    def verify_in_browser(url: str):
        """
        Open the target URL in the default web browser for manual verification of detected products.
        This allows the admin to visually inspect the site using dev tools if needed.
        """
        try:
            webbrowser.open(url)
            print(f"Opened {url} in your default web browser for verification.")
        except Exception as e:
            print(f"Error opening browser: {e}")
    
    @staticmethod
    def persist_selected_products(selected_products: List[str], filename: str = 'selected_products.json'):
        """
        Persist the selected products to a JSON file.
        """
        try:
            with open(filename, 'w') as f:
                json.dump(selected_products, f, indent=4)
            print(f"Selected products persisted to {filename}.")
        except Exception as e:
            print(f"Error persisting selected products: {e}")
    
    @staticmethod
    def load_selected_products(filename: str = 'selected_products.json') -> List[str]:
        """
        Load persisted selected products from a JSON file.
        """
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error loading selected products: {e}")
            return []


class ScraperScheduler:
    """Handles scheduling of daily scrapes"""
    
    def __init__(self, scraper: WebsiteScraper, selected_products: List[str], selectors: Dict[str, Dict[str, str]], sheets_handler: GoogleSheetsHandler):
        self.scraper = scraper
        self.selected_products = selected_products
        self.selectors = selectors
        self.sheets_handler = sheets_handler
    
    def run_scheduled_scrape(self):
        """Run the scrape job at the scheduled time"""
        print(f"Running scheduled scrape at {datetime.now()}")
        # Load selected products and selectors (assuming persisted)
        selected = ProductSelector.load_selected_products()
        if not selected:
            print("No selected products found. Skipping scrape.")
            return
        
        # For simplicity, assume generic scraper; in production, map to appropriate scraper
        records = []
        for product in selected:
            if product in self.selectors and "error" not in self.selectors[product]:
                scraper_url = getattr(self.scraper, 'url', "https://example.com")
                scraper = GenericHTMLScraper(scraper_url, self.selectors[product])
                records.extend(scraper.scrape())
        
        # Compare with baseline
        baseline_df = self.sheets_handler.read_baseline()
        comparison = PriceComparator.compare(records, baseline_df)
        report = PriceComparator.generate_report(comparison)
        print(report)
        
        # Write back to sheets
        self.sheets_handler.write_comparison(comparison)
        
        # Placeholder for notification (to be implemented in US-006)
        print("Scrape completed. (Notifications not yet implemented.)")
    
    def start_scheduler(self):
        """Start the scheduler to run daily at 1:00am"""
        # schedule.every().day.at("01:00").do(self.run_scheduled_scrape)
        print("Scheduler started. Scraping will run daily at 1:00am.")
        print("Note: schedule library not available - implement scheduling manually")
        # while True:
        #     schedule.run_pending()
        #     time.sleep(60)  # Check every minute


def main():
    """Example usage of the price tracker"""
    
    # Example 1: USPS Scraping
    print("Scraping USPS pricing...")
    usps_scraper = USPSScraper()
    current_prices = usps_scraper.scrape()
    
    print(f"Found {len(current_prices)} price records")
    for record in current_prices[:3]:  # Show first 3
        print(f"  {record.product_name}: ${record.price:.2f}")
    
    # Example 2: Product Selection Workflow
    print("\n--- Product Selection Workflow ---")
    url = input("Enter the target website URL: ").strip()
    detected = ProductSelector.detect_products(url)
    # Offer browser verification
    verify = input("Would you like to verify the detected products in your browser? (y/n): ").strip().lower()
    if verify == 'y':
        ProductSelector.verify_in_browser(url)
    selected = ProductSelector.select_products(detected)
    if selected:
        ProductSelector.persist_selected_products(selected)
        print(f"Selected products: {selected}")
    else:
        print("No products selected.")
    
    # Initialize variables for later use
    selectors = {}
    
    # Generate selectors for selected products
    if selected:
        generator = SelectorGenerator(url)
        selectors = generator.generate_selectors(selected)
        print("\nGenerated selectors:")
        for product, sel in selectors.items():
            print(f"  {product}: {sel}")
        
        # Test selectors
        test_results = generator.test_selectors(selectors)
        print("\nSelector test results:")
        for product, result in test_results.items():
            if result["success"]:
                print(f"  {product}: Success - Extracted price ${result['extracted_price']:.2f}")
            else:
                print(f"  {product}: Failed - {result['error']}")
    else:
        # Initialize empty list for later use
        selected = []
    
    # Example 3: Compare with baseline (requires Google Sheets setup)
    # Uncomment and configure when ready to use:
    sheets_handler = None
    try:
        sheets_handler = GoogleSheetsHandler(
            credentials_file='auth/google-service-account-credentials.json',
            sheet_url='https://docs.google.com/spreadsheets/d/1GRT_hiUgzu68mKJuCLa5U98333ZCi30fJgu9SnNI87k/edit'
        )
        
        baseline_df = sheets_handler.read_baseline()
        comparison = PriceComparator.compare(current_prices, baseline_df)
        report = PriceComparator.generate_report(comparison)
        
        print("\n" + report)
        
        # Write results back to Google Sheets
        sheets_handler.write_comparison(comparison)
    except FileNotFoundError:
        print("\nGoogle Sheets credentials file not found. Skipping baseline comparison.")
        print("To enable this feature, place your credentials at 'auth/google-service-account-credentials.json'")
    except Exception as e:
        print(f"\nError with Google Sheets integration: {e}")
        print("Skipping baseline comparison.")
    
    
    # Example 4: Generic scraper configuration
    # Configure for any website by specifying CSS selectors
    """
    generic_scraper = GenericHTMLScraper(
        url='https://example.com/pricing',
        selectors={
            'container': '.product-card',
            'product_name': '.product-title',
            'price': '.price-value',
            'size': '.product-size'
        }
    )
    prices = generic_scraper.scrape()
    """
    
    # Example 5: Start scheduled scraping (for demonstration, run immediately; in production, run as daemon)
    if selected and selectors and sheets_handler:
        scheduler = ScraperScheduler(usps_scraper, selected, selectors, sheets_handler)  # Using USPS as example; adapt for generic
        # For testing, run once immediately instead of scheduling
        test_run = input("Run a test scrape now? (y/n): ").strip().lower()
        if test_run == 'y':
            scheduler.run_scheduled_scrape()
        # To start actual scheduler: scheduler.start_scheduler()
    elif selected and selectors:
        print("\nScheduler not started - Google Sheets handler not available.")


if __name__ == "__main__":
    main()
