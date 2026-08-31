"""Tests for turning a Brightspace table-of-contents payload into Topics.

The TOC shape here follows D2L's documented TableOfContents structure. It is
confirmed against a live response by the discovery run (`learn-sync discover`)
before this collector is trusted in production -- see fixtures/README.md.
"""

from learn_sync.collectors.content import parse_toc
from learn_sync.models import Course

COURSE = Course(org_unit_id="123", code="34870", name="Electroacoustics")

TOC = {
    "Modules": [
        {
            "ModuleId": 1,
            "Title": "Week 1",
            "Modules": [
                {
                    "ModuleId": 2,
                    "Title": "Extra reading",
                    "Modules": [],
                    "Topics": [
                        {
                            "TopicId": 20,
                            "Title": "Bonus paper",
                            "Url": "/content/enforced/123/bonus.pdf",
                            "LastModifiedDate": "2026-09-02T10:00:00.000Z",
                        }
                    ],
                }
            ],
            "Topics": [
                {
                    "TopicId": 10,
                    "Title": "Intro slides",
                    "Url": "/content/enforced/123/intro slides.pdf",
                    "LastModifiedDate": "2026-09-01T08:00:00.000Z",
                }
            ],
        }
    ],
    "Topics": [
        {
            "TopicId": 5,
            "Title": "Course plan",
            "Url": "/content/enforced/123/plan.pdf",
            "LastModifiedDate": "2026-08-30T08:00:00.000Z",
        }
    ],
}


def test_topics_at_the_root_have_an_empty_module_path():
    topics = parse_toc(TOC, COURSE)

    root = next(t for t in topics if t.topic_id == "5")
    assert root.module_path == ()
    assert root.title == "Course plan"


def test_nested_modules_build_the_module_path():
    topics = parse_toc(TOC, COURSE)

    nested = next(t for t in topics if t.topic_id == "20")
    assert nested.module_path == ("Week 1", "Extra reading")


def test_filename_comes_from_the_url_not_the_title():
    topics = parse_toc(TOC, COURSE)

    slides = next(t for t in topics if t.topic_id == "10")
    assert slides.filename == "intro slides.pdf"


def test_revision_uses_the_last_modified_date():
    topics = parse_toc(TOC, COURSE)

    slides = next(t for t in topics if t.topic_id == "10")
    assert slides.revision == "2026-09-01T08:00:00.000Z"


def test_every_topic_carries_the_course_code():
    topics = parse_toc(TOC, COURSE)

    assert {t.course_code for t in topics} == {"34870"}
    assert len(topics) == 3


def test_download_url_is_absolute_and_uses_the_topic_download_endpoint():
    topics = parse_toc(TOC, COURSE)

    slides = next(t for t in topics if t.topic_id == "10")
    assert slides.download_url == (
        "https://learn.inside.dtu.dk/d2l/le/content/123/topics/files/download/10/DirectFileTopicDownload"
    )


def test_link_topics_without_a_file_url_are_skipped():
    """Brightspace mixes weblinks into the TOC; there is nothing to download."""
    toc = {
        "Modules": [],
        "Topics": [
            {"TopicId": 7, "Title": "A weblink", "Url": "", "LastModifiedDate": "x"},
            {"TopicId": 8, "Title": "A file", "Url": "/content/enforced/1/f.pdf",
             "LastModifiedDate": "x"},
        ],
    }

    assert [t.topic_id for t in parse_toc(toc, COURSE)] == ["8"]


def test_url_encoded_filenames_are_decoded():
    toc = {
        "Modules": [],
        "Topics": [
            {"TopicId": 9, "Title": "t", "Url": "/content/enforced/1/uge%201%20noter.pdf",
             "LastModifiedDate": "x"},
        ],
    }

    assert parse_toc(toc, COURSE)[0].filename == "uge 1 noter.pdf"


def test_an_empty_toc_yields_nothing():
    assert parse_toc({"Modules": [], "Topics": []}, COURSE) == []
