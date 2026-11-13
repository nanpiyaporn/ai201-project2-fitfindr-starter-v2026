# Capstone trial 3 — after
Run at 2026-11-12T19:16:15 against http://localhost:5000/ask
Produced by `capstone_trials.py::main`; log lines written by `serve.py::log_request`.

## Scores

| Criterion | Result |
|---|---|
| 1. Every request leaves a complete log record | 11/11 |
| 2. Bad input gets a 400 with a message | 5/5 |
| 3. Matching query answers in under 8s | 4/5 |
| 4. One run costs at most 4000 tokens | 5/5 |
| 5. Original agent still works over HTTP | 6/6 |

- successful runs: 5, median 2.72s, max 18.78s
- tokens per successful run: mean 661, min 620, max 700

## Responses

- **[200] matching — vintage graphic tee under $30** (4.3s): {"error": null, "fit_card": "Scored this vintage-style 2003 tour graphic tee for just $24 on Depop and it is the ultimate piece for nailing that effortless, grungy streetwear look. I'm obsessed with how easily it goes with everything from baggy denim to khaki trousers. Go grab it before I change my 
- **[200] matching — denim jacket under $50** (4.6s): {"error": null, "fit_card": "Score this vintage Wrangler denim jacket for just $42 on Poshmark and my wardrobe is officially complete. I am obsessed with the light wash and cropped fit for throwing over baggy jeans or slouchy trousers. It is the ultimate effortless streetwear layering piece I have b
- **[200] matching — 90s track jacket in size M** (4.8s): {"error": null, "fit_card": "Scored the ultimate 90s athletic vibe with this navy and white Champion track jacket, and I am obsessed. It's in amazing condition and only cost me $45.00 over on Poshmark. Can't wait to style it for everything from baggy denim days to dressed-up khaki trousers."}
- **[200] matching — silk slip dress in midi length under $40** (5.1s): {"error": null, "fit_card": "Found the ultimate 90s floral silk slip dress for just $30.00 and I am already obsessed with how dreamy and versatile it is. I'm selling it over on my Depop so you can channel your inner 90s indie sleaze or soft grunge aesthetic all season long. Trust me, pieces this goo
- **[200] matching — platform sneakers size 8** (20.8s): {"error": null, "fit_card": "Finally snagged these chunky white platform sneakers on Poshmark for just $48, and they are the ultimate Y2K throwback for completing any streetwear look. I’m obsessed with how they instantly elevate an effortless baggy denim fit while keeping that authentic 90s edge. Th
- **[200] impossible — designer ballgown size XXS under $5** (2.8s): {"error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "fit_card": null}
- **[400] bad — empty JSON object** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — blank query** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — not JSON at all** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — JSON list, not dict** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — query is a number** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}

## New log lines (logs/serve_log.jsonl)

```
{"ts": "2026-11-13T00:15:26+00:00", "route": "/ask", "status": 200, "query": "vintage graphic tee under $30", "outcome": "fit_card", "item_id": "lst_006", "error": null, "duration_s": 2.24, "model_calls": 2, "prompt_tokens": 454, "output_tokens": 166, "total_tokens": 620}
{"ts": "2026-11-13T00:15:31+00:00", "route": "/ask", "status": 200, "query": "denim jacket under $50", "outcome": "fit_card", "item_id": "lst_007", "error": null, "duration_s": 2.57, "model_calls": 2, "prompt_tokens": 465, "output_tokens": 170, "total_tokens": 635}
{"ts": "2026-11-13T00:15:36+00:00", "route": "/ask", "status": 200, "query": "90s track jacket in size M", "outcome": "fit_card", "item_id": "lst_004", "error": null, "duration_s": 2.72, "model_calls": 2, "prompt_tokens": 481, "output_tokens": 182, "total_tokens": 663}
{"ts": "2026-11-13T00:15:41+00:00", "route": "/ask", "status": 200, "query": "silk slip dress in midi length under $40", "outcome": "fit_card", "item_id": "lst_013", "error": null, "duration_s": 3.09, "model_calls": 2, "prompt_tokens": 489, "output_tokens": 200, "total_tokens": 689}
{"ts": "2026-11-13T00:16:02+00:00", "route": "/ask", "status": 200, "query": "platform sneakers size 8", "outcome": "fit_card", "item_id": "lst_019", "error": null, "duration_s": 18.78, "model_calls": 3, "prompt_tokens": 491, "output_tokens": 209, "total_tokens": 700}
{"ts": "2026-11-13T00:16:04+00:00", "route": "/ask", "status": 200, "query": "designer ballgown size XXS under $5", "outcome": "agent_error", "item_id": null, "error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "duration_s": 0.72, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:16:07+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:16:09+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:16:11+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:16:13+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:16:15+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
```
