from datetime import datetime

from learn_sync.collectors.calendar import parse_ics

SINGLE = """BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
UID:abc-123
SUMMARY:34870 - Lab A hand-in
DTSTART:20260912T100000Z
DTEND:20260912T120000Z
END:VEVENT
END:VCALENDAR
"""


def test_parses_a_single_event():
    events = parse_ics(SINGLE)

    assert len(events) == 1
    assert events[0].event_id == "abc-123"
    assert events[0].title == "Lab A hand-in"
    assert events[0].starts_at == datetime(2026, 9, 12, 10, 0)


def test_course_code_is_lifted_out_of_the_summary():
    assert parse_ics(SINGLE)[0].course_code == "34870"


def test_summary_without_a_course_code_keeps_the_whole_title():
    ics = SINGLE.replace("SUMMARY:34870 - Lab A hand-in", "SUMMARY:Semester start")

    event = parse_ics(ics)[0]
    assert event.title == "Semester start"
    assert event.course_code == ""


def test_folded_lines_are_unfolded():
    """RFC 5545 wraps long lines; a continuation starts with a space."""
    ics = SINGLE.replace(
        "SUMMARY:34870 - Lab A hand-in",
        "SUMMARY:34870 - Lab A hand-in with a very long\n  title that got folded",
    )

    assert parse_ics(ics)[0].title == "Lab A hand-in with a very long title that got folded"


def test_date_only_values_are_accepted():
    ics = SINGLE.replace("DTSTART:20260912T100000Z", "DTSTART;VALUE=DATE:20260912")

    assert parse_ics(ics)[0].starts_at == datetime(2026, 9, 12, 0, 0)


def test_escaped_characters_are_unescaped():
    ics = SINGLE.replace("SUMMARY:34870 - Lab A hand-in", r"SUMMARY:34870 - Lab A\, part 2")

    assert parse_ics(ics)[0].title == "Lab A, part 2"


def test_multiple_events_are_all_returned():
    ics = SINGLE.replace(
        "END:VCALENDAR",
        "BEGIN:VEVENT\nUID:def-456\nSUMMARY:62755 - Quiz\nDTSTART:20261005T090000Z\n"
        "END:VEVENT\nEND:VCALENDAR",
    )

    events = parse_ics(ics)
    assert [e.event_id for e in events] == ["abc-123", "def-456"]


def test_events_without_a_start_are_dropped():
    ics = SINGLE.replace("DTSTART:20260912T100000Z\n", "")

    assert parse_ics(ics) == []


def test_an_empty_calendar_yields_nothing():
    assert parse_ics("BEGIN:VCALENDAR\nEND:VCALENDAR\n") == []


def test_assignment_deadlines_are_marked_as_such():
    """D2L tags due dates in the summary; those are the ones worth surfacing."""
    ics = SINGLE.replace("SUMMARY:34870 - Lab A hand-in", "SUMMARY:34870 - Report 1 is due")

    assert parse_ics(ics)[0].kind == "assignment"
