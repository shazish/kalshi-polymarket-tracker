# skills/

Embedded skill copies from `~/.hermes/skills/`.

These mirror the canonical skills in `~/.hermes/skills/` but are kept
in the kalshi-tracker repo so that anyone who clones the repo gets the
operational documentation without needing Hermes Agent.

## Structure

```
skills/
├── kalshi-tracker/              # Full project manual
│   ├── SKILL.md                 # Architecture, key files, how-to-run
│   └── references/              # Pitfalls, scan procedures, settlement, audits
│       ├── pitfalls.md          # (Default read first)
│       ├── two-phase-pipeline.md
│       ├── scan-procedure.md
│       └── ...
└── two-phase-kalshi-classifier/ # Classification playbook
    ├── SKILL.md
    └── references/
        ├── fact-check-cases-20260523.md
        └── resolution-rules.md
```

## Maintenance

These are copies, not symlinks. To refresh after `~/.hermes/skills/` changes:

```bash
cd ~/kalshi-tracker
rm -rf skills/kalshi-tracker skills/two-phase-kalshi-classifier
cp -r ~/.hermes/skills/kalshi-tracker skills/
cp -r ~/.hermes/skills/two-phase-kalshi-classifier skills/
```

The canonical source is `~/.hermes/skills/`. This repo may lag behind.
