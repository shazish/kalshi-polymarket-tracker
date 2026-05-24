# Agentic Prediction Market Pipelines — Landscape Research

_Session: May 2026. Research into existing agentic betting market analysis pipelines and actionable ideas._

## Key Projects

### 1. Semantic Trading (IBM + Columbia, Dec 2025)
- **Paper**: arXiv:2512.02436
- **Idea**: Cluster prediction markets by topic using NLU, then discover relationships (same-outcome, opposite-outcome, implied complements) within clusters
- **Pipeline**: Fetch markets → cluster by title/metadata semantics → identify dependent pairs → trade the second when the first resolves
- **Results**: 60-70% accuracy on relationship detection, ~20% avg return over week-long trades
- **Actionable for us**: Cluster markets within categories before classification. E.g., all "SpaceX IPO by date X" markets are related — if one resolves YES, others cascade. Detect contradictions (e.g., "IPO by June" at 90c AND "IPO by September" at 10c).

### 2. PolySwarm (Multi-agent LLM framework, Apr 2026)
- **Paper**: arXiv:2604.03888
- **Idea**: 50 diverse LLM personas debate and trade on Polymarket asynchronously
- **Architecture**: Multiple agents with different personas → structured debate → ensemble aggregation with Bayesian combination against market priors
- **Key insight**: Single-model methods suffer from hallucination/overconfidence. Multi-agent debate + persona diversity reduces this.
- **Actionable for us**: Replace single classifier with 2-3 agents (bullish, bearish, devil's advocate) + supervisor aggregator. The devil's advocate step we have is good but it's the same model arguing with itself — truly independent agents would be stronger.

### 3. Olas Polystrat (Production agent, Feb 2026)
- **Idea**: Users define strategy in plain English → agent auto-discovers probability deviations in markets settling within 4 days → executes trades
- **Key insight**: Focus on short-horizon markets (settling within 4 days) where mispricings are most exploitable because there's less time for the market to self-correct
- **Actionable for us**: **IMPLEMENTED May 2026** — Added urgency scoring and time-adjusted edge thresholds. Markets closing sooner are prioritized. Small edges on near-term markets can trigger notification via annualized threshold.

### 4. Predly.ai (Commercial product)
- **Idea**: AI-calculated "true" probabilities vs market prices → mispricing alerts
- **Three-step process**: Analyze news/sentiment → calculate true probability → detect discrepancies
- **Claim**: 89% alert accuracy on Kalshi + Polymarket
- **Actionable for us**: Add explicit sentiment analysis step (especially for political markets). Our classifier does web search but doesn't explicitly score sentiment.

### 5. Simmer (Open-source agent harness)
- **Idea**: Unified API for AI agents to trade Polymarket + Kalshi with paper trading, safety rails, self-custody wallets
- **Key insight**: Abstracted both platforms into one REST API with safety limits
- **Actionable for us**: When ready to go from analysis → actual trading, Simmer simplifies execution. They also have paper trading for validation.

### 6. PredictionMarketBench (Backtesting framework, Feb 2026)
- **Paper**: arXiv:2602.00133
- **Idea**: SWE-bench-style benchmark for backtesting trading agents on historical prediction market data with LOB replay
- **Key insight**: Deterministic event-driven replay of historical order book data lets you test strategies without lookahead bias
- **Actionable for us**: Build a replay-based backtest (feed historical market snapshots → run classifier → compare to actual resolution) to get real accuracy metrics instead of relying on self-reported confidence.

### 7. Multi-Agent Debate / Ensemble Forecasting (Multiple papers)
- **Key insight**: Agents with different profiles debate, then a supervisor reconciles. Confidence gating overrides naive averaging when evidence is strong. Disagreement between agents is informative — flagging high-disagreement candidates for extra scrutiny (or skipping them) reduces false CERTAIN classifications.
- **Actionable for us**: Flag candidates where initial classifier pass and devil's advocate disagree for extra scrutiny or skip.

## Summary of Ideas (Priority Order)

1. ✅ **Time-to-resolution prioritization** (from Polystrat) — IMPLEMENTED May 2026
2. **Market clustering + relationship detection** (from Semantic Trading) — next candidate
3. **Multi-agent ensemble** (from PolySwarm) — medium-term improvement
4. **Sentiment analysis layer** (from Predly) — quick win for political markets
5. **Proper backtesting harness** (from PredictionMarketBench) — for validation
6. **Unified execution API** (from Simmer) — when ready to trade
