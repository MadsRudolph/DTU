"""Calendar parsing, against the real myEvents shape.

Captured 2026-08-31 from
/d2l/api/le/1.67/{ou}/calendar/events/myEvents/?startDateTime=..&endDateTime=..
It is JSON, not an iCal feed, and it requires an explicit date range.
"""

from datetime import datetime

from learn_sync.collectors.events import parse_events
from learn_sync.models import Course

COURSE = Course(org_unit_id="325536", code="34870", name="Electroacoustics")

PAYLOAD = {
    "Objects": [
        {
            "CalendarEventId": 395865,
            "OrgUnitId": 325536,
            "Title": "34870 Lecture 0 E26 - Introduction to the course",
            "Description": "",
            "StartDateTime": "2026-08-31T07:00:00.000Z",
            "EndDateTime": "2026-08-31T11:00:00.000Z",
            "IsAllDayEvent": False,
        },
        {
            "CalendarEventId": 395999,
            "OrgUnitId": 325536,
            "Title": "Lab A report is due",
            "Description": "Hand in via the assignment folder",
            "StartDateTime": "2026-09-28T22:00:00.000Z",
            "EndDateTime": "2026-09-28T22:00:00.000Z",
            "IsAllDayEvent": False,
        },
    ],
    "Next": None,
}


def test_events_are_parsed_with_their_course():
    events = parse_events(PAYLOAD, COURSE)

    assert len(events) == 2
    assert {e.course_code for e in events} == {"34870"}


def test_start_time_is_parsed():
    first = parse_events(PAYLOAD, COURSE)[0]

    assert first.starts_at == datetime(2026, 8, 31, 7, 0)


def test_event_id_is_the_calendar_event_id():
    assert parse_events(PAYLOAD, COURSE)[0].event_id == "395865"


def test_a_course_code_prefix_is_stripped_from_the_title():
    """Titles repeat the course code, which is already a column of its own."""
    first = parse_events(PAYLOAD, COURSE)[0]

    assert first.title == "Lecture 0 E26 - Introduction to the course"


def test_deadlines_are_marked_as_assignments():
    due = next(e for e in parse_events(PAYLOAD, COURSE) if "Lab A" in e.title)

    assert due.kind == "assignment"


def test_ordinary_lectures_are_not_marked_as_assignments():
    assert parse_events(PAYLOAD, COURSE)[0].kind == "other"


def test_events_without_a_start_are_dropped():
    payload = {"Objects": [{"CalendarEventId": 1, "Title": "x", "StartDateTime": None}]}

    assert parse_events(payload, COURSE) == []


def test_an_empty_calendar_yields_nothing():
    assert parse_events({"Objects": [], "Next": None}, COURSE) == []
