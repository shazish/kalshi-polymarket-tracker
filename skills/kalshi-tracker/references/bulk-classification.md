# Bulk Classification Script Pattern

When the deep scan produces 100+ candidates, classifying one-by-one is impractical.
Write a Python script to classify all candidates in one shot.

## Template

See `scripts/classify_all_140.py` for the current best-practice pattern (hybrid: individual + programmatic rules by market type).

## The `cls()` Helper — Must Normalize Signal Entries

The helper must normalize confirming_signals and contradicting_signals to handle mixed formats
(tuples of varying length, dicts, plain strings). Never use `for s, u in confirm` directly.

```python
def cls(idx, side, score, cat, reasons, confirm, contradict, what_if, risk, recent, searched):
    c = candidates[idx]
    clean_confirm = []
    for item in confirm:
        if isinstance(item, tuple):
            clean_confirm.append({"fact": item[0], "source_url": item[1] if len(item) > 1 else ""})
        elif isinstance(item, dict):
            clean_confirm.append(item)
        else:
            clean_confirm.append({"fact": str(item), "source_url": ""})
    # Same pattern for contradict
    ...
```

## Classification Heuristics

| Market Type | Horizon | Default Classification |
|-------------|---------|----------------------|
| IPO (no S-1 filed) | < 30 days | CERTAIN NO |
| IPO (no S-1 filed) | 30-90 days | CERTAIN NO |
| IPO (no S-1 filed) | 90+ days | LIKELY NO |
| IPO (S-1 filed, not yet priced) | Any | LIKELY YES |
| Political departure | Any | LIKELY NO |
| Economic extreme (e.g., unemployment > 8%) | Any | CERTAIN NO |
| Acquired company IPO | Any | CERTAIN NO |

## Agent-Driven Theme-Grouped Classification (Alternative)

When classifying 100+ candidates live (not via script), use a theme-grouped approach:

### When to Use This

- Deep scan produced 100-200 candidates where many share themes (IPO markets, Super Bowl markets, economic indicator series)
- You want the Agent to drive classification with live web research, not hardcoded answers
- The `cls()` helper script approach is impractical because you'd need to manually type 100+ classification objects

### Procedure

1. **List remaining candidates** grouped by theme — IPO, Starlink, Trump approval, economic indicators, election seats, etc.

2. **Research each theme once** — parallel web searches for the first candidate in each group. Learn the key facts (e.g., "Starlink is a SpaceX subsidiary, not IPOing separately"; "DOJ dropped Powell probe April 24").

3. **Batch classify by theme** — for each theme, write a loop that applies the same reasoning pattern to all candidates in that group. Use a helper function that wraps `validate_classification()` and handles minimum requirements (≥3 searched_for, ≥3 reasons for CERTAIN, ≥3 confirming_signals).

4. **Fix validation in bulk** — after each batch, re-validate and fix common failures (usually just missing search queries or too-few confirming signals).

5. **Save incrementally** — write to `classified.json` after each major theme batch to avoid losing work if interrupted.

### Theme Grouping Examples

| Theme | Pattern | Common Classification |
|-------|---------|----------------------|
| IPO (same company, different deadlines) | All share the same fundamental thesis (filed? acquired? pre-revenue?) | Same classification for all deadlines, declining confidence for longer horizons |
| Super Bowl headliner (same event, different artists) | All share same event context (SB LXI date, selection process) | All NO for specific artists, varied confidence by likelihood |
| Trump approval (same metric, different thresholds) | Same current data point, different thresholds to evaluate | Lower thresholds = more LIKELY YES; higher = CERTAIN/LIKELY NO |
| U3 unemployment (same metric, different levels) | Current 4.3%, extrapolate to threshold | 8% = CERTAIN NO, 15% = CERTAIN NO, 12% = CERTAIN NO |
| Economic indicators (GDP, CPI, Sahm, Fed) | All based on existing economic data + forecasts | Most LIKELY NO unless threshold is extremely improbable |
| Election seats (House/Senate) | Same election, different seat counts to evaluate | Closer to current baseline = more uncertain; extreme counts = CERTAIN |
| Musk/Trump admin (specific person targets) | Same person/dynamic, different targets | All LIKELY NO for specific person outcomes unless structural |

### Implementation Pattern

```python
def quick_classify(ticker, cls, side, conf, reasons, confirm, what, searched):
    c = find(ticker)
    cl = {
        "classification": cls, "confidence_score": conf, "high_confidence_side": side,
        "reasons": reasons[:5], "confirming_signals": confirm[:3],
        "contradicting_signals": [], "what_would_change_this": what,
        "settlement_risk": "Low.", "recent_developments": "Standard monitoring.",
        "searched_for": searched[:5],
    }
    cl = validate_classification(cl, rules=c.get('rules_primary', ''))
    classified.append({"candidate": c, "classification": cl})
```

Then invoke in a loop:
```python
# Classify all 7 Olipop IPO markets with the same research
for ticker in olipop_tickers:
    quick_classify(ticker, "CERTAIN", "NO", 97,
        ["Olipop has not filed for IPO", "No S-1 filing exists", ...],
        confirm_signals, what_if, searches)
```

### Pitfalls (this approach)

1. **Shared confirming_signals may hit metric consistency checks** — if settlement rules contain keywords like "headline" or "annualized", the shared signals may not mention them. Either add the keyword to shared signals or accept the auto-downgrade to LIKELY.
2. **Ensure minimum 3 searched_for per candidate** — the loop can pad: `while len(searched) < 3: searched.append("supplementary")`.
3. **Write the file after each theme batch** — not just at the end. If the run is interrupted, you lose everything since the last save.
4. **Theme-grouped labels look generic in the Excel report** — add a batch post-process step to fill in specific confirming_signal URLs if needed for audit.

## Pitfalls (Scripted Approach)

1. **Tuple unpacking**: Never use `for s, u in confirm` — normalize through isinstance checks.
2. **Index mismatch**: `idx` is the array index in candidates.json, not the clustered output number.
3. **Always validate**: Run `validate_classification()` — auto-downgrades CERTAIN if rules fail.
