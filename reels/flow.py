"""Call the running flow-mcp server (Flow Studio, 127.0.0.1:8787) without an MCP session.

Usage: python flow.py <method> [args.json | '{"json": "inline"}']
Methods match the flow_* tools without the prefix: status, agent, wait, narrate, voices, ...
"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

method = sys.argv[1]
raw = sys.argv[2] if len(sys.argv) > 2 else "{}"
args = Path(raw).read_text(encoding="utf-8") if Path(raw).suffix == ".json" and Path(raw).exists() else raw
token = (Path.home() / ".flow-mcp" / "token").read_text().strip()
req = urllib.request.Request(f"http://127.0.0.1:8787/api/{method}", data=args.encode("utf-8"), method="POST",
                             headers={"content-type": "application/json", "x-flow-token": token})
try:
    with urllib.request.urlopen(req, timeout=960) as r:
        print(json.dumps(json.loads(r.read()), indent=1, ensure_ascii=False))
except urllib.error.HTTPError as e:
    sys.exit(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')}")
