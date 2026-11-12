#!/usr/bin/env python3
"""
FitFindr over HTTP. ← UNIT 9

    python serve.py                       run it on your machine
    gunicorn serve:app                    run it the way a host runs it

Everything else in this repo exits after one command. A host has nothing to
keep running, so a command line cannot be deployed. This file is the smallest
thing that can: it starts a web server, waits, and hands each request to the
same `run_agent()` your CLI calls. **No new agent logic lives here.** If your
loop works from `python app.py ask`, it works from here; if it doesn't, fix it
there, not in this file.

Two routes:

    POST /ask       {"query": "vintage graphic tee under $30",
                     "wardrobe": {...}}     ← wardrobe is optional
    GET  /health    is it awake?

`/ask` returns the session dict from `run_agent()` as JSON, unchanged — the
same keys you print from the command line, including `error`. Read
`session["error"]` first, exactly as you do everywhere else.

It runs **one request at a time**, and one route is deliberately slower than a
web server has to be. The reason is worth reading before you deploy: see the
note above `_one_at_a_time` below — it also decides which gunicorn worker you
can use.

CAPSTONE (unit 9): every /ask request now writes one JSON line to
logs/serve_log.jsonl — timestamp, query, status, outcome, duration, model
calls and tokens. See write_log() / log_request() below.
"""

import json
import os
import sys
import threading
import time
from datetime import datetime, timezone

# config first, and before anything that talks to the model: it loads your .env
# and fixes the Windows console encoding for every module that imports it.
import config  # noqa: F401

from flask import Flask, jsonify, request

import generate
from agent import run_agent
from utils.data_loader import get_example_wardrobe

app = Flask(__name__)


# ── CAPSTONE (unit 9): structured log ────────────────────────────────────────
# Every /ask request — good, bad, or crashed — writes ONE line of JSON to
# logs/serve_log.jsonl. One record per line, named fields, so it can be read
# back later with a script instead of squinting at print() output.
#
# Fields:
#   ts             when the request finished (UTC, ISO 8601)
#   route          which endpoint
#   status         HTTP status code we sent back
#   query          what came in (None if there was no usable query)
#   outcome        "fit_card" | "agent_error" | "bad_input" | "crash"
#   item_id        id of the listing the agent picked (None if none)
#   error          the error message, if any
#   duration_s     wall-clock seconds for the whole request
#   model_calls    real model calls this request made (cached calls = 0)
#   prompt_tokens  tokens sent, as reported by the service
#   output_tokens  tokens received, as reported by the service
#   total_tokens   prompt + output — this is the per-run cost number

LOG_PATH = config.ROOT / "logs" / "serve_log.jsonl"


def write_log(record: dict) -> None:
    """Append one record as one JSON line. Logging must never crash a request."""
    try:
        LOG_PATH.parent.mkdir(exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception as exc:  # noqa: BLE001
        print(f"  [log] could not write log: {exc}", file=sys.stderr, flush=True)


def _usage_snapshot() -> dict:
    tokens = generate.token_counts()
    return {"calls": generate.call_count(),
            "prompt": tokens["prompt"], "output": tokens["output"]}


def log_request(start: float, before: dict, status: int, query, outcome: str,
                item_id=None, error=None) -> None:
    after = _usage_snapshot()
    prompt = after["prompt"] - before["prompt"]
    output = after["output"] - before["output"]
    write_log({
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "route": "/ask",
        "status": status,
        "query": query,
        "outcome": outcome,
        "item_id": item_id,
        "error": error,
        "duration_s": round(time.perf_counter() - start, 2),
        "model_calls": after["calls"] - before["calls"],
        "prompt_tokens": prompt,
        "output_tokens": output,
        "total_tokens": prompt + output,
    })


# ── one request at a time ─────────────────────────────────────────────────────
# Here's why this exists.
#
# A web server will happily run two requests at once. Two things in this repo
# assume otherwise:
#
#   • If you moved a tool onto MCP in unit 4, `mcp_client.call_tool` starts
#     `mcp_server.py` as a separate process over stdio, one per call. Two
#     overlapping requests means two extra Python interpreters, and the free
#     tier you're deploying to has 512 MB for all of it. That is the reason
#     that would still be here even if everything else were perfect.
#   • `generate.py`'s pacing window and its call counter are plain module
#     globals — deliberately, because that file is teaching pacing and quota,
#     not locking. Two threads sharing them means the per-minute limiter is
#     counting something that isn't true.
#
# What the lock covers is exactly the agent run: the part that spawns
# processes and calls the model. Reading the request, rejecting a bad one, and
# turning the answer into JSON all happen outside it — so a request with a
# malformed body comes straight back with a 400 instead of queueing behind
# somebody else's agent.
#
# Serialising the runs costs you nothing here — this is one user asking one
# question — and it keeps the deployed behaviour identical to the CLI's. When
# that stops being an acceptable trade, the fix is a real queue, not a bigger
# lock.
#
# The same constraint decides your start command, and this is the part that
# bites in deployment rather than on your machine. `mcp_client.call_tool`
# wraps `asyncio.run()`, and `asyncio.run()` refuses to start when an event
# loop is already running. An async worker always has one running. So under
# `gunicorn -k gevent` (or `-k eventlet`, or `serve:app` wrapped for an ASGI
# server like uvicorn) EVERY MCP call fails with "asyncio.run() cannot be
# called from a running event loop" — not some of them under load, all of
# them, every time, in a place your laptop never showed you.
#
#     gunicorn serve:app              ← right: the DEFAULT sync worker
#     gunicorn -k gevent serve:app    ← breaks every MCP call you make

_one_at_a_time = threading.Lock()


@app.get("/health")
def health():
    """Is the server awake? A host pings something like this to find out."""
    return jsonify({"status": "ok"})


@app.post("/ask")
def ask():
    """
    Run the agent on one query.

    In:   {"query": "...", "wardrobe": {...}}   wardrobe optional — leave it
                                                out and you get the same
                                                example wardrobe the CLI uses.
    Out:  the session dict from run_agent(), as JSON.
    """
    start = time.perf_counter()
    before = _usage_snapshot()

    
    payload = request.get_json(silent=True) 
    
    #query = (payload.get("query") or "").strip()
    
    if not isinstance(payload, dict):
        payload = {}
    query = payload.get("query")
    query = query.strip() if isinstance(query, str) else ""

    if not query:
        # 400 rather than a stack trace: the caller can act on this one.
        message = ("Send JSON with a 'query' field, e.g. "
                   '{"query": "vintage graphic tee under $30"}')
        log_request(start, before, 400, None, "bad_input", error=message)
        return jsonify({"error": message}), 400

    wardrobe = payload.get("wardrobe")
    if not isinstance(wardrobe, dict):
        wardrobe = get_example_wardrobe()

    # A queued request should look like a queued request. Without this the
    # second caller just sits there, and "slow" and "waiting its turn" are
    # indistinguishable from the outside — which is how people conclude the
    # deployment is broken when it is behaving exactly as designed.
    #
    # This is NOT the logging you add in the follow-along. It prints nothing
    # on the normal path, carries no timing and counts nothing; it says only
    # that this request had to wait. `locked()` can be a moment out of date,
    # so the note is occasionally missed — which costs nothing, because
    # nothing depends on it.
    if _one_at_a_time.locked():
        print(
            "  [serve] another request is still running. This one is waiting "
            "its turn — serve.py handles one at a time, on purpose.",
            file=sys.stderr,
            flush=True,
        )

    failure = None
    session = None
    with _one_at_a_time:
        try:
            session = run_agent(query, wardrobe)
        except Exception as exc:  # noqa: BLE001 — a 500 with a sentence beats a hang
            failure = f"{type(exc).__name__}: {exc}"

    # Outside the lock: building a response is not work the next caller should
    # be waiting on.
    if failure is not None:
        log_request(start, before, 500, query, "crash", error=failure)
        return jsonify({"error": failure}), 500

    item = session.get("selected_item") or {}
    outcome = "agent_error" if session.get("error") else "fit_card"
    log_request(start, before, 200, query, outcome,
                item_id=item.get("id"), error=session.get("error"))
    return jsonify(session)


if __name__ == "__main__":
    # PORT and 0.0.0.0 are not decoration. A host tells you which port to
    # listen on through PORT, and it reaches your process from outside the
    # container — bind 127.0.0.1 and nothing but the container itself can
    # connect, which looks exactly like a broken app from the browser.
    port = int(os.getenv("PORT", "5000"))

    # Never on by default. Flask's debugger executes code typed into a browser,
    # and a deployed app with it on is a stranger's shell. Set AI201_DEBUG=1 in
    # your own terminal when you want the reloader.
    debug = os.getenv("AI201_DEBUG", "0") == "1"

    print(f"\nFitFindr is listening on http://localhost:{port}")
    print("It runs one request at a time — a second one waits for the first.")
    print("Ask it something (single quotes, as always):\n")
    print(
        f"  curl -X POST http://localhost:{port}/ask \\\n"
        f"    -H 'Content-Type: application/json' \\\n"
        f"    -d '{{\"query\": \"vintage graphic tee under $30\"}}'\n"
    )
    print("Ctrl-C to stop.\n")

    app.run(host="0.0.0.0", port=port, debug=debug)
