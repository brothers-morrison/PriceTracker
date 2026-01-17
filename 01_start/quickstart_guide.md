# 🚀 Quick Start Guide - Generic Price Tracker

## Overview

This tool helps you track price changes across any website by comparing current prices with baseline data stored in Google Sheets. It's designed to be:

- **Generic**: Works with any website with proper configuration
- **Modular**: Easy to extend with new scrapers
- **Automated**: Can run on a schedule to monitor prices
- **Flexible**: Compare prices across multiple sources

## 📋 Prerequisites

### 1. Python Environment
```bash
# Python 3.8 or higher
python3 --version

# Install required packages
pip install requests beautifulsoup4 gspread oauth2client pandas lxml
```

### 2. Google Sheets Setup

**Create your baseline sheet:**
1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet called "Shipping Cost Tracker"
3. Add columns: `product_name`, `size`, `baseline_price`, `carrier`, `service_type`, `notes`
4. Populate with baseline data (see template)

**Enable API access:**
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a project → Enable "Google Sheets API"
3. Create Service Account → Download JSON credentials
4. Share your sheet with the service account email (found in JSON)

## 🎯 USPS Test Case Setup

### Baseline Data for Google Sheet

Copy this data into your Google Sheet:

| product_name | size | baseline_price | carrier | service_type |
|-------------|------|----------------|---------|--------------|
| USPS Small Flat Rate Box (Retail) | 8-11/16 × 5-7/16 × 1-3/4 in | 10.35 | USPS | Priority Mail |
| USPS Small Flat Rate Box (Commercial) | 8-11/16 × 5-7/16 × 1-3/4 in | 8.75 | USPS | Priority Mail |
| USPS Medium Flat Rate Box (Retail) | 11-1/4 × 8-3/4 × 6 in | 17.45 | USPS | Priority Mail |
| USPS Medium Flat Rate Box (Commercial) | 11-1/4 × 8-3/4 × 6 in | 15.45 | USPS | Priority Mail |
| USPS Large Flat Rate Box (Retail) | 12 × 12-1/4 × 6 in | 24.75 | USPS | Priority Mail |
| USPS Large Flat Rate Box (Commercial) | 12 × 12-1/4 × 6 in | 22.90 | USPS | Priority Mail |

### Size Mapping Notes

Your test sizes vs. actual USPS boxes:
- **Test Small** (12×9×6 in) ≈ **USPS Small** (8.69×5.44×1.75 in)
- **Test Medium** (16×12×8 in) ≈ **USPS Medium** (11.25×8.75×6 in)
- **Test Large** (20×16×12 in) ≈ **USPS Large** (12×12.25×6 in)

> Note: USPS flat rate pricing is based on using official USPS boxes, not dimensions. The mapping is conceptual for comparison purposes.

## ⚡ Quick Start (5 Minutes)

### Step 1: Save the Main Script

Save the "Generic Price Tracker Tool" code as `price_tracker.py`

### Step 2: Create Configuration File

Create `config.py`:
```python
# Google Sheets Configuration
CREDENTIALS_FILE = 'credentials.json'  # Path to your service account JSON
SHEET_URL = 'https://docs.google.com/spreadsheets/d/YOUR-SHEET-ID/edit'

# Scraping Configuration
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
REQUEST_TIMEOUT = 10
```

### Step 3: Run Your First Scrape

Create `run_tracker.py`:
```python
from price_tracker import USPSScraper, GoogleSheetsHandler, PriceComparator
from config import CREDENTIALS_FILE, SHEET_URL

# Scrape current prices
scraper = USPSScraper()
current_prices = scraper.scrape()

# Load baseline from Google Sheets
sheets = GoogleSheetsHandler(CREDENTIALS_FILE, SHEET_URL)
baseline = sheets.read_baseline()

# Compare
comparison = PriceComparator.compare(current_prices, baseline)
report = PriceComparator.generate_report(comparison)

# Print report
print(report)

# Save to Google Sheets
sheets.write_comparison(comparison, 'Latest_Comparison')
```

Run it:
```bash
python3 run_tracker.py
```

## 🎨 Customizing for Other Websites

### Example: Custom E-commerce Site

```python
from price_tracker import GenericHTMLScraper

# Configure scraper with CSS selectors
scraper = GenericHTMLScraper(
    url='https://example-carrier.com/rates',
    selectors={
        'container': 'div.pricing-card',      # Each product container
        'product_name': 'h3.service-title',   # Product name element
        'price': 'span.rate-amount',          # Price element
        'size': 'div.box-dimensions'          # Size/dimensions
    }
)

# Scrape
prices = scraper.scrape()
```

### Finding CSS Selectors

1. Open the website in Chrome/Firefox
2. Right-click on the element → "Inspect"
3. Right-click the HTML element → Copy → Copy selector
4. Use that selector in your configuration

## 📊 Understanding the Output

### Comparison Report

```
=== PRICE CHANGE REPORT ===

Total items tracked: 6
Items with changes: 2

INCREASED:
  • USPS Small Flat Rate Box (Retail): $10.25 → $10.35 (+0.10, +0.98%)
  • USPS Large Flat Rate Box (Retail): $24.50 → $24.75 (+0.25, +1.02%)

UNCHANGED:
  • USPS Medium Flat Rate Box (Retail): $17.45 (no change)
  ...
```

### Status Values
- **INCREASED**: Price went up
- **DECREASED**: Price went down
- **UNCHANGED**: No change detected
- **NEW**: Product appeared for first time
- **REMOVED**: Product no longer found

## 🔄 Automation

### Linux/Mac (cron)

Edit crontab:
```bash
crontab -e
```

Add daily check at 6 AM:
```
0 6 * * * /usr/bin/python3 /path/to/run_tracker.py >> /var/log/price_tracker.log 2>&1
```

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 6:00 AM
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `C:\path\to\run_tracker.py`

## 🚨 Adding Notifications

### Email Alerts

```python
import smtplib
from email.mime.text import MIMEText

def send_email_alert(report):
    msg = MIMEText(report)
    msg['Subject'] = 'Price Change Alert'
    msg['From'] = 'alerts@yourcompany.com'
    msg['To'] = 'you@yourcompany.com'
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email', 'your_password')
    server.send_message(msg)
    server.quit()

# Use it
if len(changes) > 0:
    send_email_alert(report)
```

### Slack Alerts

```python
import requests

def send_slack_alert(report):
    webhook_url = 'YOUR_SLACK_WEBHOOK_URL'
    requests.post(webhook_url, json={
        'text': f'🚨 Price Change Alert\n\n{report}'
    })
```

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install --upgrade requests beautifulsoup4 gspread oauth2client pandas
```

### "Authentication failed" with Google Sheets
- Verify credentials file path is correct
- Check that sheet is shared with service account email
- Ensure Google Sheets API is enabled in Cloud Console

### No data scraped from website
- Check if website structure changed
- Verify CSS selectors are correct
- Some sites block scrapers (check robots.txt)
- May need to add headers/cookies for authentication

### Rate limiting / IP blocking
```python
import time
import random

# Add delays between requests
time.sleep(random.uniform(1, 3))

# Use rotating user agents
headers = {
    'User-Agent': 'Mozilla/5.0 ...',
    'Accept': 'text/html,application/xhtml+xml...'
}
```

## 📚 Next Steps

1. **Extend to FedEx**: Create `FedExScraper` class
2. **Extend to UPS**: Create `UPSScraper` class
3. **Add API support**: Some carriers offer official APIs
4. **Create dashboard**: Build a web UI to visualize trends
5. **Track history**: Store historical data for trend analysis
6. **Add alerting**: Set thresholds for significant changes
7. **Multi-region**: Track prices across different countries

## 🔗 Useful Resources

- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [CSS Selector Reference](https://www.w3schools.com/cssref/css_selectors.asp)
- [USPS Pricing Page](https://www.usps.com/business/prices.htm)
- [FedEx Rates](https://www.fedex.com/en-us/shipping/rates.html)
- [UPS Rates](https://www.ups.com/us/en/support/shipping-support/shipping-costs-rates.page)

## 💡 Pro Tips

1. **Version control baseline**: Keep baseline data in Git alongside code
2. **Test before production**: Run manually a few times before automating
3. **Log everything**: Save logs to debug issues later
4. **Handle failures gracefully**: Don't let one failed scrape crash everything
5. **Respect robots.txt**: Be a good internet citizen
6. **Cache results**: Avoid re-scraping if data hasn't changed
7. **Monitor performance**: Track how long scrapes take

---

**Need help?** Check the usage examples or create an issue on GitHub!
