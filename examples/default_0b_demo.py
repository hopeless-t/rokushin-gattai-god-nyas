"""Fetch (once) and run the optional official default 0B starter asset."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from godnyas import AssetUnavailable, load_default_0b

try:
    model = load_default_0b()
except AssetUnavailable as exc:
    raise SystemExit(str(exc))

text = sys.argv[1] if len(sys.argv) > 1 else "ベンチ回して"
print(json.dumps(model.respond(text), ensure_ascii=False, indent=2))
