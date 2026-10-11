"""
A trace: a printed record of what your agent did, step by step, in order.

Right now, when your agent does something strange, your only evidence is the
final output. A trace turns that into a sequence you can point at.

You'll add trace calls to your loop in unit 4, Milestone 2. The formatting is
done for you here so you're not fighting alignment — what's yours is deciding
*where* the calls go, which is the part that makes the trace worth reading.

Use it like this, inside `run_agent()`:

    from trace import step, start_trace, get_trace

    start_trace()
    ...
    step("search_listings", inputs={"description": desc, "max_price": 30},
         returned=results)

At the end, `get_trace()` gives you the whole thing as text, ready to paste
into your README under **Loop Trace**.

Two things the rubric wants to see in it: every tool call in order, and the
MCP call visible among them. If you moved `search_listings` onto MCP, say so
in the step name — `search_listings (via MCP)` is enough.
"""

import config

_lines: list[str] = []
_step_number = 0


def start_trace() -> None:
    """Clear the trace. Call this at the start of each run."""
    global _step_number
    _lines.clear()
    _step_number = 0


def step(name: str, inputs=None, returned=None, note: str = "") -> None:
    """
    Record one step of the loop.

    Args:
        name:     what happened — usually a tool name.
        inputs:   what went in. Anything printable.
        returned: what came back. Shortened automatically, so passing a long
                  list of listings is fine.
        note:     an optional word on why, e.g. "branch: empty, stopping".
    """
    global _step_number
    _step_number += 1

    line = f"[{_step_number}] {name}"
    if inputs is not None:
        line += f"\n      in:  {_short(inputs)}"
    if returned is not None:
        line += f"\n      out: {_short(returned)}"
    if note:
        line += f"\n      →    {note}"

    _lines.append(line)
    print(line, flush=True)


def get_trace() -> str:
    """The whole trace as text, ready to paste into your README."""
    return "\n".join(_lines)


def _short(value, limit: int = 110) -> str:
    """Keep the trace readable. A 40-item list of dicts is not readable."""
    if isinstance(value, list):
        if not value:
            return "[] (empty)"
        head = value[0]
        if isinstance(head, dict) and "title" in head:
            titles = ", ".join(str(v.get("title", "?")) for v in value[:3])
            more = f" … +{len(value) - 3} more" if len(value) > 3 else ""
            return f"{len(value)} items: {titles}{more}"
        return f"{len(value)} items: {str(head)[:60]}…"

    if isinstance(value, dict):
        if "title" in value:
            return f"{value.get('title')} [id {value.get('id')}] (${value.get('price')}, {value.get('platform')})"
        keys = ", ".join(list(value)[:6])
        return f"dict with keys: {keys}"

    text = str(value).replace("\n", " ")
    return text if len(text) <= limit else text[:limit] + "…"


def check_iterations(count: int) -> None:
    """
    Stop condition. Raise if the loop has gone round too many times.

    Your loop this unit is short enough that you may never hit this. Keep the
    call anyway — a missing stop condition is the most common architectural
    failure in production agents, and the habit is the point.
    """
    if count > config.MAX_ITERATIONS:
        raise RuntimeError(
            f"The loop ran {count} times, past MAX_ITERATIONS "
            f"({config.MAX_ITERATIONS}) in config.py.\n"
            f"That almost always means a branch isn't ending. Print the value "
            f"your branch checks, on the line before the `if`."
        )
