#!/usr/bin/env python3
"""Keep manual pane-border labels synchronized with Herdr pane IDs."""
from __future__ import annotations

import json
import os
import subprocess
import sys


def herdr(*args: str) -> dict:
    p = subprocess.run(["herdr", *args], text=True, capture_output=True, check=True)
    return json.loads(p.stdout)


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] != "sync":
        print("usage: pane_labels.py sync", file=sys.stderr)
        return 2

    workspaces = herdr("workspace", "list")["result"]["workspaces"]
    changed = 0
    for workspace in workspaces:
        wid = workspace["workspace_id"]
        panes = herdr("pane", "list", "--workspace", wid)["result"]["panes"]
        for pane in panes:
            pane_id = pane["pane_id"]
            agent = pane.get("agent")
            label = f"{pane_id} · {agent}" if agent else pane_id
            # Manual names are rendered in the pane border and do not alter PTY output.
            herdr("pane", "rename", pane_id, label)
            changed += 1

    print(json.dumps({"status": "synced", "panes": changed}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
