"""TOC parsing, against the real /d2l/api/le/1.67/{ou}/content/toc shape.

Captured from 34870 on 2026-08-31. Note there is no top-level "Topics" key --
everything hangs off "Modules" -- and Link topics carry a Url just like File
topics do, so TypeIdentifier is the only safe discriminator.
"""

from learn_sync.collectors.content import parse_toc
from learn_sync.models import Course

COURSE = Course(org_unit_id="325536", code="34870", name="Electroacoustics")

ENFORCED = "/content/enforced/325536-DTU_e26_34870"


def topic(topic_id, title, url, type_id="File", **kw):
    payload = {
        "TopicId": topic_id,
        "Identifier": str(topic_id),
        "TypeIdentifier": type_id,
        "Title": title,
        "Url": url,
        "LastModifiedDate": "2026-08-20T12:46:46.053Z",
        "IsHidden": False,
        "IsBroken": False,
    }
    payload.update(kw)
    return payload


TOC = {
    "Modules": [
        {
            "ModuleId": 1241922,
            "Title": "Basic Material",
            "Modules": [],
            "Topics": [
                topic(1248761, "34870 Course plan Fall 2026",
                      f"{ENFORCED}/Basic Material/34870 Course plan Fall2026.pdf"),
            ],
        },
        {
            "ModuleId": 1241923,
            "Title": "Lecture 1 - Analogies Introduction",
            "Modules": [
                {
                    "ModuleId": 1241924,
                    "Title": "Extra",
                    "Modules": [],
                    "Topics": [
                        topic(1248770, "Bonus", f"{ENFORCED}/Lecture 1/bonus.pdf")
                    ],
                }
            ],
            "Topics": [
                topic(1248765, "34870_Lecture1_31082026",
                      f"{ENFORCED}/Lecture 1/34870_Lecture1_31082026.pdf"),
                topic(1248767, "Lecture 1: Analogies",
                      "https://panopto.dtu.dk/watch?id=abc", type_id="Link"),
            ],
        },
    ]
}


def test_file_topics_become_topics():
    topics = parse_toc(TOC, COURSE)

    assert "1248761" in {t.topic_id for t in topics}


def test_link_topics_are_skipped_even_though_they_have_a_url():
    """A Link topic points at Panopto or a website; there is no file to fetch."""
    assert "1248767" not in {t.topic_id for t in parse_toc(TOC, COURSE)}


def test_nested_modules_build_the_module_path():
    nested = next(t for t in parse_toc(TOC, COURSE) if t.topic_id == "1248770")

    assert nested.module_path == ("Lecture 1 - Analogies Introduction", "Extra")


def test_top_level_module_is_the_whole_path_for_its_own_topics():
    plan = next(t for t in parse_toc(TOC, COURSE) if t.topic_id == "1248761")

    assert plan.module_path == ("Basic Material",)


def test_filename_comes_from_the_url_not_the_title():
    """The title is prose: '34870 Course plan Fall 2026' vs the real filename."""
    plan = next(t for t in parse_toc(TOC, COURSE) if t.topic_id == "1248761")

    assert plan.filename == "34870 Course plan Fall2026.pdf"
    assert plan.title == "34870 Course plan Fall 2026"


def test_revision_uses_the_last_modified_date():
    plan = next(t for t in parse_toc(TOC, COURSE) if t.topic_id == "1248761")

    assert plan.revision == "2026-08-20T12:46:46.053Z"


def test_download_url_uses_the_topic_download_endpoint():
    plan = next(t for t in parse_toc(TOC, COURSE) if t.topic_id == "1248761")

    assert plan.download_url == (
        "https://learn.inside.dtu.dk/d2l/le/content/325536/topics/files/download/"
        "1248761/DirectFileTopicDownload"
    )


def test_broken_topics_are_skipped():
    toc = {"Modules": [{"Title": "M", "Modules": [], "Topics": [
        topic(1, "gone", f"{ENFORCED}/gone.pdf", IsBroken=True)
    ]}]}

    assert parse_toc(toc, COURSE) == []


def test_hidden_topics_are_skipped():
    toc = {"Modules": [{"Title": "M", "Modules": [], "Topics": [
        topic(1, "draft", f"{ENFORCED}/draft.pdf", IsHidden=True)
    ]}]}

    assert parse_toc(toc, COURSE) == []


def test_url_encoded_filenames_are_decoded():
    toc = {"Modules": [{"Title": "M", "Modules": [], "Topics": [
        topic(1, "t", f"{ENFORCED}/uge%201%20noter.pdf")
    ]}]}

    assert parse_toc(toc, COURSE)[0].filename == "uge 1 noter.pdf"


def test_every_topic_carries_the_course_code():
    assert {t.course_code for t in parse_toc(TOC, COURSE)} == {"34870"}


def test_a_toc_with_no_modules_yields_nothing():
    assert parse_toc({"Modules": []}, COURSE) == []
