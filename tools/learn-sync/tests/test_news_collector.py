"""Announcement parsing, against the real /d2l/api/le/1.67/{ou}/news/ shape.

Captured 2026-08-31 from 34870. Body arrives as both Text and Html; the plain
Text carries CRLF line endings that would otherwise leak into the vault note.
"""

from datetime import datetime

from learn_sync.collectors.news import parse_news
from learn_sync.models import Course

COURSE = Course(org_unit_id="325536", code="34870", name="Electroacoustics")

PAYLOAD = [
    {
        "Id": 184779,
        "IsHidden": False,
        "Attachments": [],
        "CreatedDate": "2024-08-20T08:39:27.570Z",
        "LastModifiedDate": "2026-08-23T12:50:15.077Z",
        "Title": "Welcome to the course",
        "Body": {"Text": "Dear all,\r\nWelcome.\r\n", "Html": "<p>Dear all,</p>"},
    },
    {
        "Id": 184999,
        "IsHidden": True,
        "Attachments": [],
        "CreatedDate": "2026-08-25T08:00:00.000Z",
        "LastModifiedDate": "2026-08-25T08:00:00.000Z",
        "Title": "Draft notice",
        "Body": {"Text": "not published", "Html": ""},
    },
]


def test_announcements_are_parsed():
    news = parse_news(PAYLOAD, COURSE, since=None)

    assert len(news) == 1
    assert news[0].title == "Welcome to the course"
    assert news[0].course_code == "34870"


def test_hidden_announcements_are_skipped():
    assert "Draft notice" not in {n.title for n in parse_news(PAYLOAD, COURSE, since=None)}


def test_crlf_is_normalised_out_of_the_body():
    body = parse_news(PAYLOAD, COURSE, since=None)[0].body_markdown

    assert "\r" not in body
    assert "Dear all,\nWelcome." in body


def test_posted_at_uses_the_last_modified_date():
    """A lecturer editing an old post is news; the creation date is not."""
    assert parse_news(PAYLOAD, COURSE, since=None)[0].posted_at == datetime(
        2026, 8, 23, 12, 50, 15, 77000
    )


def test_since_watermark_filters_already_seen_posts():
    assert parse_news(PAYLOAD, COURSE, since="184779") == []


def test_since_watermark_lets_newer_posts_through():
    assert len(parse_news(PAYLOAD, COURSE, since="100000")) == 1


def test_an_empty_feed_yields_nothing():
    assert parse_news([], COURSE, since=None) == []
