"""Enrolment parsing, against the real /d2l/api/lp/1.47/enrollments/myenrollments/ shape.

Captured from a live session on 2026-08-31. Two things this payload taught us:
every enrolment reads IsActive=true, even courses from 2024, so activity is
useless for picking out the current semester -- the Code field's semester token
is the real signal. And DTU mixes non-course org units into the same list.
"""

from learn_sync.collectors.courses import parse_enrollments

PAYLOAD = {
    "PagingInfo": {"Bookmark": "325536", "HasMoreItems": False},
    "Items": [
        {
            "OrgUnit": {
                "Id": 325536,
                "Type": {"Id": 3, "Code": "Course Offering"},
                "Name": "34870 Electroacoustics, Fall 2026",
                "Code": "DTU_e26_34870",
            },
            "Access": {"IsActive": True},
        },
        {
            "OrgUnit": {
                "Id": 325428,
                "Type": {"Id": 3, "Code": "Course Offering"},
                "Name": "62755 Power Electronics, Fall 2026",
                "Code": "DTU_e26_62755",
            },
            "Access": {"IsActive": True},
        },
        {
            "OrgUnit": {
                "Id": 293661,
                "Type": {"Id": 3, "Code": "Course Offering"},
                "Name": "34722 Linear control design 1, Spring 2026",
                "Code": "DTU_f26_34722",
            },
            "Access": {"IsActive": True},
        },
        {
            "OrgUnit": {
                "Id": 121765,
                "Type": {"Id": 3, "Code": "Course Offering"},
                "Name": "DesignBuildLab",
                "Code": "CO_62DBL",
            },
            "Access": {"IsActive": True},
        },
        {
            "OrgUnit": {
                "Id": 6606,
                "Type": {"Id": 1, "Code": "Organization"},
                "Name": "DTU Learn - Technical University of Denmark",
                "Code": "DTU",
            },
            "Access": {"IsActive": True},
        },
    ],
}


def test_semester_filter_selects_only_the_current_term():
    courses = parse_enrollments(PAYLOAD, semesters=["e26"])

    assert {c.code for c in courses} == {"34870", "62755"}


def test_an_old_course_is_excluded_by_semester_not_by_activity():
    """Every enrolment reports IsActive=true, so only the semester token can filter."""
    spring = [i for i in PAYLOAD["Items"] if i["OrgUnit"]["Code"] == "DTU_f26_34722"][0]
    assert spring["Access"]["IsActive"] is True

    assert "34722" not in {c.code for c in parse_enrollments(PAYLOAD, semesters=["e26"])}
    assert "34722" in {c.code for c in parse_enrollments(PAYLOAD, semesters=["f26"])}


def test_course_code_comes_from_the_code_field():
    course = next(c for c in parse_enrollments(PAYLOAD, semesters=["e26"])
                  if c.code == "34870")

    assert course.org_unit_id == "325536"


def test_semester_suffix_is_stripped_from_the_name():
    course = next(c for c in parse_enrollments(PAYLOAD, semesters=["e26"])
                  if c.code == "34870")

    assert course.name == "Electroacoustics"


def test_org_units_without_a_dtu_course_code_are_ignored():
    """DesignBuildLab and the DTU root org unit are not courses."""
    names = {c.name for c in parse_enrollments(PAYLOAD, semesters=None)}

    assert "DesignBuildLab" not in names
    assert not any("Technical University" in n for n in names)


def test_no_semester_filter_returns_every_real_course():
    assert {c.code for c in parse_enrollments(PAYLOAD, semesters=None)} == {
        "34870", "62755", "34722"
    }


def test_several_semesters_can_be_requested():
    codes = {c.code for c in parse_enrollments(PAYLOAD, semesters=["e26", "f26"])}

    assert codes == {"34870", "62755", "34722"}


def test_an_empty_payload_yields_nothing():
    assert parse_enrollments({"Items": []}, semesters=["e26"]) == []
