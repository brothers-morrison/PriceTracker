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
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


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
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            self.credentials_file, scope)
        self.client = gspread.authorize(creds)
        self.sheet = self.client.open_by_url(self.sheet_url)
    
    def read_baseline(self, worksheet_name: str = "Baseline") -> pd.DataFrame:
        """Read baseline pricing data from sheet"""
        if not self.sheet:
            self.connect()
        
        worksheet = self.sheet.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    
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


def main():
    """Example usage of the price tracker"""
    
    # Example 1: USPS Scraping
    print("Scraping USPS pricing...")
    usps_scraper = USPSScraper()
    current_prices = usps_scraper.scrape()
    
    print(f"Found {len(current_prices)} price records")
    for record in current_prices[:3]:  # Show first 3
        print(f"  {record.product_name}: ${record.price:.2f}")
    
    # Example 2: Compare with baseline (requires Google Sheets setup)
    # Uncomment and configure when ready to use:

    sheets_handler = GoogleSheetsHandler(
        credentials_file='auth/google-service-account-credentials.json',
        sheet_url='https://docs.google.com/spreadsheets/d/1GRT_hiUgzu68mKJuCLa5U98333ZCi30fJgu9SnNI87k/edit'
    )
    """
    sheets_handler = GoogleSheetsHandler(
        credentials_file='path/to/credentials.json',
        sheet_url='your-google-sheet-url'
    )
    """

    baseline_df = sheets_handler.read_baseline()
    comparison = PriceComparator.compare(current_prices, baseline_df)
    report = PriceComparator.generate_report(comparison)
    
    print("\n" + report)
    
    # Write results back to Google Sheets
    sheets_handler.write_comparison(comparison)
    
    
    # Example 3: Generic scraper configuration
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


if __name__ == "__main__":
    main()
