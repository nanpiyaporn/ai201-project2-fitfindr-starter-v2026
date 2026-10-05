"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import re

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── query parsing ─────────────────────────────────────────────────────────────

# "under $30", "below 30", "less than $30", "max 30", "$30 or less", "$30 max"
_PRICE_PATTERNS = [
    r"(?:under|below|less than|max(?:imum)?|up to|no more than)\s*\$?\s*(\d+(?:\.\d+)?)",
    r"\$\s*(\d+(?:\.\d+)?)\s*(?:or less|or under|max|tops)",
]
# "size M", "size US 8.5", "size W30", "size S/M"
_SIZE_PATTERN = r"\bsize\s+((?:US|W)\s?\d+(?:\.\d+)?|[A-Z]{1,3}(?:/[A-Z]{1,3})?)\b"
_SIZE_WORDS = {"small": "S", "medium": "M", "large": "L"}


def parse_query(query: str) -> dict:
    """
    Pull a description, a size, and a max_price out of plain language, by regex.
    Whatever isn't a price or a size phrase is left behind as the description.
    """
    text = query
    max_price = None
    for pattern in _PRICE_PATTERNS:
        match = re.search(pattern, text, re.I)
        if match:
            max_price = float(match.group(1))
            text = text[: match.start()] + text[match.end():]
            break

    size = None
    match = re.search(_SIZE_PATTERN, text, re.I)
    if match:
        size = match.group(1).upper()
        text = text[: match.start()] + text[match.end():]
    else:
        match = re.search(r"\b(?:size\s+|in (?:a )?)?(small|medium|large)\b", text, re.I)
        if match:
            size = _SIZE_WORDS[match.group(1).lower()]
            text = text[: match.start()] + text[match.end():]

    description = re.sub(r"[,$]", " ", text)
    description = re.sub(r"\s+", " ", description).strip()
    return {"description": description, "size": size, "max_price": max_price}


def _no_results_message(parsed: dict) -> str:
    """
    Say what to change, not just that nothing came back. Re-runs the search with
    one filter dropped at a time to find out which one is doing the blocking.
    """
    description, size, max_price = parsed["description"], parsed["size"], parsed["max_price"]
    said = f'"{description}"'
    if size:
        said += f" in size {size}"
    if max_price is not None:
        said += f" under ${max_price:g}"

    if max_price is not None:
        without_price = search_listings(description, size, None)
        if without_price:
            cheapest = min(item["price"] for item in without_price)
            return (
                f"Nothing matched {said}. The cheapest match is ${cheapest:g} — "
                f"raise your budget to at least ${cheapest:g}, or try different words."
            )
    if size:
        without_size = search_listings(description, None, max_price)
        if without_size:
            sizes = sorted({item["size"] for item in without_size})
            return (
                f"Nothing matched {said}. Those items come in {', '.join(sizes[:5])} — "
                f"try one of those sizes, or leave the size out."
            )
    return (
        f"Nothing matched {said}. No listing uses those words — try naming the kind "
        f"of item (tee, jeans, jacket, boots) or a style (vintage, y2k, grunge)."
    )


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    session = new_session(query, wardrobe)
    next_step = "parse"
    count = 0

    while next_step != "done":
        count += 1
        trace.check_iterations(count)

        if next_step == "parse":
            session["parsed"] = parse_query(session["query"])
            next_step = "search"

        elif next_step == "search":
            parsed = session["parsed"]
            session["search_results"] = search_listings(
                parsed["description"], parsed["size"], parsed["max_price"]
            )
            # The branch: an empty search ends the run here.
            if not session["search_results"]:
                session["error"] = _no_results_message(session["parsed"])
                next_step = "done"
            else:
                next_step = "select"

        elif next_step == "select":
            session["selected_item"] = session["search_results"][0]
            next_step = "outfit"

        elif next_step == "outfit":
            session["outfit_suggestion"] = suggest_outfit(
                session["selected_item"], session["wardrobe"]
            )
            next_step = "fit_card"

        elif next_step == "fit_card":
            session["fit_card"] = create_fit_card(
                session["outfit_suggestion"], session["selected_item"]
            )
            next_step = "done"

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
