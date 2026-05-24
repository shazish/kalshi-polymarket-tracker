# Phase 3 Fact-Check Case Studies — May 23, 2026 Anomaly Scan

## Case 1: Todd Blanche — "Leave Deputy Attorney General before 2027"

**Initial classification:** CERTAIN/YES (confidence 98)
**Fact-check result:** DOWNGRADED to UNCLEAR

**What went wrong:** The research found that Blanche was "elevated to Acting Attorney General" and interpreted this as "left DAG." In reality, DOJ.gov shows he serves as BOTH Acting Attorney General AND Deputy Attorney General simultaneously. He never left the DAG role.

**Lesson:** When a market asks "will [person] leave [position]," verify the person actually left that specific role — not that they were promoted to a different role while retaining the original.

**Key source:** https://www.justice.gov/ag/staff-profile/meet-acting-attorney-general-0

---

## Case 2: Government Shutdowns — "Exactly 2 distinct shutdowns in 2026"

**Initial classification:** CERTAIN/YES (confidence 97)
**Fact-check result:** DOWNGRADED to LIKELY/YES (confidence 78)

**What went wrong:** Wikipedia confirmed exactly 2 shutdowns (Jan 31-Feb 3, Feb 14-Apr 30), but Wikipedia is NOT a settlement source for Kalshi contracts. The GOVTSHUTDOWN contract specifies OMB/OPM as primary sources, with NYT/WSJ/AP/Reuters/Bloomberg/Guardian/Politico as secondary.

**Lesson:** Wikipedia can inform your reasoning but cannot be the basis for CERTAIN classification. Always verify against the contract's authorized settlement sources.

**Settlement source hierarchy (GOVTSHUTDOWN):**
- Primary: OMB, OPM
- Secondary: NYT, WSJ, AP, Reuters, Bloomberg, Guardian, Politico

**Wikipedia article:** https://en.wikipedia.org/wiki/2026_United_States_federal_government_shutdowns

---

## Case 3: OpenAI IPO — "Confirm IPO before Sep 1, 2026"

**Initial classification:** CERTAIN/NO (confidence 96)
**Fact-check result:** DOWNGRADED to UNCLEAR (confidence 55)

**What went wrong:** Research was conducted before breaking news. On May 20, 2026, Axios/CNBC/Forbes all reported OpenAI was preparing a confidential IPO filing THIS WEEK targeting a September debut. The research had concluded no filing would happen before Sep 1.

**Lesson:** Breaking news can invalidate research between Phase 1 and Phase 3. Always re-search CERTAIN candidates against current sources before finalizing, especially for fast-moving topics like IPOs.

**Key sources:**
- Axios: https://www.axios.com/2026/05/20/openai-ipo-spacex-musk
- CNBC: https://www.cnbc.com/2026/05/20/openai-ipo-filing.html

---

## Case 4: Fed Rate — "Upper bound above 3.50% after Apr 28, 2027 meeting"

**Initial classification:** CERTAIN/YES (confidence 99)
**Fact-check result:** CONFIRMED CERTAIN/YES

**Why it held:** The Fed held rates at 3.50%-3.75% on April 29, 2026. The upper bound (3.75%) is strictly above 3.50%. This was confirmed by the Federal Reserve's official website, which is the contract's settlement source.

**Settlement source:** https://www.federalreserve.gov/monetarypolicy/openmarket.htm
**Contract PDF:** https://kalshi-public-docs.s3.amazonaws.com/contract_terms/FED.pdf

**Note:** The opportunity manager flagged this as "contract already expired" — the Fed meeting was April 29, 2026 and the rate was already set. This market may have already settled. Always verify on Kalshi whether the market is still open for trading.

---

## Summary Table

| Ticker | Initial | Fact-Checked | Key Issue |
|--------|---------|--------------|-----------|
| KXTRUMPADMINLEAVE-26DEC31-TBLA | CERTAIN/YES | UNCLEAR | Role confusion — still serving as DAG |
| KXNUMSHUTDOWNS-27JAN01-T2 | CERTAIN/YES | LIKELY/YES | Wikipedia not a settlement source |
| KXIPOOPENAI-26SEP01 | CERTAIN/NO | UNCLEAR | Breaking news invalidated research |
| KXFED-27APR-T3.50 | CERTAIN/YES | CERTAIN/YES | Confirmed by Fed official source |
