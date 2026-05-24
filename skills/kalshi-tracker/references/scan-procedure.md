# Kalshi Tracker — Direct Scan Procedure

_Use this procedure when running scans as a Hermes cron job. Do NOT use
`python orchestrator.py` for deep/incremental — it times out._

## Recommended: Events-Based Scanning (Fastest)

The `/events?with_nested_markets=true` endpoint is ~10x faster than paginating
`/markets` because each call returns both the event and all its nested markets.

```python
import requests, json, os, time

BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"

def to_cents(d):
    if d is None: return 0
    return int(round(float(d) * 100))

TARGET_CATS = {"Politics", "Economics", "Entertainment", "Weather", "World", "Elections"}
PRICE_THRESHOLD = 90
DEEP_PRICE_THRESHOLD = 80
SPREAD_MAX = 3
MIN_VOLUME = 50
MAX_PAGES = 50

candidates = []
cursor = None
events_scanned = 0
markets_scanned = 0
consecutive_429s = 0

for page in range(MAX_PAGES):
    params = {"status": "open", "limit": 100, "with_nested_markets": "true"}
    if cursor:
        params["cursor"] = cursor

    resp = requests.get(f"{BASE_URL}/events", params=params, timeout=15)

    if resp.status_code == 429:
        wait = float(resp.headers.get("Retry-After", 2 ** (consecutive_429s + 1)))
        time.sleep(wait)
        consecutive_429s += 1
        if consecutive_429s >= 3:
            break
        continue

    if resp.status_code != 200:
        break

    consecutive_429s = 0
    events = resp.json().get("events", [])
    if not events:
        break

    for e in events:
        events_scanned += 1
        if e.get("category") not in TARGET_CATS:
            continue

        for m in e.get("markets", []):
            markets_scanned += 1

            # Skip multivariate combo markets (multi-leg sports bets)
            title = (m.get("title", "") or "").lower()
            comma_legs = [s.strip() for s in title.split(",")
                          if s.strip().startswith(("yes ", "no "))]
            if len(comma_legs) > 2:
                continue

            yes_bid = to_cents(m.get("yes_bid_dollars"))
            yes_ask = to_cents(m.get("yes_ask_dollars"))
            no_bid = to_cents(m.get("no_bid_dollars"))
            no_ask = to_cents(m.get("no_ask_dollars"))
            volume = float(m.get("volume_fp", 0) or 0)

            max_p = max(yes_bid, no_bid)
            if max_p < PRICE_THRESHOLD:
                continue

            spread = (yes_ask - yes_bid) if yes_bid >= no_bid else (no_ask - no_bid)
            if spread > SPREAD_MAX:
                continue
            if volume < MIN_VOLUME:
                continue

            side = "YES" if yes_bid >= no_bid else "NO"
            candidates.append({
                "ticker": m.get("ticker", ""),
                "title": e.get("title", ""),
                "event_ticker": e.get("event_ticker", ""),
                "yes_bid": yes_bid, "yes_ask": yes_ask,
                "no_bid": no_bid, "no_ask": no_ask,
                "volume": volume,
                "close_date": m.get("close_time", ""),
                "rules_primary": m.get("rules_primary", ""),
                "high_confidence_side": side,
                "implied_probability": max_p,
                "category": e.get("category", ""),
            })

    cursor = resp.json().get("cursor")
    if not cursor:
        break

    time.sleep(0.15)  # proactive throttling

print(f"Scanned {events_scanned} events, {markets_scanned} markets → {len(candidates)} candidates")

cache_dir = os.path.expanduser("~/.hermes/kalshi-tracker/cache")
os.makedirs(cache_dir, exist_ok=True)
with open(f"{cache_dir}/candidates.json", "w") as f:
    json.dump(candidates, f, indent=2)
```

### Key Differences from Old Approach

| Old (broken) | New (working) |
|---|---|
| Paginate `/markets` (2000+ markets, 20+ pages) | Paginate `/events?with_nested_markets=true` (5000 events, 50 pages) |
| Filter by `series_ticker` (always null in API) | Filter by `event.category` in target categories |
| No delay between requests → 429s | 150ms throttle + Retry-After respect |
| `_enrich_candidate()` calls `get_event()` per market | Events come with nested markets |
| ~5+ minutes for full scan | ~15 seconds for 5000 events |

## Step 2: Classify Each Candidate (Agent LLM)

For each candidate in `cache/candidates.json`:

1. Build classification prompt using `classifier.build_classifier_prompt(candidate)`
2. Prepend `classifier.CLASSIFIER_SYSTEM_PROMPT`
3. Perform >=2 web searches about the event
4. Include search results in the prompt
5. Output structured JSON matching the schema
6. Validate with `classifier.validate_classification(output)`
7. Save to `cache/classified.json`

## Step 3: Run Opportunity Manager (Edge Calculation)

**Do NOT use `OpportunityManager.compute_edge()` directly** — it uses `implied_probability` as both market price and true probability, producing negative edge for all high-price markets.

**Correct approach:** Use the classifier's `confidence_score` as the true probability estimate:

```python
for c in classified:
    if c["classification"] != "CERTAIN":
        continue
    
    # Classifier's assessment of true probability
    true_prob = c["confidence_score"] / 100.0
    
    # Market price (what you pay)
    if c["high_confidence_side"] == "YES":
        market_price = c["yes_bid"] / 100.0
    else:
        market_price = c["no_bid"] / 100.0
    
    # Edge = true_prob - market_price
    edge_before_fees = true_prob - market_price
    
    # Fee estimate (quadratic model, ~1.5% average)
    fee = 0.015 * market_price * (1 - market_price) * 2
    edge_after_fees = edge_before_fees - fee
    
    # Kelly fraction (capped at 5%)
    if edge_after_fees > 0:
        odds = (1 - market_price) / market_price
        kelly = min(edge_after_fees / odds, 0.05)
        suggested_size = round(kelly * 1000, 2)  # $1000 bankroll
    else:
        kelly = 0
        suggested_size = 0
    
    # Filter: edge_after_fees >= 0.03 (3%)
    if edge_after_fees >= 0.03:
        # Check dedup (7-day TTL), then notify
        ...
```

**Example (May 2026):** Gasoline CPI NO at 94c, classifier confidence 97%:
- `edge = 0.97 - 0.94 = 0.03` (3.0%)
- `fee = 0.015 * 0.94 * 0.06 * 2 ≈ 0.0017`
- `edge_after_fees = 0.0283` (2.83%) — just below 3% threshold, not notified

**Key insight:** Even CERTAIN markets can have edge below the 3% threshold when the market price is already very high (94c+). This is expected — the market efficiently prices near-certainties. Structural impossibilities at 95c+ with 97%+ confidence typically yield 2-3% raw edge, which after fees may not clear the 3% bar.
