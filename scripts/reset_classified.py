#!/usr/bin/env python3
"""Reset classified.json to empty array for re-classification."""
import json
with open('/home/shaah/kalshi-tracker/cache/classified.json', 'w') as f:
    json.dump([], f)
print("Reset classified.json to []")
