# Checking Kalshi Resolution Rules

Before marking any candidate as CERTAIN (especially with high edge), verify the resolution rules against the actual contract terms. Subagents frequently hallucinate specific numeric claims (dates, durations, thresholds) even when the core direction is correct.

## How to Check

### 1. Find the contract PDF

Kalshi publishes contract terms as PDFs on S3. The naming convention is:

```
https://kalshi-public-docs.s3.amazonaws.com/contract_terms/{BASE_TICKER}.pdf
```

For example, GOVTSHUTLENGTH → `{BASE_TICKER}` = `GOVTSHUTLENGTH`

Extract the base ticker from the candidate's `rules_primary` field or the ticker itself. The `rules_primary` field typically references the definition contract (e.g., "as defined in the GOVTSHUTLENGTH contract").

### 2. Extract text from the PDF

Use `execute_code` with PyPDF2 or pypdf:

```python
import requests, io
resp = requests.get("https://kalshi-public-docs.s3.amazonaws.com/contract_terms/{TICKER}.pdf", timeout=10)
pdf_file = io.BytesIO(resp.content)
reader = PyPDF2.PdfReader(pdf_file)
for page in reader.pages:
    print(page.extract_text())
```

Alternatively, use the browser tool to navigate to the PDF URL and use browser_vision to read it.

### 3. Verify the settlement source hierarchy

The contract defines Source Agencies in hierarchical order:

- **Primary**: Usually OMB, OPM, or government agencies
- **Secondary**: News outlets (NYT, WSJ, AP, Reuters, Bloomberg, etc.)

**Wikipedia is NEVER a valid settlement source.** Do not accept Wikipedia citations for CERTAIN classifications unless cross-verified against a primary or secondary source.

### 4. Check what you need to verify

| Claim type | What to verify | Where to check |
|-----------|---------------|----------------|
| Event occurred | Primary source (government announcement) or secondary (AP, Reuters) | News search, official statements |
| Event duration | Primary source or secondary | Multiple secondary sources preferred |
| Threshold met (e.g., "inflation > X%") | Government data release (BLS, BEA) | Official data release |
| Timeline | Event date vs contract expiration | Source agency data |

### 5. Known pitfalls

- **Hallucinated sources**: DeepSeek subagents may invent source URLs or fabricate specific numbers (e.g., "76 days" instead of the actual 4 days). If a number sounds extraordinary, verify it.
- **Wikipedia as sole source**: Rejected for CERTAIN — Wikipedia is not in any Kalshi contract's settlement source list.
- **Payroll companies as political sources**: A source like Paychex (payroll processor) is not a valid settlement source for government shutdown contracts.
- **Price vs edge sanity check**: If the market is at 60¢ and you claim 60% edge, ask why arbitrageurs haven't captured it. A large gap between market price and your confidence threshold is a red flag — investigate.
