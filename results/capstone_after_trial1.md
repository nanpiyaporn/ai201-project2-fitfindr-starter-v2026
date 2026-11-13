# Capstone trial 1 — after
Run at 2026-11-12T19:14:28 against http://localhost:5000/ask
Produced by `capstone_trials.py::main`; log lines written by `serve.py::log_request`.

## Scores

| Criterion | Result |
|---|---|
| 1. Every request leaves a complete log record | 11/11 |
| 2. Bad input gets a 400 with a message | 5/5 |
| 3. Matching query answers in under 8s | 5/5 |
| 4. One run costs at most 4000 tokens | 5/5 |
| 5. Original agent still works over HTTP | 6/6 |

- successful runs: 5, median 2.60s, max 4.35s
- tokens per successful run: mean 687, min 634, max 756

## Responses

- **[200] matching — vintage graphic tee under $30** (6.4s): {"error": null, "fit_card": "Found this 2003 tour bootleg style graphic tee on Depop and I am obsessed with the worn-in grunge vibe. At just $24.00, it's the ultimate piece for throwing together effortless streetwear looks or dressing up with tailored trousers. Trust me, you need a good vintage band
- **[200] matching — denim jacket under $50** (4.7s): {"error": null, "fit_card": "Just scored this vintage Wrangler cropped denim jacket on Poshmark for $42 and I am already obsessed with the light wash. It has that ultimate effortless streetwear vibe, especially thrown over baggy dark denim or wide-leg khakis. Honestly, finding classic outerwear like
- **[200] matching — 90s track jacket in size M** (4.6s): {"error": null, "fit_card": "Score this vintage 90s Champion track jacket for just $45.00 on Poshmark and you’ve got the ultimate streetwear piece. It’s giving major retro athletic energy, whether you're dressing it down with baggy denim or leaning into that high-low prep vibe with khaki trousers. G
- **[200] matching — silk slip dress in midi length under $40** (4.6s): {"error": null, "fit_card": "Obsessed with this 90s floral silk slip dress—it's giving the ultimate retro grunge and cottagecore crossover. I styled it two ways, from throwing it over baggy denim with combat boots to wearing it as a skirt under an oversized crewneck. Snagged this beauty for just $30
- **[200] matching — platform sneakers size 8** (4.7s): {"error": null, "fit_card": "Scored these chunky white platform sneakers on Poshmark for just $48, and they instantly unlocked the ultimate 90s streetwear vibe for my wardrobe. I am so obsessed with how easily they anchor a casual outfit, whether I am pairing them with baggy denim or relaxed khaki t
- **[200] impossible — designer ballgown size XXS under $5** (2.8s): {"error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "fit_card": null}
- **[400] bad — empty JSON object** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — blank query** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — not JSON at all** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — JSON list, not dict** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — query is a number** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}

## New log lines (logs/serve_log.jsonl)

```
{"ts": "2026-11-13T00:13:56+00:00", "route": "/ask", "status": 200, "query": "vintage graphic tee under $30", "outcome": "fit_card", "item_id": "lst_006", "error": null, "duration_s": 4.35, "model_calls": 2, "prompt_tokens": 487, "output_tokens": 208, "total_tokens": 695}
{"ts": "2026-11-13T00:14:01+00:00", "route": "/ask", "status": 200, "query": "denim jacket under $50", "outcome": "fit_card", "item_id": "lst_007", "error": null, "duration_s": 2.6, "model_calls": 2, "prompt_tokens": 497, "output_tokens": 213, "total_tokens": 710}
{"ts": "2026-11-13T00:14:05+00:00", "route": "/ask", "status": 200, "query": "90s track jacket in size M", "outcome": "fit_card", "item_id": "lst_004", "error": null, "duration_s": 2.56, "model_calls": 2, "prompt_tokens": 461, "output_tokens": 173, "total_tokens": 634}
{"ts": "2026-11-13T00:14:10+00:00", "route": "/ask", "status": 200, "query": "silk slip dress in midi length under $40", "outcome": "fit_card", "item_id": "lst_013", "error": null, "duration_s": 2.54, "model_calls": 2, "prompt_tokens": 522, "output_tokens": 234, "total_tokens": 756}
{"ts": "2026-11-13T00:14:14+00:00", "route": "/ask", "status": 200, "query": "platform sneakers size 8", "outcome": "fit_card", "item_id": "lst_019", "error": null, "duration_s": 2.63, "model_calls": 2, "prompt_tokens": 463, "output_tokens": 178, "total_tokens": 641}
{"ts": "2026-11-13T00:14:17+00:00", "route": "/ask", "status": 200, "query": "designer ballgown size XXS under $5", "outcome": "agent_error", "item_id": null, "error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "duration_s": 0.73, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:14:19+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:14:21+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:14:23+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:14:25+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:14:27+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
```
