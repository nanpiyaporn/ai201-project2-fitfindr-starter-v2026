# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
FitFindr helps a thrift shopper find a secondhand item and figure out how to wear it. The user types a request in plain language, like `vintage graphic tee under $30, size M`. FitFindr searches 40 listings (jackets, dresses, sneakers and more) for the best match within that size and budget. It then suggests one or two outfits that pair the item with pieces from the user's wardrobe and writes a short, social-post-style "fit card" caption about the find. If nothing matches, it stops and tells the user what to change, such as raising the budget or trying a different size.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the 40 listings in data/listings.json. Filters by max price and size when they are giving
- **Inputs:** 'description' (str), keywords such as "vintage graphic tee"; 'size' (str or None), None skips the size filter; 'max_price' (float or None), inclusive, None skips the price filter. A size matches only as a whole token: "M" matches "S/M" and "M/L", but "L" does not match "XL" and "S" does not match "US 9". One-size listings match any size.
- **Returns:** A list of up to 10 listing dicts (config.SEARCH_RESULT_LIMIT) best match first.
- **When it has nothing:** Return an empty list. not None and not an exception. The loop checks for this stops.

### `suggest_outfit`

- **What it does:** Asks for the model, via generate(), for one or two outfits built around the new item, using pieces from the user's wardrobe
- **Inputs:** 'new_item'(dict), one listing dict from search_listings; 'wardrobe'(dict) with an 'items' key holding a list of wardrobe item.
- **Returns:** A non-empty string with one or two outfit suggestions that name specific wardrobe pieces to pair with the item.
- **When it has nothing:** If 'wardrobe["items"]'is empty, it asks the model for general styling advice for the item instead, so it still return a non empty data

### `create_fit_card`

- **What it does:** Asks the model to write a short, social-post-style caption about the find, using the item details and the outfit suggestion.
- **Inputs:** 'outfit'(str), the string from suggest_outfit; 'new_item'(dict), the listing dict.
- **Returns:** A caption (str) 2-4 sentences. It mentions the item's title, price and platform once each, describes the vibe ( No show brand if it None )
- **When it has nothing:**
If 'outfit' is empty or only whitespace, it skips the model and return
--- a message like "No outfit suggestion available. Can't write a fit for this item

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, put a message in `session["error"]` that says what the user could change (raise the budget to the cheapest match, try a size that's in stock, or use different words) and stop without calling `suggest_outfit` or `create_fit_card`. Otherwise, take the first result as `session["selected_item"]` and go on to `suggest_outfit`, then `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex, in `agent.py::parse_query`. It pulls out a max price ("under $30", "below 30", "$30 or less"), then a size ("size M", "size US 8.5", "small/medium/large"). Whatever text is left becomes the description.

**What moves through the session:** `query` → `parsed` (description, size, max_price) → `search_results` → `selected_item` (the first result) → `outfit_suggestion` → `fit_card`. On the empty-search path, the run stops after `search_results` with `error` set, and `selected_item`, `outfit_suggestion` and `fit_card` stay `None`.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'
  Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   **Outfit 1: Casual Grunge Streetwear**
Pair the graphic tee with the baggy straight-leg jeans and the brown leather belt. Layer the black cropped zip hoodie on top (wear it unzipped to show off the graphic). Finish with the chunky white sneakers and the black crossbody bag. 

**Outfit 2: Contrast Neutral Mix**
Tuck the graphic tee into the wide-leg khaki trousers, secured with the brown leather belt. Throw the vintage black denim jacket over your shoulders and ground the look with the black combat boots. Accessorize with the black crossbody bag for an effortless, balanced fit.

  Fit card: Finally found the ultimate 2003 tour bootleg style graphic tee to complete my grunge streetwear rotation, and I scored it on Depop for just $24.00. The vintage fade on this black top is so good, and it looks insanely cool layered under an unzipped hoodie or tucked into wide-leg trousers. It has that authentic thrifted band merch energy that makes every outfit instantly cooler.

0 model calls this session, 2 served from cache
```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'threadUp'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
**Outfit 1: Casual Streetwear**
Pair the vintage Levi's 501 Jeans with the white ribbed tank top and the vintage black denim jacket. Cinch the waist with the brown leather belt and finish with the chunky white sneakers and black crossbody bag.

**Outfit 2: Off-Duty Comfort**
Style the vintage Levi's 501 Jeans with the oversized grey crewneck sweatshirt layered over top. Accessorize with the brown leather belt and ground the look with the black combat boots and black crossbody bag.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Nothing beats the effortless, lived-in vibe of a classic straight-leg denim look with crisp white sneakers. I just scored these vintage Levi's 501 jeans in a timeless medium wash over on depop for a total steal at $38. They've got that perfect broken-in feel and look so good dressed down for running errands or casual coffee runs.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*  I asked Claude by using a short question
- *What came back:* Nothing came back, AI needs a clear question ans a clear content
- *What I changed:* I asked Claude using a longer content

**Moment 2**

- *What I asked for:* I asked Claude with a longe content with others questions that relate to the topics.
- *What came back:* It came back better content
- *What I changed:* I will asking them the right questions with the right content

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Item search picked is the item every later tool received | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card names the facts and doesn't repeat itself | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search never returns anything over the price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Source: `results/run_2026-10-11_1428_before.md` — 5 tries per scenario, cache
off, temperature 0.9.

- **Row 3** is scored on the listing line the trace prints (title, price,
  platform), which was identical at `select_item`, `suggest_outfit` and
  `create_fit_card` in all five tries. The trace does not print the `id`.
- **Row 4** used the Graphic Tee — 2003 Tour Bootleg Style, so the price
  checked was `24` / `24.00`, not `18`.
- **Row 5**'s five tries are five different queries from this run, each
  returning the same results on all five of its repeats:

| Try | Query | `max_price` parsed | Results | Highest price returned |
|---|---|---|---|---|
| 1 | `graphic tee under $30` | 30.0 | 7 | $27 |
| 2 | `jeans $25 or less` | 25.0 | 0 | — (stopped early) |
| 3 | `jacket max 40` | 40.0 | 1 | $33 |
| 4 | `denim jacket under $50` | 50.0 | 7 | $45 |
| 5 | `vintage graphic tee under $30` | 30.0 | 10 | $27 |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

Produced by `run_eval.py::main`, running the loop in `agent.py::run_agent`
with the tools in `tools.py`. Copied from
`results/run_2026-10-11_1033_before.md`, scenario "empty wardrobe", try 1.

- Query: `denim jacket under $50`
- Wardrobe: empty

**Try 1**

- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:

```
At $42 for a vintage Wrangler piece in excellent condition, buy it. A light wash, cropped denim jacket is extremely versatile. 

**Outfit 1: Casual Streetwear**
Pair the jacket with *black high-waisted wide-leg trousers*, a *ribbed white crop top*, and *retro sneakers* like Nike Dunks or Adidas Sambas. Add a *crossbody nylon bag* to finish the look.

**Outfit 2: Off-Duty Contrast**
Throw it over a *black ribbed cotton midi dress*. Ground the outfit with *chunkier black leather boots* (like Dr. Martens) and a *minimalist leather shoulder bag* to balance the casual vintage vibe with a sharper silhouette.
```

Fit card:

```
Just scored this vintage cropped Wrangler denim jacket on Poshmark for $42 and I am obsessed with the light wash. It has that effortless streetwear vibe that instantly pulls together a simple white tee and wide-leg trousers. Honestly, it’s about to become my most-worn transitional piece this season.
```

Trace:

```
[1] parse_query
      in:  denim jacket under $50
      out: {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
[2] search_listings (via MCP)
      in:  {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
      out: 7 items: Denim Jacket — Light Wash, Cropped, 90s Track Jacket — Navy/White Stripe, High-Waisted Denim Shorts — Cutoff … +4 more
      →    branch: got results, going on to select
[3] select_item
      out: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      →    took the first (best-scoring) result
[4] suggest_outfit
      in:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      out: At $42 for a vintage Wrangler piece in excellent condition, buy it. A light wash, cropped denim jacket is extr…
[5] create_fit_card
      in:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
      out: Just scored this vintage cropped Wrangler denim jacket on Poshmark for $42 and I am obsessed with the light wa…
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools | 4 of 5 | MET (5/5) | All five tries of `vintage graphic tee under $30` reached step `[5] create_fit_card` and printed `completed — fit card N chars` (370, 315, 282, 396, 336). |
| 2 | Impossible query stops before the second tool | 5 of 5 | MET (5/5) | All five tries of `designer ballgown size XXS under $5` ended at step `[2]` with `branch: empty, stopping before suggest_outfit`, and the message named what to change ("try naming the kind of item… or a style"). |
| 3 | Item search picked is the item every later tool received | 5 of 5 | MET (5/5) | In all five tries the trace shows `Denim Jacket — Light Wash, Cropped ($42.0, poshmark)` as the `select_item` output and as the input to both `suggest_outfit` and `create_fit_card`, and it is the first title in the search results. Scored on title, price and platform, because the trace doesn't print the `id`. |
| 4 | Fit card names the facts and doesn't repeat itself | 4 of 5 | MET (5/5) | I read the five cards for the Graphic Tee. Each one names `$24` or `$24.00` and Depop and is three sentences long. No two share a first sentence, and none contains `None`. |
| 5 | Search never returns anything over the price ceiling | 5 of 5 | MET (5/5) | For five priced queries in three phrasings ("under $30", "$25 or less", "max 40"), `max_price` in the `parse_query` output was the number typed, and the highest price returned was under it each time ($27, none, $33, $45, $27). |

**Diagnoses**

No criterion missed its target on this run, so there is no failure to place in
a tool, the branch, the session or the model's output. Two of the criteria
could not be measured exactly as I wrote them, though:

- **Criterion 3 — the trace can't show what the criterion asks for.** I wrote
  it as comparing `session["selected_item"]["id"]` against the `id` each later
  tool received, but the trace prints title, price and platform, not `id`. The
  session itself is fine; the gap is in what the trace records. Two listings
  with the same title, price and platform would look identical here, which is
  the exact mix-up the criterion was meant to catch.
- **Criterion 4 — the price in the criterion isn't the item's price.** It says
  the card should mention `18` or `18.00`, but the query I ran selects a $24
  item, so I checked for `24`. The criterion should say "the item's price"
  rather than a fixed number.

One thing I noticed that isn't a miss: `jeans $25 or less` returned nothing
and stopped early, so it only proves the parser read the phrasing, not that
the filter removed anything. The other four queries did return listings, all
under the ceiling.


---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
[1] parse_query
      in:  looking for a vintage graphic tee under $30
      out: {'description': 'looking for a vintage graphic tee', 'size': None, 'max_price': 30.0}
[2] search_listings (via MCP)
      in:  {'description': 'looking for a vintage graphic tee', 'size': None, 'max_price': 30.0}
      out: 10 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey, Y2K Baby Tee — Butterfly Print … +7 more
      →    branch: got results, going on to select
[3] select_item
      out: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      →    took the first (best-scoring) result
[4] suggest_outfit
      in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      out: **Outfit 1: Casual Grunge Streetwear** Pair the graphic tee with the baggy straight-leg jeans and the brown le…
[5] create_fit_card
      in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      out: Finally found the ultimate 2003 tour bootleg style graphic tee to complete my grunge streetwear rotation, and …

  Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   **Outfit 1: Casual Grunge Streetwear**
Pair the graphic tee with the baggy straight-leg jeans and the brown leather belt. Layer the black cropped zip hoodie on top (wear it unzipped to show off the graphic). Finish with the chunky white sneakers and the black crossbody bag. 

**Outfit 2: Contrast Neutral Mix**
Tuck the graphic tee into the wide-leg khaki trousers, secured with the brown leather belt. Throw the vintage black denim jacket over your shoulders andground the look with the black combat boots. Accessorize with the black crossbody bag for an effortless, balanced fit.

  Fit card: Finally found the ultimate 2003 tour bootleg style graphic tee to complete my grunge streetwear rotation, and I scored it on Depop for just $24.00. The vintage fade on this black top is so good, and it looks insanely cool layered under an unzipped hoodie or tucked into wide-leg trousers. It has that authentic thrifted band merch energy that makes every outfit instantly cooler.

```

**Empty search**

```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    branch: empty, stopping before suggest_outfit

  Nothing matched "designer ballgown" in size XXS under $5. No listing uses those words — try naming the kind of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge).
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->
=> On the the next step of run_agent, I add try cast that except ModelUnavailable for stop the error.
=> The trace should stop at stop [2] with the note "branch: empty, stopping before suggest_outfit".

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

One line in `trace.py::_short` (line 86). When the trace prints a listing, it
now includes the listing's `id`:

```
before:  Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
after:   Denim Jacket — Light Wash, Cropped [id lst_007] ($42.0, poshmark)
```

Nothing in the tools, the loop or the prompts changed.

**Which failure it was meant to fix:**

No criterion missed in the before-run, so this fixes a measurement gap rather
than a miss. Criterion 3 says the `id` search picked must be the `id` that
reached `suggest_outfit` and `create_fit_card`, but the trace only printed
title, price and platform, so I had to score it on those instead. Two listings
with the same title, price and platform would have looked identical.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Item search picked is the item every later tool received | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card names the facts and doesn't repeat itself | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search never returns anything over the price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Source: `results/run_2026-10-11_1525_after.md`, produced by `run_eval.py::main`
running `agent.py::run_agent` (5 tries per scenario, cache off, temperature 0.9).
Same scenarios as the before-run.

- **1:** every try on `vintage graphic tee under $30` reached step `[5] create_fit_card` and returned a card (212–344 chars).
- **2:** every try on `designer ballgown size XXS under $5` ended at step `[2]` with `out: [] (empty)` and the note `branch: empty, stopping before suggest_outfit`.
- **3:** in every try on `denim jacket under $50`, steps `[3] select_item`, `[4] suggest_outfit` and `[5] create_fit_card` all show `[id lst_007]`, and step `[3]` notes it took the first search result. This is now checked by id.
- **4:** all 5 cards for the Graphic Tee name `$24` or `$24.00` and Depop, are 2–3 sentences long, open with 5 different first sentences, and none contains `None`.
- **5:** same five priced queries as the before-run. `max_price` was parsed as the number typed each time (30, 25, 40, 50, 30) and the highest price returned was $27, none (stopped early), $33, $45 and $27.

Real output from try 1 of "selected item carried through":

```
[1] parse_query
      in:  denim jacket under $50
      out: {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
[2] search_listings (via MCP)
      in:  {'description': 'denim jacket', 'size': None, 'max_price': 50.0}
      out: 7 items: Denim Jacket — Light Wash, Cropped, 90s Track Jacket — Navy/White Stripe, High-Waisted Denim Shorts — Cutoff … +4 more
      →    branch: got results, going on to select
[3] select_item
      out: Denim Jacket — Light Wash, Cropped [id lst_007] ($42.0, poshmark)
      →    took the first (best-scoring) result
[4] suggest_outfit
      in:  Denim Jacket — Light Wash, Cropped [id lst_007] ($42.0, poshmark)
      out: **Outfit 1: Casual Streetwear** Layer the new Denim Jacket over the White ribbed tank top and pair with your B…
[5] create_fit_card
      in:  Denim Jacket — Light Wash, Cropped [id lst_007] ($42.0, poshmark)
      out: Score this vintage Wrangler denim jacket for just $42 on Poshmark and instantly level up your streetwear game.…
```

Fit card from that try:

```
Score this vintage Wrangler denim jacket for just $42 on Poshmark and instantly level up your streetwear game. The light wash and cropped fit make it super easy to style, whether you're pairing it with baggy denim for a double-denim moment or balancing out wide-leg trousers. It is the ultimate effortless layering piece for that cool, vintage-meets-modern vibe.
```

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->

It helped with measuring, not with the scores. All five criteria were MET (5/5) before and are MET (5/5) after, so no number moved. What changed is that
criterion 3 can now be checked the way I wrote it: the trace shows the same
`id` (`lst_007`) at steps `[3]`, `[4]` and `[5]` in all five tries, where
before I could only compare titles. The change touched
only how the trace prints, so I didn't expect it to change any result, and it didn't.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

The criterion 4 still names a price of 18 when the item costs $24, and jeans $25 or less returns nothing. I ran out of time.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
