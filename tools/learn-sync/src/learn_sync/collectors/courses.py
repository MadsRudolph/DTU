"""Which courses are we enrolled in, from the Valence LP enrolments API.

`/d2l/api/lp/1.47/enrollments/myenrollments/?orgUnitTypeId=3` answers with a
plain session cookie -- no institution app key needed -- so this is a documented
JSON API rather than scraped markup.

Two traps the live payload revealed:

* Every enrolment reports `IsActive: true`, including courses from 2024. Activity
  cannot be used to find the current semester; the `Code` field's semester token
  (`DTU_e26_34870` -> autumn 2026) is the only reliable signal.
* DTU mixes non-course org units (DesignBuildLab, "How to DTU", the DTU root)
  into the same list. They have no `DTU_<sem>_<code>` code and are dropped.
"""

from __future__ import annotations

import re

from ..models import Course

ENROLMENTS_PATH = "/d2l/api/lp/1.47/enrollments/myenrollments/?orgUnitTypeId=3"

# "DTU_e26_34870" -> semester e26, course 34870
_CODE = re.compile(r"^DTU_(?P<semester>[a-z]\d{2})_(?P<course>\d{5})$", re.IGNORECASE)
# "34870 Electroacoustics, Fall 2026" -> "Electroacoustics"
_NAME = re.compile(
    r"^\s*\d{5}\s+(?P<name>.+?)(?:,\s*(?:Fall|Spring|Summer|June|January)\s+\d{4})?\s*$"
)


def parse_enrollments(payload: dict, semesters=None) -> list[Course]:
    """Return the real courses, optionally narrowed to given semester tokens.

    `semesters` is a list like ["e26"]; None means every course ever enrolled in.
    """
    courses: list[Course] = []

    for item in payload.get("Items") or []:
        org_unit = item.get("OrgUnit") or {}
        matched = _CODE.match(str(org_unit.get("Code") or ""))
        if not matched:
            continue

        if semesters is not None and matched.group("semester").lower() not in {
            s.lower() for s in semesters
        }:
            continue

        raw_name = str(org_unit.get("Name") or "")
        name = _NAME.match(raw_name)
        courses.append(
            Course(
                org_unit_id=str(org_unit.get("Id")),
                code=matched.group("course"),
                name=name.group("name").strip() if name else raw_name.strip(),
            )
        )

    return courses
