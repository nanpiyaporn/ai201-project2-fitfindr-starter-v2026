# Capstone trial 1 — after
Run at 2026-11-12T19:07:33 against http://localhost:5000/ask
Produced by `capstone_trials.py::main`; log lines written by `serve.py::log_request`.

## Scores

| Criterion | Result |
|---|---|
| 1. Every request leaves a complete log record | 11/11 |
| 2. Bad input gets a 400 with a message | 5/5 |
| 3. Matching query answers in under 8s | 5/5 |
| 4. One run costs at most 4000 tokens | 0/5 |
| 5. Original agent still works over HTTP | 6/6 |

- successful runs: 5, median 0.72s, max 1.14s
- tokens per successful run: mean 0, min 0, max 0

## Responses

- **[200] matching — vintage graphic tee under $30** (3.2s): {"error": null, "fit_card": "Finally found the ultimate 2003 tour bootleg style graphic tee to complete my grunge streetwear rotation, and I scored it on Depop for just $24.00. The vintage fade on this black top is so good, and it looks insanely cool layered under an unzipped hoodie or tucked into w
- **[200] matching — denim jacket under $50** (2.8s): {"error": null, "fit_card": "Score this vintage Wrangler denim jacket for just $42.00 on Poshmark and instantly level up your off-duty streetwear rotation. It’s got that perfect light wash and cropped fit for building high-contrast casual looks or leaning into some easy streetwear prep. Run, don't w
- **[200] matching — 90s track jacket in size M** (2.8s): {"error": null, "fit_card": "scored this vintage 90s navy and white champion track jacket for just $45 over on Poshmark, and it is the ultimate athletic streetwear piece for layering. i put together two easy ways to style it, leaning into that effortless retro vibe with baggy denim and chunky sneake
- **[200] matching — silk slip dress in midi length under $40** (2.8s): {"error": null, "fit_card": "Found the absolute dreamiest 90s silk slip dress on Depop for just $30, and I am obsessed with the grunge-meets-cottagecore floral print. I'm already planning to toughen it up with combat boots and an oversized sweatshirt, but it's going to look equally good layered over
- **[200] matching — platform sneakers size 8** (2.8s): {"error": null, "fit_card": "Found these chunky white platform sneakers on Poshmark for just $48, and they are the ultimate 90s streetwear staple for bringing all the nostalgic attitude to any outfit. I am obsessed with how the chunky sole anchors a relaxed denim look while still feeling completely 
- **[200] impossible — designer ballgown size XXS under $5** (2.8s): {"error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "fit_card": null}
- **[400] bad — empty JSON object** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — blank query** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — not JSON at all** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — JSON list, not dict** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — query is a number** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}

## New log lines (logs/serve_log.jsonl)

```
{"ts": "2026-11-13T00:07:09+00:00", "route": "/ask", "status": 200, "query": "vintage graphic tee under $30", "outcome": "fit_card", "item_id": "lst_006", "error": null, "duration_s": 1.14, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:07:11+00:00", "route": "/ask", "status": 200, "query": "denim jacket under $50", "outcome": "fit_card", "item_id": "lst_007", "error": null, "duration_s": 0.71, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:07:14+00:00", "route": "/ask", "status": 200, "query": "90s track jacket in size M", "outcome": "fit_card", "item_id": "lst_004", "error": null, "duration_s": 0.72, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:07:17+00:00", "route": "/ask", "status": 200, "query": "silk slip dress in midi length under $40", "outcome": "fit_card", "item_id": "lst_013", "error": null, "duration_s": 0.71, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:07:20+00:00", "route": "/ask", "status": 200, "query": "platform sneakers size 8", "outcome": "fit_card", "item_id": "lst_019", "error": null, "duration_s": 0.72, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:07:23+00:00", "route": "/ask", "status": 200, "query": "designer ballgown size XXS under $5", "outcome": "agent_error", "item_id": null, "error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "duration_s": 0.75, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:07:25+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:07:27+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:07:29+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:07:31+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:07:33+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
```
