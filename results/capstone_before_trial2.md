# Capstone trial 2 — before
Run at 2026-11-12T17:54:50 against http://localhost:5000/ask
Produced by `capstone_trials.py::main`; log lines written by `serve.py::log_request`.

## Scores

| Criterion | Result |
|---|---|
| 1. Every request leaves a complete log record | 9/11 |
| 2. Bad input gets a 400 with a message | 3/5 |
| 3. Matching query answers in under 8s | 5/5 |
| 4. One run costs at most 4000 tokens | 5/5 |
| 5. Original agent still works over HTTP | 6/6 |

- successful runs: 5, median 2.43s, max 3.02s
- tokens per successful run: mean 668, min 640, max 700

## Responses

- **[200] matching — vintage graphic tee under $30** (4.3s): {"error": null, "fit_card": "Scored this sick 2003 tour bootleg graphic tee on Depop for just $24, and it's got that perfect lived-in grunge fade. I'm obsessed with styling it either super casual with baggy denim or leaning into the contrast by tucking it into wide-leg trousers. It brings instant Y2
- **[200] matching — denim jacket under $50** (4.4s): {"error": null, "fit_card": "Score this vintage Wrangler denim jacket in an effortless light wash for just $42.00 on Poshmark, and it instantly elevates my casual streetwear rotation. The cropped fit is giving the ultimate effortless '90s vibe, whether I'm throwing it over a simple tank or layering 
- **[200] matching — 90s track jacket in size M** (4.5s): {"error": null, "fit_card": "Scored this vintage 90s Champion track jacket for just $45.00 on Poshmark and it is the ultimate athletic streetwear piece for layering. I am obsessed with the navy and white stripes for capturing that effortless retro aesthetic. It looks so good thrown over a tank with 
- **[200] matching — silk slip dress in midi length under $40** (4.8s): {"error": null, "fit_card": "Found the ultimate grunge-meets-cottagecore piece with this 90s silk slip dress. At just $30.00 on Depop, it is so easy to style whether you want to toughen it up with combat boots or keep it casual under a sweatshirt. Grab it before I change my mind and keep it for myse
- **[200] matching — platform sneakers size 8** (5.1s): {"error": null, "fit_card": "Score these dreamy platform sneakers for just $48.00 on Poshmark and immediately unlocked the ultimate 90s streetwear aesthetic. They literally make every casual baggy-jean fit and Y2K sporty look ten times better without even trying. Seriously obsessed with how chunky a
- **[200] impossible — designer ballgown size XXS under $5** (2.7s): {"error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "fit_card": null}
- **[400] bad — empty JSON object** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — blank query** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — not JSON at all** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[500] bad — JSON list, not dict** (2.0s): <!doctype html> <html lang=en> <title>500 Internal Server Error</title> <h1>Internal Server Error</h1> <p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p> 
- **[500] bad — query is a number** (2.1s): <!doctype html> <html lang=en> <title>500 Internal Server Error</title> <h1>Internal Server Error</h1> <p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p> 

## New log lines (logs/serve_log.jsonl)

```
{"ts": "2026-11-12T22:54:18+00:00", "route": "/ask", "status": 200, "query": "vintage graphic tee under $30", "outcome": "fit_card", "item_id": "lst_006", "error": null, "duration_s": 2.26, "model_calls": 2, "prompt_tokens": 464, "output_tokens": 184, "total_tokens": 648}
{"ts": "2026-11-12T22:54:22+00:00", "route": "/ask", "status": 200, "query": "denim jacket under $50", "outcome": "fit_card", "item_id": "lst_007", "error": null, "duration_s": 2.32, "model_calls": 2, "prompt_tokens": 453, "output_tokens": 187, "total_tokens": 640}
{"ts": "2026-11-12T22:54:27+00:00", "route": "/ask", "status": 200, "query": "90s track jacket in size M", "outcome": "fit_card", "item_id": "lst_004", "error": null, "duration_s": 2.43, "model_calls": 2, "prompt_tokens": 480, "output_tokens": 184, "total_tokens": 664}
{"ts": "2026-11-12T22:54:31+00:00", "route": "/ask", "status": 200, "query": "silk slip dress in midi length under $40", "outcome": "fit_card", "item_id": "lst_013", "error": null, "duration_s": 2.74, "model_calls": 2, "prompt_tokens": 500, "output_tokens": 200, "total_tokens": 700}
{"ts": "2026-11-12T22:54:36+00:00", "route": "/ask", "status": 200, "query": "platform sneakers size 8", "outcome": "fit_card", "item_id": "lst_019", "error": null, "duration_s": 3.02, "model_calls": 2, "prompt_tokens": 486, "output_tokens": 200, "total_tokens": 686}
{"ts": "2026-11-12T22:54:39+00:00", "route": "/ask", "status": 200, "query": "designer ballgown size XXS under $5", "outcome": "agent_error", "item_id": null, "error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "duration_s": 0.71, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-12T22:54:41+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-12T22:54:43+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-12T22:54:45+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
```
