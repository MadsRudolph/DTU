from datetime import datetime

from learn_sync.models import Announcement, Event
from learn_sync.notes import (
    inject_block,
    render_announcements,
    render_deadlines,
    render_index,
)

MARKER = "learn-sync:deadlines"


# --- Home.md marker injection -------------------------------------------------


def test_injects_block_with_markers_when_absent():
    result = inject_block("# Home\n\nMy timetable\n", MARKER, "DEADLINES")

    assert "<!-- learn-sync:deadlines:start -->" in result
    assert "<!-- learn-sync:deadlines:end -->" in result
    assert "DEADLINES" in result
    assert "My timetable" in result


def test_replaces_only_the_region_between_markers():
    doc = (
        "# Home\n\nBefore text\n\n"
        "<!-- learn-sync:deadlines:start -->\n"
        "OLD CONTENT\n"
        "<!-- learn-sync:deadlines:end -->\n\n"
        "After text\n"
    )

    result = inject_block(doc, MARKER, "NEW CONTENT")

    assert "OLD CONTENT" not in result
    assert "NEW CONTENT" in result
    assert "Before text" in result
    assert "After text" in result


def test_injection_is_idempotent():
    once = inject_block("# Home\n", MARKER, "BODY")
    twice = inject_block(once, MARKER, "BODY")

    assert once == twice


def test_injection_does_not_disturb_other_marker_blocks():
    doc = (
        "<!-- learn-sync:other:start -->\n"
        "OTHER\n"
        "<!-- learn-sync:other:end -->\n"
        "<!-- learn-sync:deadlines:start -->\n"
        "OLD\n"
        "<!-- learn-sync:deadlines:end -->\n"
    )

    result = inject_block(doc, MARKER, "NEW")

    assert "OTHER" in result
    assert "OLD" not in result


def test_empty_marker_region_gets_filled():
    doc = (
        "<!-- learn-sync:deadlines:start -->\n"
        "<!-- learn-sync:deadlines:end -->\n"
    )

    assert "BODY" in inject_block(doc, MARKER, "BODY")


# --- INDEX.md -----------------------------------------------------------------


def test_index_renders_nested_modules_with_links():
    entries = [
        (("Week 1",), "Intro slides", "Obsidian/Courses/34870 X/Slides/intro.pdf"),
        (("Week 1", "Extra"), "Bonus", "Obsidian/Courses/34870 X/_Learn/Week 1/Extra/b.pdf"),
        (("Week 2",), "Lab guide", "Obsidian/Courses/34870 X/Labs/lab.pdf"),
    ]

    result = render_index("34870 Electroacoustics", entries)

    assert "## Week 1" in result
    assert "### Extra" in result
    assert "## Week 2" in result
    # Links are vault-relative wiki links, so the "Obsidian/" prefix is stripped.
    assert "[[Courses/34870 X/Slides/intro.pdf|Intro slides]]" in result
    assert "Obsidian/Courses" not in result


def test_index_orders_modules_as_brightspace_returned_them():
    entries = [
        (("Week 9",), "late", "Obsidian/a.pdf"),
        (("Week 1",), "early", "Obsidian/b.pdf"),
    ]

    result = render_index("X", entries)

    assert result.index("Week 9") < result.index("Week 1")


# --- Announcements.md ---------------------------------------------------------


def announcement(ann_id="1", day=1, title="Welcome") -> Announcement:
    return Announcement(
        announcement_id=ann_id,
        course_code="34870",
        posted_at=datetime(2026, 9, day),
        title=title,
        body_markdown="Body text",
    )


def test_announcements_file_is_created_with_heading():
    result = render_announcements("", [announcement()])

    assert result.startswith("# Announcements")
    assert "## 2026-09-01 — Welcome" in result
    assert "Body text" in result


def test_new_announcements_are_prepended_above_existing_ones():
    existing = "# Announcements\n\n## 2026-09-01 — Old\n\nOld body\n"

    result = render_announcements(existing, [announcement(day=2, title="New")])

    assert result.index("New") < result.index("Old")
    assert "Old body" in result


def test_multiple_new_announcements_are_newest_first():
    result = render_announcements(
        "", [announcement(day=1, title="First"), announcement(day=3, title="Third")]
    )

    assert result.index("Third") < result.index("First")


# --- Deadlines ----------------------------------------------------------------


def test_deadlines_render_as_a_dated_table_soonest_first():
    events = [
        Event("2", "62755", "Report 2", datetime(2026, 10, 5), kind="assignment"),
        Event("1", "34870", "Lab A", datetime(2026, 9, 12), kind="assignment"),
    ]

    result = render_deadlines(events)

    assert result.index("Lab A") < result.index("Report 2")
    assert "2026-09-12" in result
    assert "34870" in result


def test_empty_deadlines_render_a_placeholder_not_an_empty_table():
    result = render_deadlines([])

    assert result.strip() != ""
    assert "|" not in result
