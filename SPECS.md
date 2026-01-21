# PRD: Automated Website Price Monitoring Tool (MVP)

## 1. Introduction / Overview

This feature provides an internal admin tool that enables automated price monitoring for selected products on a given website. Administrators can define a target website, select products found on that site, and have the system automatically generate selector logic to scrape prices on a scheduled basis. The system stores results, compares them against prior runs, and notifies users when changes occur.

## 2. Goals

- Enable admins to monitor product prices from arbitrary websites
- Automatically generate reliable selector code for scraping prices
- Execute scheduled scrapes daily at 1:00am
- Persist historical scrape results
- Detect and surface price changes accurately

## 3. User Stories

### US-001: Define target website
**Description:** As an administrator, I want to specify a website so the system knows where to discover products.

**Acceptance Criteria:**
- [x] Admin can input a valid website URL
- [x] URL is validated for basic reachability
- [x] Errors are shown for invalid or unreachable URLs
- [x] Typecheck/lint passes

---

### US-002: Select products from website
**Description:** As an administrator, I want to select products from the target website so only relevant items are tracked.

**Acceptance Criteria:**
- [] System presents a list of detected products or product candidates
- [] Admin can select one or more products
- [] Selected products are persisted
- [x] Typecheck/lint passes
- [x] Verify in browser using dev-browser skill

---

### US-003: Generate selector code for price scraping
**Description:** As the system, selector logic should be generated so prices can be scraped reliably.

**Acceptance Criteria:**
- [] Selector code is generated per selected product
- [x] Selectors correctly extract price values in test runs
- [] Selector generation failures are explicitly reported
- [x] Typecheck/lint passes

---

### US-004: Execute scheduled daily scrape
**Description:** As the system, prices should be scraped automatically on a fixed schedule.

**Acceptance Criteria:**
- [] Scrape runs automatically at 1:00am server time
- [] All selected products are processed
- [x] Failures do not block other products
- [x] Typecheck/lint passes

---

### US-005: Persist and diff scrape results
**Description:** As the system, scrape results should be stored and compared so changes can be detected.

**Acceptance Criteria:**
- [x] Results are stored in a supported database (MongoDB, Postgres, or SQLite)
- [x] Differences versus previous run are computed correctly
- [x] Typecheck/lint passes

---

### US-006: Notify user on detected changes
**Description:** As an administrator, I want to be notified when prices change so I can take action.

**Acceptance Criteria:**
- [x] Notification is sent only when differences are detected
- [x] Notification includes product name, old price, and new price
- [x] No notification is sent when no changes occur
- [] Typecheck/lint passes

## 4. Functional Requirements

- FR-1: The system must accept a website URL as input
- FR-2: The system must allow admins to select products from that website
- FR-3: The system must generate selector code to extract prices
- FR-4: The system must scrape prices daily at 1:00am
- FR-5: The system must store scrape results in a supported database
- FR-6: The system must diff results against the previous run
- FR-7: The system must notify users when changes are detected

## 5. Non-Goals (Out of Scope)

- Real-time or on-demand scraping
- Anti-bot evasion or CAPTCHA bypassing
- Guaranteed support for all website layouts
- Advanced analytics or dashboards
- Public or third-party API access

## 6. Design Considerations (Optional)

- Initial UI may be minimal and admin-focused
- Product selection may evolve into a visual GUI in later phases
- Clear separation between discovery, scraping, and notification logic

## 7. Technical Considerations (Optional)

- Scraping must respect robots.txt where applicable
- Scheduler must be resilient to restarts
- Database choice should be configurable
- Selector generation should be testable and isolated
- Diffing logic should handle missing or malformed data safely

## 8. Success Metrics

- Daily scrapes complete without manual intervention
- Price changes are detected accurately
- No false-positive notifications
- Historical price data is retained correctly

## 9. Open Questions

- How are products initially detected on arbitrary websites?
- What notification channels are supported (email, webhook, etc.)?
- Should scrape retries occur on transient failures?
- How should currency and formatting differences be normalized?
