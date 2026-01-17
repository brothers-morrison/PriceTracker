# Shipping Cost Baseline - Google Sheets Template

## Sheet 1: Baseline

This is your baseline pricing data. Create a Google Sheet with these columns and data:

| product_name | size | baseline_price | carrier | service_type | notes |
|-------------|------|----------------|---------|--------------|-------|
| USPS Small Flat Rate Box (Retail) | 8-11/16 × 5-7/16 × 1-3/4 in | 10.35 | USPS | Priority Mail Flat Rate | Approximate to 12 × 9 × 6 in |
| USPS Small Flat Rate Box (Commercial) | 8-11/16 × 5-7/16 × 1-3/4 in | 8.75 | USPS | Priority Mail Flat Rate | Approximate to 12 × 9 × 6 in |
| USPS Medium Flat Rate Box (Retail) | 11-1/4 × 8-3/4 × 6 in | 17.45 | USPS | Priority Mail Flat Rate | Approximate to 16 × 12 × 8 in |
| USPS Medium Flat Rate Box (Commercial) | 11-1/4 × 8-3/4 × 6 in | 15.45 | USPS | Priority Mail Flat Rate | Approximate to 16 × 12 × 8 in |
| USPS Large Flat Rate Box (Retail) | 12 × 12-1/4 × 6 in | 24.75 | USPS | Priority Mail Flat Rate | Approximate to 20 × 16 × 12 in |
| USPS Large Flat Rate Box (Commercial) | 12 × 12-1/4 × 6 in | 22.90 | USPS | Priority Mail Flat Rate | Approximate to 20 × 16 × 12 in |
| FedEx Small Box | 12.25 × 10.875 × 1.5 in | TBD | FedEx | One Rate | To be researched |
| FedEx Medium Box | 13.25 × 11.5 × 2.375 in | TBD | FedEx | One Rate | To be researched |
| FedEx Large Box | 17.875 × 12.375 × 3 in | TBD | FedEx | One Rate | To be researched |
| UPS Small Box | ~12 × 9 × 6 in | TBD | UPS | Ground | To be researched |
| UPS Medium Box | ~16 × 12 × 8 in | TBD | UPS | Ground | To be researched |
| UPS Large Box | ~20 × 16 × 12 in | TBD | UPS | Ground | To be researched |

## Sheet 2: Comparison (Auto-generated)

This sheet will be automatically populated by the Python script when you run it. It will show:
- Current prices
- Baseline prices
- Price differences ($ and %)
- Status (INCREASED, DECREASED, UNCHANGED, NEW, REMOVED)

## Sheet 3: Change History (Optional)

Track changes over time:

| timestamp | product_name | old_price | new_price | change_amount | change_pct |
|-----------|-------------|-----------|-----------|---------------|------------|
| 2026-01-18 | USPS Small Flat Rate Box (Retail) | 10.25 | 10.35 | +0.10 | +0.98% |

---

## Setup Instructions

### 1. Create Google Sheet
1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet
3. Name it "Shipping Cost Tracker"
4. Copy the data from "Sheet 1: Baseline" above into your sheet
5. Note the URL of your sheet

### 2. Enable Google Sheets API
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable "Google Sheets API"
4. Create credentials → Service Account
5. Download the JSON credentials file
6. Share your Google Sheet with the service account email (found in JSON)

### 3. Install Python Dependencies
```bash
pip install requests beautifulsoup4 gspread oauth2client pandas lxml
```

### 4. Update Code Configuration
In the Python script, update:
```python
sheets_handler = GoogleSheetsHandler(
    credentials_file='path/to/your-credentials.json',
    sheet_url='https://docs.google.com/spreadsheets/d/YOUR-SHEET-ID/edit'
)
```

---

## Size Mapping Reference

### USPS Flat Rate Boxes (Actual Dimensions)
- **Small**: 8-11/16 × 5-7/16 × 1-3/4 inches (8.69 × 5.44 × 1.75 in)
- **Medium (Top-load)**: 11-1/4 × 8-3/4 × 6 inches
- **Medium (Side-load)**: 14-1/8 × 12 × 3-1/2 inches  
- **Large**: 12 × 12-1/4 × 6 inches

### Test Case Comparison Sizes
- **Small Test Size**: 12 × 9 × 6 inches (closest approx to USPS Small in volume)
- **Medium Test Size**: 16 × 12 × 8 inches (closest approx to USPS Medium)
- **Large Test Size**: 20 × 16 × 12 inches (closest approx to USPS Large)

### Important Notes
- USPS Flat Rate pricing is **not** based on dimensions but on using official USPS boxes
- For UPS and FedEx, pricing **is** based on actual dimensions and weight
- The test case sizes are approximations for comparison purposes
- Always verify current pricing on official carrier websites
- USPS rates changed January 18, 2026 - verify if these are current
