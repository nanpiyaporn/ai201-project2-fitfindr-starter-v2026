# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
My search is a plain keyword-overlap score, so a phrasing like "old band shirt"
can miss a listing titled "Vintage Graphic Tee" even though a person would call
it a match. Two of the three steps also call the model, so one try in five can
fail for reasons outside my code. 5 of 5 would be testing my luck with wording,
not whether the loop works.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
This path never touches the model. It's one `if not session["search_results"]`
check in `run_agent`, and the same empty list goes into it every time. There's
no randomness to allow for, so a single miss means the branch is wrong, and
anything less than 5 of 5 would be letting a bug through.

---

## 3. The item search picked is the item every later tool received

For 5 matching queries, `session["selected_item"]["id"]` equals
`session["search_results"][0]["id"]`, and the trace shows that same `id` in the
`new_item` input of both `suggest_outfit` and `create_fit_card` — 5 of 5 runs,
zero mismatched ids.

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->
     In 5 matching runs, the item search pick keeps the same listing 'id'. It must match 'search_results[0]', 'search_item', and the 'new_item'. that reaches both 'suggest_outfit' and 'create_fit_card(check through the trace).Target is 5 of 5 because passing a dict through the session involves no model.

**Why this target:**
Passing a dict through the session is plain Python with no model involved, so
there is nothing that should vary between runs. If an id ever differs, I've
overwritten the session or passed the wrong variable  that's a bug, and I'd
rather it show up as a failed criterion than as a fit card describing a jacket
when the search found a tee. Comparing ids instead of titles means two listings
with similar names can't hide a mix-up.


---

## 4. The fit card names the facts and doesn't repeat itself

Run `create_fit_card` 5 times on the same item with the cache off
(`AI201_CACHE=0`). At least 4 of the 5 cards mention the item's price (as
`18` or `18.00`) and its platform, and are 2–4 sentences long. Across all 5,
no two cards open with the same first sentence, and no card ever contains the
word `None` — 5 of 5.

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

     Run it 5 times one item with the cache turned off ( AI201_CACHE = 0)
     - At least 4 of 5 cards name the price the platform and 2-4 sentences long (the model doesn't always follow the prompt).


**Why this target:**
The words are supposed to change — `TEMPERATURE` is 0.9 — so I'm only checking
the things a buyer actually needs (price, where to buy it) and that it's short
enough to post. The model follows the prompt most of the time, not every time,
so one card in five that drops the price or runs to five sentences is the model
being a model, not my code being wrong. The `None` check is 5 of 5 because most
listings have `brand: null`, and if `None` ever shows up in a caption, that's
my prompt formatting, not the model.


---

## 5. Search never returns anything over the price ceiling

For 5 queries that name a price — using at least three different phrasings,
e.g. "under $30", "$25 or less", "max 40" — every listing in
`session["search_results"]` has `price <= session["parsed"]["max_price"]`, and
`max_price` is the number the user typed. 5 of 5 queries, zero listings over.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

**Why this target:**
A budget is the one thing a thrift shopper won't forgive — showing a $45 jacket
to someone who said "under $30" makes the whole tool feel broken. The filter is
a plain number comparison, so it should never miss. The real risk is the
parser: if a phrasing like "max 40" doesn't get read, `max_price` comes back
`None` and the filter silently switches off. That's why I'm using several
phrasings instead of only "under $X" — an easy query would pass even if my
parsing was broken.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
