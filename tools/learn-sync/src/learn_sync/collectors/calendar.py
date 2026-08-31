"""Deadlines and events from the Brightspace iCal subscription feed.

The feed is plain RFC 5545, so unlike the HTML scrapers this parser does not
depend on Brightspace markup and will not break when D2L restyles a page. Only
the feed URL itself has to be discovered once.
"""

from __future__ import annotations

import re
from datetime import datetime

from ..models import Event

_COURSE_CODE = re.compile(r"^\s*(\d{5})\s*[-–:]?\s*(.*)$")
_ASSIGNMENT = re.compile(r"\bdue\b|hand-?in|deadline|aflever", re.IGNORECASE)


def _unfold(text: str) -> list[str]:
    """Rejoin RFC 5545 folded lines, where a continuation begins with a space or tab."""
    lines: list[str] = []
    for raw in text.splitlines():
        if raw[:1] in (" ", "\t") and lines:
            lines[-1] += raw[1:]
        else:
            lines.append(raw)
    return lines


def _unescape(value: str) -> str:
    return (
        value.replace("\\n", "\n")
        .replace("\\N", "\n")
        .replace("\\,", ",")
        .replace("\\;", ";")
        .replace("\\\\", "\\")
    )


def _parse_dt(value: str) -> datetime | None:
    value = value.strip().rstrip("Z")
    for fmt in ("%Y%m%dT%H%M%S", "%Y%m%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return None


def parse_ics(text: str) -> list[Event]:
    events: list[Event] = []
    current: dict[str, str] | None = None

    for line in _unfold(text):
        if line.startswith("BEGIN:VEVENT"):
            current = {}
            continue
        if line.startswith("END:VEVENT"):
            if current is not None:
                event = _build(current)
                if event is not None:
                    events.append(event)
            current = None
            continue
        if current is None or ":" not in line:
            continue

        name, _, value = line.partition(":")
        # Strip parameters such as ";VALUE=DATE" from the property name.
        current[name.split(";", 1)[0].upper()] = value

    return events


def _build(fields: dict[str, str]) -> Event | None:
    starts_at = _parse_dt(fields.get("DTSTART", ""))
    if starts_at is None:
        return None

    summary = _unescape(fields.get("SUMMARY", "")).strip()
    course_code = ""
    match = _COURSE_CODE.match(summary)
    if match:
        course_code, summary = match.group(1), match.group(2).strip()

    return Event(
        event_id=fields.get("UID", summary),
        course_code=course_code,
        title=summary,
        starts_at=starts_at,
        kind="assignment" if _ASSIGNMENT.search(summary) else "other",
    )
