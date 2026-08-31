from pathlib import PurePosixPath

import pytest

from learn_sync.filing import load_rules, resolve_collision
from learn_sync.models import Course, Topic

RULES_YAML = """
courses:
  "34870":
    vault: "34870 Electroacoustics"
    rules:
      - {module: "^Lab", to: "Labs/"}
      - {file: "(?i)lecture.*pdf$", to: "Slides/"}
      - {module: "(?i)literature", file: "(?i)pdf$", to: "Literature/"}
    default: "_Learn/{module}/"
"""


def topic(**kw) -> Topic:
    defaults = dict(
        topic_id="1",
        course_code="34870",
        module_path=("Week 1",),
        title="t",
        filename="handout.pdf",
        download_url="https://example/1",
        revision="a",
    )
    defaults.update(kw)
    return Topic(**defaults)


COURSE = Course(org_unit_id="100", code="34870", name="Electroacoustics")


def test_first_matching_rule_wins():
    rules = load_rules(RULES_YAML)
    # Matches both the ^Lab module rule and the lecture-pdf file rule; Lab is first.
    t = topic(module_path=("Lab A",), filename="Lecture notes.pdf")

    assert rules.path_for(t, COURSE) == PurePosixPath(
        "Obsidian/Courses/34870 Electroacoustics/Labs/Lecture notes.pdf"
    )


def test_module_rule_matches_joined_module_path():
    rules = load_rules(RULES_YAML)
    t = topic(module_path=("Labs", "Lab 3"), filename="guide.docx")

    assert rules.path_for(t, COURSE).parent == PurePosixPath(
        "Obsidian/Courses/34870 Electroacoustics/Labs"
    )


def test_file_rule_matches_filename():
    rules = load_rules(RULES_YAML)
    t = topic(module_path=("Week 2",), filename="Lecture 4 handout.pdf")

    assert rules.path_for(t, COURSE) == PurePosixPath(
        "Obsidian/Courses/34870 Electroacoustics/Slides/Lecture 4 handout.pdf"
    )


def test_rule_with_module_and_file_requires_both():
    rules = load_rules(RULES_YAML)
    # Module matches "literature" but the file is not a pdf, so the rule must not fire.
    t = topic(module_path=("Literature",), filename="reading list.txt")

    assert rules.path_for(t, COURSE) == PurePosixPath(
        "Obsidian/Courses/34870 Electroacoustics/_Learn/Literature/reading list.txt"
    )


def test_unmatched_topic_falls_back_to_default_with_module_interpolated():
    rules = load_rules(RULES_YAML)
    t = topic(module_path=("Week 5", "Extra"), filename="notes.txt")

    assert rules.path_for(t, COURSE) == PurePosixPath(
        "Obsidian/Courses/34870 Electroacoustics/_Learn/Week 5/Extra/notes.txt"
    )


def test_unknown_course_uses_code_and_name_as_folder():
    rules = load_rules(RULES_YAML)
    course = Course(org_unit_id="200", code="62755", name="Power Electronics")
    t = topic(course_code="62755", module_path=("Lecture 1",), filename="intro.pdf")

    assert rules.path_for(t, course) == PurePosixPath(
        "Obsidian/Courses/62755 Power Electronics/_Learn/Lecture 1/intro.pdf"
    )


def test_is_known_reports_missing_course():
    rules = load_rules(RULES_YAML)

    assert rules.is_known("34870") is True
    assert rules.is_known("62755") is False


def test_module_path_is_sanitised_for_the_filesystem():
    rules = load_rules(RULES_YAML)
    t = topic(module_path=('Week 3: "intro" / basics',), filename="a.txt")

    assert rules.path_for(t, COURSE) == PurePosixPath(
        "Obsidian/Courses/34870 Electroacoustics/_Learn/Week 3 - intro - basics/a.txt"
    )


def test_filename_is_sanitised_for_the_filesystem():
    rules = load_rules(RULES_YAML)
    t = topic(module_path=("Week 1",), filename='slides: part 1?.txt')

    assert rules.path_for(t, COURSE).name == "slides - part 1.txt"


@pytest.mark.parametrize(
    "taken, expected",
    [
        (set(), "dir/a.pdf"),
        ({"dir/a.pdf"}, "dir/a (2).pdf"),
        ({"dir/a.pdf", "dir/a (2).pdf"}, "dir/a (3).pdf"),
    ],
)
def test_resolve_collision_suffixes_until_free(taken, expected):
    result = resolve_collision(PurePosixPath("dir/a.pdf"), {PurePosixPath(p) for p in taken})

    assert result == PurePosixPath(expected)


def test_semesters_are_read_from_the_rules_file():
    rules = load_rules('semesters: [e26, f27]\ncourses: {}\n')

    assert rules.semesters == ["e26", "f27"]


def test_missing_semesters_key_means_no_filter():
    rules = load_rules("courses: {}\n")

    assert rules.semesters is None
