"""Course announcements from the Brightspace news API.

Source: `/d2l/api/le/1.67/{orgUnitId}/news/`, which returns a plain list. The
body arrives as both `Text` and `Html`; the plain text carries CRLF line endings
that would otherwise leak into the vault note.

`LastModifiedDate` is used rather than `CreatedDate`: lecturers routinely edit an
old welcome post to carry this year's information, and that edit is the news.
"""

from __future__ import annotations

from datetime import datetime

from ..models import Announcement, Course

NEWS_PATH = "/d2l/api/le/1.67/{org_unit_id}/news/"


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


def parse_news(payload, course: Course, since: str | None) -> list[Announcement]:
    """Parse announcements newer than the `since` watermark (a previous post id)."""
    announcements: list[Announcement] = []
    watermark = int(since) if since and str(since).isdigit() else None

    for raw in payload or []:
        if raw.get("IsHidden"):
            continue

        news_id = raw.get("Id")
        if watermark is not None and news_id is not None and int(news_id) <= watermark:
            continue

        posted_at = _parse_dt(raw.get("LastModifiedDate")) or _parse_dt(
            raw.get("CreatedDate")
        )
        if posted_at is None:
            continue

        body = (raw.get("Body") or {}).get("Text") or ""
        announcements.append(
            Announcement(
                announcement_id=str(news_id),
                course_code=course.code,
                posted_at=posted_at,
                title=str(raw.get("Title") or "").strip(),
                body_markdown=body.replace("\r\n", "\n").replace("\r", "\n").strip(),
            )
        )

    return announcements
