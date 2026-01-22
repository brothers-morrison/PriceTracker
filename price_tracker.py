import os
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import json

@dataclass
class PriceRecord:
    product_name: str
    price: float
    url: str
    timestamp: str

class WebsiteScraper(ABC):
    """Abstract base class for website scrapers"""
    
    @abstractmethod
    def scrape(self) -> List[PriceRecord]:
        pass

class USPSScraper(WebsiteScraper):
    """Scrapes USPS flat rate pricing"""
    
    def __init__(self, url: str = "https://www.usps.com/ship/flat-rate-shipping-options.htm"):
        self.url = url
    
    def scrape(self) -> List[PriceRecord]:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        records = []
        # Example parsing logic (simplified)
        for item in soup.find_all('div', class_='flat-rate-item'):
            product_name = item.find('h3').text.strip()
            price_text = item.find('span', class_='price').text.strip()
            price = self._extract_price(price_text)
            records.append(PriceRecord(product_name, price, self.url, time.strftime('%Y-%m-%d %H:%M:%S')))
        return records
    
    def _extract_price(self, price_text: str) -> float:
        # Simplified extraction
        return float(price_text.replace('$', ''))

class GenericHTMLScraper(WebsiteScraper):
    """Generic scraper that can be configured for different websites"""
    
    def __init__(self, url: str, selectors: Dict[str, str]):
        self.url = url
        self.selectors = selectors
    
    def scrape(self) -> List[PriceRecord]:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        records = []
        for product, sel in self.selectors.items():
            element = soup.select_one(sel)
            if element:
                price_text = element.text.strip()
                price = self._extract_price(price_text)
                records.append(PriceRecord(product, price, self.url, time.strftime('%Y-%m-%d %H:%M:%S')))
        return records
    
    def _extract_price(self, price_text: str) -> float:
        # Simplified extraction
        return float(price_text.replace('$', ''))

class SelectorGenerator:
    """Generates CSS selectors for product scraping based on website analysis"""
    
    def __init__(self, url: str):
        self.url = url
    
    def generate_selectors(self, selected_products: List[str]) -> Dict[str, Dict[str, str]]:
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')
        selectors = {}
        containers = soup.find_all('div', class_='product-container')  # Example
        for product in selected_products:
            selectors[product] = self._find_selectors_for_product(soup, product, containers)
        return selectors
    
    def _find_selectors_for_product(self, soup: BeautifulSoup, product_name: str, containers: List) -> Dict[str, str]:
        for container in containers:
            if product_name in container.text:
                price_elem = self._find_price_element(container)
                if price_elem:
                    return {'price': self._generate_selector(price_elem)}
        return {}
    
    def _find_price_element(self, container) -> Optional[Any]:
        return container.find('span', class_='price')
    
    def _generate_selector(self, element) -> str:
        # Simplified selector generation
        return f"span.price"
    
    def test_selectors(self, selectors: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        # Test logic here
        return selectors

class DatabaseHandler:
    """Handles storing and retrieving scrape results in a database (SQLite by default)"""
    
    def __init__(self, db_path: str = 'price_tracker.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''CREATE TABLE IF NOT EXISTS prices (
                            id INTEGER PRIMARY KEY,
                            product_name TEXT,
                            price REAL,
                            url TEXT,
                            timestamp TEXT
                        )''')
        conn.close()
    
    def store_results(self, records: List[PriceRecord]):
        conn = sqlite3.connect(self.db_path)
        for record in records:
            conn.execute('INSERT INTO prices (product_name, price, url, timestamp) VALUES (?, ?, ?, ?)',
                         (record.product_name, record.price, record.url, record.timestamp))
        conn.commit()
        conn.close()
    
    def get_latest_results(self) -> pd.DataFrame:
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT * FROM prices ORDER BY timestamp DESC LIMIT 100", conn)
        conn.close()
        return df

class GoogleSheetsHandler:
    """Handles reading/writing to Google Sheets"""
    
    def __init__(self, credentials_file: str, sheet_url: str):
        self.credentials_file = credentials_file
        self.sheet_url = sheet_url
        self.gc = None
    
    def connect(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        self.gc = gspread.authorize(creds)
    
    def read_baseline(self, worksheet_name: str = "Baseline") -> pd.DataFrame:
        sheet = self.gc.open_by_url(self.sheet_url).worksheet(worksheet_name)
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    
    def write_comparison(self, comparison_data: pd.DataFrame, worksheet_name: str = "Comparison"):
        sheet = self.gc.open_by_url(self.sheet_url).worksheet(worksheet_name)
        sheet.update([comparison_data.columns.values.tolist()] + comparison_data.values.tolist())

class PriceComparator:
    """Compares current prices with baseline"""
    
    @staticmethod
    def compare(current_records: List[PriceRecord], baseline_df: pd.DataFrame) -> pd.DataFrame:
        """
        Compare current prices with baseline
        
        Returns:
            DataFrame with comparison results including differences
        """
        current_df = pd.DataFrame([{'product_name': r.product_name, 'current_price': r.price} for r in current_records])
        merged = pd.merge(current_df, baseline_df, on='product_name', how='left')
        merged['difference'] = merged['current_price'] - merged['baseline_price']
        merged['status'] = merged.apply(lambda row: PriceComparator.get_status(row), axis=1)
        return merged
    
    @staticmethod
    def get_status(row):
        if row['difference'] > 0:
            return 'increased'
        elif row['difference'] < 0:
            return 'decreased'
        else:
            return 'unchanged'
    
    @staticmethod
    def generate_report(comparison_df: pd.DataFrame) -> str:
        report = "Price Change Report:\n"
        for _, row in comparison_df.iterrows():
            report += f"{row['product_name']}: {row['status']} by {row['difference']}\n"
        return report

class NotificationHandler:
    """Handles sending notifications when price changes are detected"""
    
    def __init__(self, notification_method: str = 'console', email_config: Optional[Dict] = None):
        self.notification_method = notification_method
        self.email_config = email_config
    
    def notify_if_changes(self, comparison_df: pd.DataFrame):
        changes = comparison_df[comparison_df['status'] != 'unchanged']
        if not changes.empty:
            report = PriceComparator.generate_report(changes)
            if self.notification_method == 'console':
                print(report)
            elif self.notification_method == 'email':
                self._send_email_notification(report)
    
    def _send_email_notification(self, report: str):
        msg = MIMEMultipart()
        msg['From'] = self.email_config['from']
        msg['To'] = self.email_config['to']
        msg['Subject'] = "Price Change Alert"
        msg.attach(MIMEText(report, 'plain'))
        server = smtplib.SMTP(self.email_config['smtp_server'], self.email_config['port'])
        server.starttls()
        server.login(self.email_config['username'], self.email_config['password'])
        text = msg.as_string()
        server.sendmail(self.email_config['from'], self.email_config['to'], text)
        server.quit()

class ProductSelector:
    """Handles product detection and selection from a website"""
    
    @staticmethod
    def detect_products(url: str) -> List[str]:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        products = [elem.text.strip() for elem in soup.find_all('h3', class_='product-name')]
        return products
    
    @staticmethod
    def select_products(detected_products: List[str]) -> List[str]:
        # Simplified selection, perhaps interactive
        return detected_products[:5]  # Select first 5
    
    @staticmethod
    def verify_in_browser(url: str):
        import webbrowser
        webbrowser.open(url)
    
    @staticmethod
    def persist_selected_products(selected_products: List[str], filename: str = 'selected_products.json'):
        with open(filename, 'w') as f:
            json.dump(selected_products, f)
    
    @staticmethod
    def load_selected_products(filename: str = 'selected_products.json') -> List[str]:
        with open(filename, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def persist_selectors(selectors: Dict[str, Dict[str, str]], filename: str = 'selectors.json'):
        with open(filename, 'w') as f:
            json.dump(selectors, f)
    
    @staticmethod
    def load_selectors(filename: str = 'selectors.json') -> Dict[str, Dict[str, str]]:
        with open(filename, 'r') as f:
            return json.load(f)

class ScraperScheduler:
    """Handles scheduling of daily scrapes"""
    
    def __init__(self, scraper: WebsiteScraper, selected_products: List[str], selectors: Dict[str, Dict[str, str]], db_handler: DatabaseHandler, notification_handler: NotificationHandler):
        self.scraper = scraper
        self.selected_products = selected_products
        self.selectors = selectors
        self.db_handler = db_handler
        self.notification_handler = notification_handler
    
    def run_scheduled_scrape(self):
        records = self.scraper.scrape()
        self.db_handler.store_results(records)
        # Assume baseline is loaded elsewhere
        baseline_df = pd.DataFrame()  # Placeholder
        comparison_df = PriceComparator.compare(records, baseline_df)
        self.notification_handler.notify_if_changes(comparison_df)
    
    def start_scheduler(self):
        schedule.every().day.at("09:00").do(self.run_scheduled_scrape)
        while True:
            schedule.run_pending()
            time.sleep(1)

def program_complete():
    print("<PROGRAM_COMPLETE>")

def main():
    # Example usage
    scraper = USPSScraper()
    records = scraper.scrape()
    db = DatabaseHandler()
    db.store_results(records)
    # More logic here...
    program_complete()
