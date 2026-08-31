"""Which courses are we enrolled in this semester.

Read off the dashboard rather than the Valence API, which needs an institution-
issued app key a student cannot self-register. Course links are matched by
their /d2l/home/<orgUnitId> shape, which is stable across Brightspace themes.
"""

from __future__ import annotations

import re

from ..models import Course

_COURSE_LINK = re.compile(
    r'href="/d2l/home/(?P<ou>\d+)"[^>]*>(?P<label>[^<]+)<', re.IGNORECASE
)
# "34870 Electroacoustics E26" -> code 34870, name Electroacoustics
_LABEL = re.compile(r"^\s*(?P<code>\d{5})\s+(?P<name>.+?)\s*$")
_SEMESTER_SUFFIX = re.compile(r"\s+[EF]\d{2}$")


def parse_courses(html: str) -> list[Course]:
    """Extract enrolled courses, ignoring admin org units and duplicate links."""
    courses: list[Course] = []
    seen: set[str] = set()

    for match in _COURSE_LINK.finditer(html):
        label = match.group("label").strip()
        parsed = _LABEL.match(label)
        if not parsed:
            # No 5-digit course code: an administrative org unit, not a course.
            continue

        org_unit_id = match.group("ou")
        if org_unit_id in seen:
            continue
        seen.add(org_unit_id)

        courses.append(
            Course(
                org_unit_id=org_unit_id,
                code=parsed.group("code"),
                name=_SEMESTER_SUFFIX.sub("", parsed.group("name")).strip(),
            )
        )

    return courses
