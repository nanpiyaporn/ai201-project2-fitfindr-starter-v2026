# Capstone trial 2 — after
Run at 2026-11-12T19:15:22 against http://localhost:5000/ask
Produced by `capstone_trials.py::main`; log lines written by `serve.py::log_request`.

## Scores

| Criterion | Result |
|---|---|
| 1. Every request leaves a complete log record | 11/11 |
| 2. Bad input gets a 400 with a message | 5/5 |
| 3. Matching query answers in under 8s | 4/5 |
| 4. One run costs at most 4000 tokens | 5/5 |
| 5. Original agent still works over HTTP | 6/6 |

- successful runs: 5, median 2.48s, max 16.23s
- tokens per successful run: mean 686, min 618, max 730

## Responses

- **[200] matching — vintage graphic tee under $30** (4.5s): {"error": null, "fit_card": "Found this vintage-look 2003 tour bootleg graphic tee and I am so obsessed with the grunge streetwear vibe. I'm styling it two ways—either layered with a black denim jacket and chunky sneakers or dressed down with khaki trousers and combat boots. Snagged it on Depop for 
- **[200] matching — denim jacket under $50** (4.6s): {"error": null, "fit_card": "Score this vintage Wrangler denim jacket for just $42.00 on Poshmark and immediately built two fresh streetwear looks around it. The light wash and cropped fit make it super easy to layer over everything from baggy jeans to chunky sweaters for that effortless, textured v
- **[200] matching — 90s track jacket in size M** (18.3s): {"error": null, "fit_card": "Nothing beats finding a classic 90s athletic piece like this navy and white Champion track jacket to nail that effortless streetwear vibe. I am obsessed with how easily this vintage find styles up, whether you're throwing it over baggy denim or high-waisted trousers. Gra
- **[200] matching — silk slip dress in midi length under $40** (8.5s): {"error": null, "fit_card": "Channeling total 90s romance with this floral silk slip dress, and I'm obsessed with how versatile it is. You can style it grunge-style over baggy denim or keep it cozy under an oversized crewneck for effortless street style. Grab this vintage find for just $30.00 in my 
- **[200] matching — platform sneakers size 8** (4.5s): {"error": null, "fit_card": "Score these chunky white platform sneakers on Poshmark for just $48 and instantly level up your Y2K streetwear rotation. I am so obsessed with how easily these give that effortless 90s edge whether you're styling them with baggy denim or relaxed khaki trousers. Absolute 
- **[200] impossible — designer ballgown size XXS under $5** (2.8s): {"error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "fit_card": null}
- **[400] bad — empty JSON object** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — blank query** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — not JSON at all** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — JSON list, not dict** (2.1s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}
- **[400] bad — query is a number** (2.0s): {"error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}"}

## New log lines (logs/serve_log.jsonl)

```
{"ts": "2026-11-13T00:14:33+00:00", "route": "/ask", "status": 200, "query": "vintage graphic tee under $30", "outcome": "fit_card", "item_id": "lst_006", "error": null, "duration_s": 2.43, "model_calls": 2, "prompt_tokens": 476, "output_tokens": 201, "total_tokens": 677}
{"ts": "2026-11-13T00:14:37+00:00", "route": "/ask", "status": 200, "query": "denim jacket under $50", "outcome": "fit_card", "item_id": "lst_007", "error": null, "duration_s": 2.48, "model_calls": 2, "prompt_tokens": 504, "output_tokens": 226, "total_tokens": 730}
{"ts": "2026-11-13T00:14:55+00:00", "route": "/ask", "status": 200, "query": "90s track jacket in size M", "outcome": "fit_card", "item_id": "lst_004", "error": null, "duration_s": 16.23, "model_calls": 2, "prompt_tokens": 480, "output_tokens": 194, "total_tokens": 674}
{"ts": "2026-11-13T00:15:04+00:00", "route": "/ask", "status": 200, "query": "silk slip dress in midi length under $40", "outcome": "fit_card", "item_id": "lst_013", "error": null, "duration_s": 6.37, "model_calls": 2, "prompt_tokens": 514, "output_tokens": 216, "total_tokens": 730}
{"ts": "2026-11-13T00:15:08+00:00", "route": "/ask", "status": 200, "query": "platform sneakers size 8", "outcome": "fit_card", "item_id": "lst_019", "error": null, "duration_s": 2.48, "model_calls": 2, "prompt_tokens": 451, "output_tokens": 167, "total_tokens": 618}
{"ts": "2026-11-13T00:15:11+00:00", "route": "/ask", "status": 200, "query": "designer ballgown size XXS under $5", "outcome": "agent_error", "item_id": null, "error": "Nothing matched \"designer ballgown\" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).", "duration_s": 0.72, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:15:13+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:15:15+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:15:17+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:15:19+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
{"ts": "2026-11-13T00:15:21+00:00", "route": "/ask", "status": 400, "query": null, "outcome": "bad_input", "item_id": null, "error": "Send JSON with a 'query' field, e.g. {\"query\": \"vintage graphic tee under $30\"}", "duration_s": 0.0, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "total_tokens": 0}
```
