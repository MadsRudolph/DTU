"""Deadlines and lectures from the Brightspace calendar API.

Source: `/d2l/api/le/1.67/{orgUnitId}/calendar/events/myEvents/` with an explicit
`startDateTime`/`endDateTime` range -- without the range it answers 400. It is
JSON rather than an iCal feed, and it is per course.
"""

from __future__ import annotations

import re
from datetime import datetime

from ..models import Course, Event

EVENTS_PATH = (
    "/d2l/api/le/1.67/{org_unit_id}/calendar/events/myEvents/"
    "?startDateTime={start}&endDateTime={end}"
)

_ASSIGNMENT = re.compile(r"\bdue\b|hand-?in|deadline|aflever|innleve", re.IGNORECASE)
_LEADING_CODE = re.compile(r"^\s*\d{5}\s+")


def _parse_dt(value) -> datetime | None:
    if not value:
        return None
    text = str(value).replace("Z", "")
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def parse_events(payload: dict, course: Course) -> list[Event]:
    events: list[Event] = []

    for raw in payload.get("Objects") or []:
        starts_at = _parse_dt(raw.get("StartDateTime"))
        if starts_at is None:
            continue

        # Titles repeat the course code, which is already its own column.
        title = _LEADING_CODE.sub("", str(raw.get("Title") or "")).strip()

        events.append(
            Event(
                event_id=str(raw.get("CalendarEventId")),
                course_code=course.code,
                title=title,
                starts_at=starts_at,
                kind="assignment" if _ASSIGNMENT.search(title) else "other",
            )
        )

    return events
