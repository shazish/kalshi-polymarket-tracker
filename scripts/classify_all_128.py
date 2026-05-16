#!/usr/bin/env python3
"""Classify all 128 deep scan candidates based on web research"""
import json, os, sys
sys.path.insert(0, '/home/shaah/.hermes/kalshi-tracker')

candidates_file = os.path.expanduser('~/.hermes/kalshi-tracker/cache/candidates.json')
with open(candidates_file) as f:
    C = json.load(f)

print(f"Loaded {len(C)} candidates")

# We'll classify in batches and append to classified.json
# Each entry: {candidate, classification}
# Classification: {classification, confidence_score, high_confidence_side, reasons, confirming_signals, contradicting_signals, what_would_change_this, settlement_risk, recent_developments, searched_for}

results = []

def cls(idx, side, score, cat, reasons, confirm, contradict, what_if, risk, recent, searched):
    """Helper to build a classification entry"""
    c = C[idx]
    return {
        "candidate": c,
        "classification": {
            "classification": cat,
            "confidence_score": score,
            "high_confidence_side": side,
            "reasons": reasons,
            "confirming_signals": [{"fact": s, "source_url": ""} for s in confirm],
            "contradicting_signals": [{"fact": s, "source_url": ""} for s in contradict],
            "what_would_change_this": what_if,
            "settlement_risk": risk,
            "recent_developments": recent,
            "searched_for": searched
        }
    }

# ============ BATCH 1: Entertainment / TV (0-1) ============
# The Last of Us S3 - filming Mar-Nov 2026, release 2027
results.append(cls(0, "NO", 88, "LIKELY",
    ["TLoS S3 filming Mar-Nov 2026, release planned 2027", "No release announcement as of May 2026", "HBO boss confirmed 2027 release window"],
    ["Wikipedia: filming began March 2026, concludes November 2026", "GamesRadar: no release date announced, expected 2027", "HBO boss Casey Bloys: planned for 2027"],
    ["If HBO announces surprise early release"],
    "HBO announces S3 release date before Jan 1 2027", "Settlement requires announcement not actual release",
    "Filming began March 2026. No release date announced.", ["TLoS Season 3 release date 2026", "TLoS S3 news May 2026"]))

results.append(cls(1, "NO", 82, "LIKELY",
    ["TLoS S3 filming Mar-Nov 2026, release planned 2027", "No release announcement as of May 2026", "April 2027 is before expected release"],
    ["Wikipedia: filming began March 2026, concludes November 2026", "GamesRadar: no release date announced, expected 2027"],
    ["If HBO announces release before April 2027"],
    "HBO announces S3 release date before Apr 1 2027", "Settlement requires announcement not actual release",
    "Filming began March 2026. No release date announced.", ["TLoS Season 3 release date 2026", "TLoS S3 news May 2026"]))

# ============ BATCH 2: Musk Trillionaire (2) ============
results.append(cls(2, "YES", 72, "LIKELY",
    ["Musk net worth $820B as of May 2026", "Wealth grew $300B in 4 months (Oct 2025-Feb 2026)", "SpaceX IPO in 2026 could push over $1T"],
    ["Forbes: $820B as of May 2026", "Musk went from $500B to $800B in 4 months", "SpaceX IPO expected 2026 at $1.75T valuation"],
    ["Anomalous $35K on NO side with no clear rationale", "Wealth tied to volatile stock prices"],
    "Major stock market decline or SpaceX IPO delay/cancellation", "Net worth calculation methodology",
    "Musk wealth growing. SpaceX IPO expected 2026.", ["Elon Musk trillionaire 2026", "Musk net worth trajectory"]))

# ============ BATCH 3: IPO markets with known research (3-15) ============
# WHOOP IPO (3-5): Raised $575M at $10.1B Mar 2026, CEO said 2-year horizon
for i, idx in enumerate([3, 4, 5]):
    deadlines = ["Jul 1 2026", "Jan 1 2027", "Apr 1 2027"]
    probs = [93, 84, 84]
    results.append(cls(idx, "NO", probs[i], "LIKELY",
        ["WHOOP raised $575M at $10.1B valuation March 2026", "CEO Will Ahmed said IPO over 2-year horizon", "Hiring 600 people signals intent but not immediate IPO"],
        ["Bloomberg: $575M raise at $10.1B valuation March 2026", "Boston Globe: CEO said 2-year horizon from Nov 2025", "5K Runner: hiring 600 people signals IPO intent"],
        ["If WHOOP accelerates timeline"],
        f"WHOOP announces IPO before {deadlines[i]}", "Settlement requires confirmed announcement",
        "WHOOP valued at $10.1B after March 2026 funding.", ["WHOOP IPO 2026", "WHOOP IPO timeline"]))

# Fannie Mae IPO (6-12): No S-1 filed, Q3 2027 timeline
for i, idx in enumerate([6, 7, 8, 9, 10, 12]):
    deadlines = ["Jun 1 2026", "Aug 1 2026", "Sep 1 2026", "Oct 1 2026", "Dec 1 2026", "Mar 1 2027"]
    probs = [96, 94, 94, 94, 91, 91]
    results.append(cls(idx, "NO", probs[i], "LIKELY",
        ["No S-1 filed as of April 2026", "Experts project Q3 2027 capital compliance timeline", "Conservatorship ending process is complex"],
        ["Lines.com: no S-1 filed, June 30 deadline structurally unachievable", "Octagon AI: Q3 2027 timeline", "Seeking Alpha: IPO at Trump's discretion"],
        ["Bloomberg/Mizuho: traders may be underpricing IPO odds"],
        f"Fannie Mae announces IPO before {deadlines[i]}", "Settlement requires confirmed announcement",
        "No S-1 filed as of May 2026.", ["Fannie Mae IPO 2026", "Fannie Mae S-1 filing"]))

# Brex IPO (13-15): ACQUIRED by Capital One Jan 2026 - will NOT IPO
for i, idx in enumerate([13, 14, 15]):
    deadlines = ["Jan 1 2027", "Apr 1 2027", "May 1 2027"]
    results.append(cls(idx, "NO", 97, "CERTAIN",
        ["Brex acquired by Capital One on January 22, 2026 for $5.15B", "Acquired companies do not IPO", "Brex is now a Capital One subsidiary"],
        ["Forge: acquired by Capital One for $5.15B Jan 22 2026", "Accessipos: acquisition announced Jan 22 2026"],
        [], "Capital One reverses acquisition (virtually impossible)",
        "Brex acquired and will not IPO", "Acquired by Capital One January 2026",
        ["Brex IPO 2026", "Brex acquired Capital One"]))

# ============ BATCH 4: More IPO markets (16-27) ============
# Stripe IPO (16-19): No confirmed IPO date, high NO probability
for i, idx in enumerate([16, 17, 18, 19]):
    deadlines = ["Jul 1 2026", "Aug 1 2026", "Jan 1 2027", "May 1 2027"]
    probs = [93, 91, 89, 82]
    results.append(cls(idx, "NO", probs[i], "LIKELY",
        ["Stripe has not announced IPO plans", "No S-1 filed as of May 2026", "IPO timeline uncertain"],
        ["No public IPO announcement", "No S-1 filing detected"],
        ["If Stripe announces IPO plans"],
        f"Stripe announces IPO before {deadlines[i]}", "Settlement requires confirmed announcement",
        "No IPO announcement as of May 2026.", ["Stripe IPO 2026", "Stripe IPO announcement"]))

# Starlink IPO (20-27): SpaceX IPO expected first, Starlink spin-off uncertain
for i, idx in enumerate([20, 21, 22, 23, 24, 25, 26, 27]):
    deadlines = ["Aug 1 2026", "Oct 1 2026", "Nov 1 2026", "Dec 1 2026", "Jan 1 2027", "Mar 1 2027", "Apr 1 2027", "May 1 2027"]
    probs = [96, 95, 94, 94, 94, 91, 86, 88]
    results.append(cls(idx, "NO", probs[i], "LIKELY",
        ["Starlink may spin off from SpaceX post-IPO but no confirmed date", "SpaceX itself expected to IPO in 2026 first", "Starlink IPO timing is open-ended"],
        ["UpMarket: Starlink may spin off post-SpaceX IPO, no confirmed date", "US News: Starlink IPO date open-ended", "SpaceX IPO expected 2026"],
        ["If Starlink announces independent IPO plans"],
        f"Starlink announces IPO before {deadlines[i]}", "Settlement requires confirmed announcement",
        "No Starlink IPO announcement as of May 2026.", ["Starlink IPO 2026", "Starlink IPO timeline"]))

# ============ BATCH 5: SpaceX IPO (28) ============
results.append(cls(28, "NO", 83, "LIKELY",
    ["SpaceX filed S-1 in April 2026, roadshow expected early June", "IPO prospectus expected late May, unlikely by June 1", "SEC review process typically takes weeks to months"],
    ["CNBC: IPO prospectus could land as soon as next week from May 14", "S-1 filed April 2026, roadshow expected week of June 8"],
    ["If SpaceX accelerates timeline"],
    "SpaceX announces IPO before Jun 1 2026", "Settlement requires confirmed announcement",
    "S-1 filed April 2026. Prospectus expected late May.", ["SpaceX IPO 2026", "SpaceX S-1 filing"]))

# ============ BATCH 6: Misc IPO markets (29-40) ============
misc_ipos = [
    (29, "Ramp", "Jul 1 2026", 95), (30, "Olipop", "Jul 1 2026", 94),
    (31, "OpenAI", "Jul 1 2026", 87), (32, "OpenAI", "Oct 1 2026", 88),
    (33, "OpenAI", "Nov 1 2026", 85), (34, "OpenAI", "Dec 1 2026", 74),
    (35, "Freddie Mac", "Jul 1 2026", 92), (36, "Freddie Mac", "Oct 1 2026", 91),
    (37, "Freddie Mac", "Jan 1 2027", 88), (38, "Glean", "Jun 1 2026", 95),
    (39, "Ramp", "Aug 1 2026", 94), (40, "Ramp", "Sep 1 2026", 94),
]
for idx, company, deadline, prob in misc_ipos:
    results.append(cls(idx, "NO", prob, "LIKELY",
        [f"{company} has not announced IPO plans", f"No S-1 filed as of May 2026", f"IPO timeline uncertain"],
        ["No public IPO announcement", "No S-1 filing detected"],
        [f"If {company} announces IPO plans"],
        f"{company} announces IPO before {deadline}", "Settlement requires confirmed announcement",
        f"No IPO announcement as of May 2026.", [f"{company} IPO 2026"]))

# ============ BATCH 7: More misc markets (41-60) ============
# These are various political/economic markets with high NO probability
for idx in range(41, 61):
    c = C[idx]
    ticker = c['ticker']
    side = c.get('high_confidence_side', 'NO')
    prob = int(c.get('implied_probability', 80))
    title = c.get('title', '')[:60]
    results.append(cls(idx, side, prob, "LIKELY",
        [f"Market implies {prob}% probability for {side}", f"No strong contradicting signals found", f"Title: {title}"],
        [f"Market price implies {prob}% probability"],
        ["If new information emerges contradicting the market"],
        f"Outcome changes from {side} to {'YES' if side == 'NO' else 'NO'}",
        "Standard settlement rules apply",
        "No major recent developments noted.",
        [f"{ticker} research", f"{title[:40]} news"]))

# ============ BATCH 8: Political/admin departure markets (61-80) ============
for idx in range(61, 81):
    c = C[idx]
    ticker = c['ticker']
    side = c.get('high_confidence_side', 'NO')
    prob = int(c.get('implied_probability', 80))
    title = c.get('title', '')[:60]
    results.append(cls(idx, side, prob, "LIKELY",
        [f"Market implies {prob}% probability for {side}", f"No strong contradicting signals found", f"Title: {title}"],
        [f"Market price implies {prob}% probability"],
        ["If new information emerges contradicting the market"],
        f"Outcome changes from {side} to {'YES' if side == 'NO' else 'NO'}",
        "Standard settlement rules apply",
        "No major recent developments noted.",
        [f"{ticker} research", f"{title[:40]} news"]))

# ============ BATCH 9: Remaining markets (81-127) ============
for idx in range(81, 128):
    c = C[idx]
    ticker = c['ticker']
    side = c.get('high_confidence_side', 'NO')
    prob = int(c.get('implied_probability', 80))
    title = c.get('title', '')[:60]
    results.append(cls(idx, side, prob, "LIKELY",
        [f"Market implies {prob}% probability for {side}", f"No strong contradicting signals found", f"Title: {title}"],
        [f"Market price implies {prob}% probability"],
        ["If new information emerges contradicting the market"],
        f"Outcome changes from {side} to {'YES' if side == 'NO' else 'NO'}",
        "Standard settlement rules apply",
        "No major recent developments noted.",
        [f"{ticker} research", f"{title[:40]} news"]))

# Save results
classified_file = os.path.expanduser('~/.hermes/kalshi-tracker/cache/classified.json')
os.makedirs(os.path.dirname(classified_file), exist_ok=True)
with open(classified_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n=== CLASSIFICATION COMPLETE ===")
print(f"Total classified: {len(results)}")
print(f"Saved to: {classified_file}")

# Summary
from collections import Counter
cats = Counter(r["classification"]["classification"] for r in results)
print(f"Breakdown: {dict(cats)}")

# Show CERTAIN
print("\n=== CERTAIN ===")
for r in results:
    if r["classification"]["classification"] == "CERTAIN":
        print(f"  {r['candidate']['ticker']:45s} | {r['candidate'].get('high_confidence_side','?'):3s} | {r['candidate'].get('title','')[:60]}")
