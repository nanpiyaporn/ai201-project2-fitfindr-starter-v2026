# Capstone trial 3 — before
Run at 2026-11-12T17:59:13 against http://localhost:5000/ask
Produced by `capstone_trials.py::main`; log lines written by `serve.py::log_request`.

## Scores

| Criterion | Result |
|---|---|
| 1. Every request leaves a complete log record | 9/11 |
| 2. Bad input gets a 400 with a message | 3/5 |
| 3. Matching query answers in under 8s | 5/5 |
| 4. One run costs at most 4000 tokens | 5/5 |
| 5. Original agent still works over HTTP | 6/6 |

- successful runs: 5, median 2.73s, max 3.60s
- tokens per successful run: mean 721, min 639, max 793

## Responses

- **[200] matching — vintage graphic tee under $30** (4.8s): {"error": null, "fit_card": "Just scored this 2003 tour bootleg style graphic tee on Depop for $24 and I'm obsessed with the worn-in grunge vibe. It's the ultimate piece for throwing together an effortless streetwear look with baggy jeans or dressing up with tailored trousers. You already know this 
- **[200] matching — denim jacket under $50** (4.9s): {"error": null, "fit_card": "Score this incredible cropped Wrangler denim jacket for just $42.00 on Poshmark and instantly level up your streetwear rotation. The vintage light wash looks so good styled against baggy dark denim or relaxed khaki trousers for that ultimate high-contrast casual vibe. It
- **[200] matching — 90s track jacket in size M** (4.5s): {"error": null, "fit_card": "Scored this vintage 90s Champion track jacket in the best navy and white stripe combo, and it's giving me all the nostalgic streetwear energy. I'm totally planning to style it over a ribbed tank with baggy denim or wide-leg khakis for that effortless athletic look. Grabb
- **[200] matching — silk slip dress in midi length under $40** (5.6s): {"error": null, "fit_card": "Finally scored the 90s Silk Slip Dress of my dreams on Depop for just $30, and I am so obsessed with how dreamy the floral print is. I'm planning to lean into that ultimate 90s model-off-duty energy by layering it over baggy denim with chunky sneakers, or grunge it up a 
- **[200] matching — platform sneakers size 8** (4.7s): {"error": null, "fit_card": "Found these white chunky sole platform sneakers on Poshmark for just $48, and they are the ultimate 90s streetwear staple. They instantly elevate my casual outfits, whether I'm leaning into baggy denim or making wide-leg trousers look effortlessly cool. Such a good thrif
- **[200] impossible — designer ballgown size XXS under $5** (2.8s): {"error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "fit_card": null}
- **[400] bad — empty JSON object** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — blank query** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — not JSON at all** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[500] bad — JSON list, not dict** (2.1s): <!doctype html> <html lang=en> <title>500 Internal Server Error</title> <h1>Internal Server Error</h1> <p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p> 
- **[500] bad — query is a number** (2.0s): <!doctype html> <html lang=en> <title>500 Internal Server Error</title> <h1>Internal Server Error</h1> <p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p> 

## New log lines (logs/serve_log.jsonl)

```
{"ts": "2026-11-12T22:58:40+00:00", "route": "/ask", "status": 200, "query": "vintage graphic tee under $30", "outcome": "fit_card", "item_id": "lst_006", "error": null, "duration_s": 2.73, "model_calls": 2, "prompt_tokens": 462, "output_tokens": 177, "total_tokens": 639}
{"ts": "2026-11-12T22:58:45+00:00", "route": "/ask", "status": 200, "query": "denim jacket under $50", "outcome": "fit_card", "item_id": "lst_007", "error": null, "duration_s": 2.87, "model_calls": 2, "prompt_tokens": 516, "output_tokens": 235, "total_tokens": 751}
{"ts": "2026-11-12T22:58:49+00:00", "route": "/ask", "status": 200, "query": "90s track jacket in size M", "outcome": "fit_card", "item_id": "lst_004", "error": null, "duration_s": 2.47, "model_calls": 2, "prompt_tokens": 477, "output_tokens": 194, "total_tokens": 671}
{"ts": "2026-11-12T22:58:55+00:00", "route": "/ask", "status": 200, "query": "silk slip dress in midi length under $40", "outcome": "fit_card", "item_id": "lst_013", "error": null, "duration_s": 3.6, "model_calls": 2, "prompt_tokens": 530, "output_tokens": 263, "total_tokens": 793}
{"ts": "2026-11-12T22:58:59+00:00", "route": "/ask", "status": 200, "query": "platform sneakers size 8", "outcome": "fit_card", "item_id": "lst_019", "error": null, "duration_s": 2.63, "model_calls": 2, "prompt_tokens": 516, "output_tokens": 234, "total_tokens": 750}
{"ts": "2026-11-12T22:59:02+00:00", "route": "/ask", "status": 200, "query": "designer ballgown size XXS under $5", "outcome": "agent_error", "item_id": null, "error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "duration_s": 0.74, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-12T22:59:04+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-12T22:59:06+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-12T22:59:08+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
```
