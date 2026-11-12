#!/usr/bin/env python3
"""
CAPSTONE (unit 9) — one trial against the running server.

    Terminal 1:  python serve.py                (with the cache OFF, see RUNNING.md)
    Terminal 2:  python capstone_trials.py --label before --trial 1

Sends the same 11 requests every trial, reads back the new lines in
logs/serve_log.jsonl, scores the five capstone criteria in criteria.md, and
writes everything to results/capstone_<label>_trial<N>.md.

Uses only the standard library, so there is nothing new to install.
"""

import argparse
import json
import statistics
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
LOG_PATH = ROOT / "logs" / "serve_log.jsonl"
RESULTS_DIR = ROOT / "results"

# Matching queries: every one has something real in data/listings.json.
MATCHING = [
    "vintage graphic tee under $30",
    "denim jacket under $50",
    "90s track jacket in size M",
    "silk slip dress in midi length under $40",
    "platform sneakers size 8",
]
# Matches nothing on purpose — the agent's own "no results" branch.
IMPOSSIBLE = ["designer ballgown size XXS under $5"]
# Bad input — each is a different way a caller can send garbage.
#   (name, raw body bytes, content type)
BAD_INPUTS = [
    ("empty JSON object",   b"{}",                         "application/json"),
    ("blank query",         b'{"query": "   "}',           "application/json"),
    ("not JSON at all",     b"hello",                      "text/plain"),
    ("JSON list, not dict", b'["vintage tee"]',            "application/json"),
    ("query is a number",   b'{"query": 123}',             "application/json"),
]
REQUIRED_FIELDS = ["ts", "status", "query", "outcome", "duration_s", "total_tokens"]
LATENCY_LIMIT_S = 8.0
TOKEN_LIMIT = 4000


def post(url, body: bytes, content_type: str):
    """Send one POST. Returns (status, parsed JSON or raw text, seconds)."""
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": content_type})
    start = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            status, raw = resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        status, raw = err.code, err.read().decode("utf-8", "replace")
    seconds = time.perf_counter() - start
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = raw  # Flask's HTML crash page lands here
    return status, data, seconds


def read_log_lines():
    if not LOG_PATH.exists():
        return []
    return LOG_PATH.read_text(encoding="utf-8").splitlines()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:5000")
    parser.add_argument("--label", required=True, help="before or after")
    parser.add_argument("--trial", type=int, required=True, help="1, 2 or 3")
    args = parser.parse_args()
    ask_url = args.url.rstrip("/") + "/ask"

    lines_before = len(read_log_lines())
    sent, rows = 0, []

    print(f"Trial {args.trial} ({args.label}) → {ask_url}\n")
    for q in MATCHING + IMPOSSIBLE:
        body = json.dumps({"query": q}).encode()
        status, data, secs = post(ask_url, body, "application/json")
        sent += 1
        kind = "matching" if q in MATCHING else "impossible"
        rows.append({"kind": kind, "name": q, "status": status, "data": data, "secs": secs})
        print(f"  [{status}] {secs:5.1f}s  {kind:<10} {q}")
    for name, body, ctype in BAD_INPUTS:
        status, data, secs = post(ask_url, body, ctype)
        sent += 1
        rows.append({"kind": "bad", "name": name, "status": status, "data": data, "secs": secs})
        print(f"  [{status}] {secs:5.1f}s  bad input  {name}")

    time.sleep(0.5)  # let the last log line land
    new_lines = read_log_lines()[lines_before:]
    records = []
    for line in new_lines:
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            pass

    # ── score the five criteria ───────────────────────────────────────────────
    complete = [r for r in records if all(f in r for f in REQUIRED_FIELDS)]
    c1 = (len(complete), sent)

    bad = [r for r in rows if r["kind"] == "bad"]
    c2_pass = sum(1 for r in bad if r["status"] == 400
                  and isinstance(r["data"], dict) and r["data"].get("error"))
    c2 = (c2_pass, len(bad))

    fit_records = [r for r in records if r.get("outcome") == "fit_card"]
    c3_pass = sum(1 for r in fit_records if r["duration_s"] < LATENCY_LIMIT_S)
    c3 = (c3_pass, len(MATCHING))

    c4_pass = sum(1 for r in fit_records if 0 < r["total_tokens"] <= TOKEN_LIMIT)
    c4 = (c4_pass, len(MATCHING))

    c5_pass = 0
    for r in rows:
        d = r["data"] if isinstance(r["data"], dict) else {}
        if r["kind"] == "matching" and r["status"] == 200 and d.get("fit_card"):
            c5_pass += 1
        if r["kind"] == "impossible" and r["status"] == 200 and d.get("error") and not d.get("fit_card"):
            c5_pass += 1
    c5 = (c5_pass, len(MATCHING) + len(IMPOSSIBLE))

    scores = [
        ("1. Every request leaves a complete log record", c1),
        ("2. Bad input gets a 400 with a message", c2),
        (f"3. Matching query answers in under {LATENCY_LIMIT_S:.0f}s", c3),
        (f"4. One run costs at most {TOKEN_LIMIT} tokens", c4),
        ("5. Original agent still works over HTTP", c5),
    ]

    durations = [r["duration_s"] for r in fit_records]
    tokens = [r["total_tokens"] for r in fit_records]
    summary = []
    if durations:
        summary.append(f"successful runs: {len(fit_records)}, "
                       f"median {statistics.median(durations):.2f}s, "
                       f"max {max(durations):.2f}s")
    if tokens:
        summary.append(f"tokens per successful run: mean {statistics.mean(tokens):.0f}, "
                       f"min {min(tokens)}, max {max(tokens)}")

    print("\nScores this trial:")
    for name, (got, out_of) in scores:
        print(f"  {name:<48} {got}/{out_of}")
    for s in summary:
        print("  " + s)

    # ── write the evidence file ───────────────────────────────────────────────
    RESULTS_DIR.mkdir(exist_ok=True)
    out = RESULTS_DIR / f"capstone_{args.label}_trial{args.trial}.md"
    md = [f"# Capstone trial {args.trial} — {args.label}",
          f"Run at {datetime.now().isoformat(timespec='seconds')} against {ask_url}",
          "Produced by `capstone_trials.py::main`; log lines written by `serve.py::log_request`.",
          "", "## Scores", "", "| Criterion | Result |", "|---|---|"]
    md += [f"| {n} | {g}/{o} |" for n, (g, o) in scores]
    md += ["", *[f"- {s}" for s in summary], "", "## Responses", ""]
    for r in rows:
        shown = r["data"]
        if isinstance(shown, dict):
            shown = {k: shown.get(k) for k in ("error", "fit_card") if k in shown}
            shown = json.dumps(shown, ensure_ascii=False)
        shown = str(shown).replace("\n", " ")[:300]
        md.append(f"- **[{r['status']}] {r['kind']} — {r['name']}** ({r['secs']:.1f}s): {shown}")
    md += ["", "## New log lines (logs/serve_log.jsonl)", "", "```", *new_lines, "```", ""]
    out.write_text("\n".join(md), encoding="utf-8")
    print(f"\nWrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
