"""Recover which message a pre-attribution Little Tutor thread came from.

``tutor_source_message_id`` is written when a side chat is opened, but threads
created before that field existed only kept the passage itself: either in
``preferences.tutor_selected_text`` (selection-scope threads) or as a quote
attachment on the thread's first user message. Both are enough to find the
message the learner selected, using the same Markdown projection that grounds
a live selection.

A passage that occurs in exactly one parent message is authoritative. One that
occurs in several is left alone rather than guessing, and a thread with no
passage at all is never attributed. The work is recorded per thread so the
scan runs once, not on every thread-list read.
"""

from __future__ import annotations

import logging
from typing import Any

from .quote_attachments import read_quotes
from .selection_grounding import rendered_markdown_text

logger = logging.getLogger(__name__)

# Set once attribution has been attempted (successfully or not) so a thread is
# not re-scanned on every read. Clearing an anchor also sets it, which keeps a
# deliberate detach from being undone by a later backfill.
BACKFILL_ATTEMPTED_KEY = "tutor_source_backfill_attempted"
# One request may have to recover several threads; each needs the thread's
# transcript and (at most once) the parent's. Keep a single caller bounded.
MAX_BACKFILLED_THREADS = 50
# Shorter passages match too many messages to be evidence of a source.
MIN_QUOTE_CHARS = 8
_TRANSCRIPT_ROLES = frozenset({"user", "assistant"})


def _normalized(text: str) -> str:
    return " ".join(str(text or "").split())


def locate_quote_message(messages: list[dict[str, Any]], quote: str) -> int | str | None:
    """The one parent message containing ``quote``, or None when ambiguous."""
    needle = _normalized(quote)
    if len(needle) < MIN_QUOTE_CHARS:
        return None
    matches: list[tuple[Any, str]] = []
    for message in messages:
        role = str(message.get("role") or "")
        if role not in _TRANSCRIPT_ROLES:
            continue
        content = str(message.get("content") or "")
        if not content:
            continue
        if needle in _normalized(content):
            matches.append((message.get("id"), role))
            continue
        try:
            if needle in rendered_markdown_text(content):
                matches.append((message.get("id"), role))
        except Exception:
            # A message the Markdown projection cannot read simply does not
            # ground this passage; it must not take the whole scan down.
            logger.debug("tutor thread backfill: unreadable message", exc_info=True)
    matches = [(message_id, role) for message_id, role in matches if message_id is not None]
    assistant_matches = [message_id for message_id, role in matches if role == "assistant"]
    if len(assistant_matches) == 1:
        return assistant_matches[0]
    if len(matches) == 1:
        return matches[0][0]
    return None


async def _quote_for_thread(store: Any, thread: dict[str, Any]) -> str:
    """The passage a thread was opened from, from preferences or its quote."""
    preferences = thread.get("preferences") or {}
    stored = str(preferences.get("tutor_selected_text") or "").strip()
    if stored:
        return stored
    session_id = str(thread.get("session_id") or "").strip()
    if not session_id:
        return ""
    messages = await store.get_messages(session_id)
    first_user = next((message for message in messages if message.get("role") == "user"), None)
    if first_user is None:
        return ""
    quotes = read_quotes(list(first_user.get("attachments") or []))
    return quotes[0] if quotes else ""


async def backfill_thread_sources(
    store: Any,
    parent_session_id: str,
    threads: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Attribute legacy threads in place; return the same rows."""
    pending = [
        thread
        for thread in threads
        if not (thread.get("preferences") or {}).get("tutor_source_message_id")
        and not (thread.get("preferences") or {}).get(BACKFILL_ATTEMPTED_KEY)
    ]
    if not pending:
        return threads

    parent_messages: list[dict[str, Any]] | None = None
    for thread in pending[:MAX_BACKFILLED_THREADS]:
        preferences = dict(thread.get("preferences") or {})
        try:
            quote = await _quote_for_thread(store, thread)
            message_id = None
            if quote:
                if parent_messages is None:
                    parent_messages = await store.get_messages(parent_session_id)
                message_id = locate_quote_message(parent_messages, quote)
            updates: dict[str, Any] = {BACKFILL_ATTEMPTED_KEY: True}
            if message_id is not None:
                updates["tutor_source_message_id"] = message_id
            # ``touch=False`` keeps the thread where it was in the newest-first
            # list; recovering an anchor is not activity.
            await store.update_session_preferences(
                str(thread.get("session_id") or ""), updates, touch=False
            )
        except Exception:
            logger.warning(
                "could not recover the source of tutor thread %s",
                thread.get("session_id"),
                exc_info=True,
            )
            continue
        thread["preferences"] = {**preferences, **updates}
    return threads


__all__ = [
    "BACKFILL_ATTEMPTED_KEY",
    "MAX_BACKFILLED_THREADS",
    "backfill_thread_sources",
    "locate_quote_message",
]
