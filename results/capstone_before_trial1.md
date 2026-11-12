# Capstone trial 1 — before
Run at 2026-11-12T17:45:36 against http://localhost:5000/ask
Produced by `capstone_trials.py::main`; log lines written by `serve.py::log_request`.

## Scores

| Criterion | Result |
|---|---|
| 1. Every request leaves a complete log record | 9/11 |
| 2. Bad input gets a 400 with a message | 3/5 |
| 3. Matching query answers in under 8s | 5/5 |
| 4. One run costs at most 4000 tokens | 5/5 |
| 5. Original agent still works over HTTP | 6/6 |

- successful runs: 5, median 2.63s, max 5.59s
- tokens per successful run: mean 714, min 655, max 847

## Responses

- **[200] matching — vintage graphic tee under $30** (7.6s): {"error": null, "fit_card": "Just scored this 2003 tour bootleg style graphic tee on Depop and I am so obsessed with the grunge energy. It has that perfectly worn-in look and was only $24.00, making it the ultimate piece for building effortless streetwear fits. I can't wait to style it with baggy de
- **[200] matching — denim jacket under $50** (4.7s): {"error": null, "fit_card": "Just scored this vintage Wrangler cropped denim jacket on Poshmark for $42 and I am already obsessed with the light wash. It’s got that perfect effortless streetwear vibe, whether I'm leaning into a high-contrast double-denim look or layering it over an oversized crewnec
- **[200] matching — 90s track jacket in size M** (4.5s): {"error": null, "fit_card": "Score this vintage 90s Champion track jacket for just $45.00 and you've got the ultimate streetwear staple for effortless athletic styling. I just listed it over on Poshmark, and it’s in amazing condition ready to elevate your retro wardrobe."}
- **[200] matching — silk slip dress in midi length under $40** (5.0s): {"error": null, "fit_card": "Channeling peak 90s romance with this floral silk slip dress, but I'm obsessed with styling it down with grunge denim and a slouchy crewneck. Snagged this dreamy vintage piece for just $30.00, and it's up in my Depop shop right now."}
- **[200] matching — platform sneakers size 8** (4.4s): {"error": null, "fit_card": "Score these white chunky sole platform sneakers on Poshmark for just $48 and instantly level up your off-duty streetwear game. Whether you're channeling effortless 90s minimalism or going full Y2K with baggy denim, this pair adds the ultimate throwback edge to any fit. T
- **[200] impossible — designer ballgown size XXS under $5** (2.8s): {"error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "fit_card": null}
- **[400] bad — empty JSON object** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — blank query** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — not JSON at all** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[500] bad — JSON list, not dict** (2.1s): <!doctype html> <html lang=en> <title>500 Internal Server Error</title> <h1>Internal Server Error</h1> <p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p> 
- **[500] bad — query is a number** (2.1s): <!doctype html> <html lang=en> <title>500 Internal Server Error</title> <h1>Internal Server Error</h1> <p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p> 

## New log lines (logs/serve_log.jsonl)

```
{"ts": "2026-11-12T22:45:04+00:00", "route": "/ask", "status": 200, "query": "vintage graphic tee under $30", "outcome": "fit_card", "item_id": "lst_006", "error": null, "duration_s": 5.59, "model_calls": 2, "prompt_tokens": 468, "output_tokens": 198, "total_tokens": 666}
{"ts": "2026-11-12T22:45:09+00:00", "route": "/ask", "status": 200, "query": "denim jacket under $50", "outcome": "fit_card", "item_id": "lst_007", "error": null, "duration_s": 2.63, "model_calls": 2, "prompt_tokens": 563, "output_tokens": 284, "total_tokens": 847}
{"ts": "2026-11-12T22:45:14+00:00", "route": "/ask", "status": 200, "query": "90s track jacket in size M", "outcome": "fit_card", "item_id": "lst_004", "error": null, "duration_s": 2.43, "model_calls": 2, "prompt_tokens": 482, "output_tokens": 173, "total_tokens": 655}
{"ts": "2026-11-12T22:45:18+00:00", "route": "/ask", "status": 200, "query": "silk slip dress in midi length under $40", "outcome": "fit_card", "item_id": "lst_013", "error": null, "duration_s": 2.9, "model_calls": 2, "prompt_tokens": 504, "output_tokens": 196, "total_tokens": 700}
{"ts": "2026-11-12T22:45:23+00:00", "route": "/ask", "status": 200, "query": "platform sneakers size 8", "outcome": "fit_card", "item_id": "lst_019", "error": null, "duration_s": 2.35, "model_calls": 2, "prompt_tokens": 488, "output_tokens": 212, "total_tokens": 700}
{"ts": "2026-11-12T22:45:26+00:00", "route": "/ask", "status": 200, "query": "designer ballgown size XXS under $5", "outcome": "agent_error", "item_id": null, "error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "duration_s": 0.74, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-12T22:45:28+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-12T22:45:30+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-12T22:45:32+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
```
