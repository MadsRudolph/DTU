import pytest

from learn_sync.filing import load_rules
from learn_sync.models import Course, Topic
from learn_sync.state import State
from learn_sync.sync import Sync

RULES = load_rules(
    """
courses:
  "34870":
    vault: "34870 Electroacoustics"
    rules:
      - {file: "(?i)lecture.*pdf$", to: "Slides/"}
    default: "_Learn/{module}/"
"""
)

COURSE = Course(org_unit_id="123", code="34870", name="Electroacoustics")
UNKNOWN = Course(org_unit_id="999", code="34871", name="Nonlinear Transducers")


def topic(topic_id="1", filename="Lecture 1.pdf", revision="a", module=("Week 1",)) -> Topic:
    return Topic(
        topic_id=topic_id,
        course_code="34870",
        module_path=module,
        title=filename,
        filename=filename,
        download_url=f"https://example/{topic_id}",
        revision=revision,
    )


class Downloader:
    """Records what was fetched and serves canned bytes."""

    def __init__(self, content=b"pdf-bytes", fail_for=()):
        self.content = content
        self.fail_for = set(fail_for)
        self.fetched = []

    def __call__(self, t: Topic) -> bytes:
        self.fetched.append(t.topic_id)
        if t.topic_id in self.fail_for:
            raise ConnectionError("download failed")
        return self.content if isinstance(self.content, bytes) else self.content[t.topic_id]


@pytest.fixture
def sync(tmp_path):
    return Sync(rules=RULES, state=State.empty(), repo_root=tmp_path,
                download=Downloader())


def test_new_topic_is_written_to_its_filed_path(tmp_path, sync):
    sync.process(COURSE, [topic()])

    written = tmp_path / "Obsidian/Courses/34870 Electroacoustics/Slides/Lecture 1.pdf"
    assert written.read_bytes() == b"pdf-bytes"


def test_written_file_is_recorded_in_the_report(sync):
    sync.process(COURSE, [topic()])

    assert sync.report.files_added == [
        ("34870", "Obsidian/Courses/34870 Electroacoustics/Slides/Lecture 1.pdf")
    ]


def test_unchanged_topic_is_not_downloaded_again(tmp_path):
    downloader = Downloader()
    state = State.empty()
    state.record(topic(), sha256="x", vault_path="whatever")
    s = Sync(rules=RULES, state=state, repo_root=tmp_path, download=downloader)

    s.process(COURSE, [topic(revision="a")])

    assert downloader.fetched == []
    assert s.report.files_added == []


def test_reupload_of_identical_bytes_is_downloaded_but_not_rewritten(tmp_path):
    """New revision, same content: we must fetch to know, but not churn the vault."""
    import hashlib

    digest = hashlib.sha256(b"pdf-bytes").hexdigest()
    state = State.empty()
    state.record(topic(revision="a"), sha256=digest, vault_path="Obsidian/x.pdf")
    downloader = Downloader()
    s = Sync(rules=RULES, state=state, repo_root=tmp_path, download=downloader)

    s.process(COURSE, [topic(revision="b")])

    assert downloader.fetched == ["1"]
    assert s.report.files_added == []


def test_two_topics_landing_on_one_path_do_not_overwrite_each_other(tmp_path, sync):
    sync.process(COURSE, [topic("1"), topic("2")])

    base = tmp_path / "Obsidian/Courses/34870 Electroacoustics/Slides"
    assert (base / "Lecture 1.pdf").exists()
    assert (base / "Lecture 1 (2).pdf").exists()
    assert "collision" in " ".join(sync.report.warnings).lower()


def test_unknown_course_is_filed_under_learn_and_warned_about(tmp_path, sync):
    t = Topic("9", "34871", ("Module A",), "n.pdf", "n.pdf", "https://e/9", "a")

    sync.process(UNKNOWN, [t])

    assert (tmp_path / "Obsidian/Courses/34871 Nonlinear Transducers/_Learn/Module A/n.pdf").exists()
    assert any("34871" in w for w in sync.report.warnings)


def test_failed_download_is_skipped_and_warned_without_poisoning_state(tmp_path):
    downloader = Downloader(fail_for=["1"])
    state = State.empty()
    s = Sync(rules=RULES, state=state, repo_root=tmp_path, download=downloader)

    s.process(COURSE, [topic("1"), topic("2", filename="Lecture 2.pdf")])

    # The good file still landed.
    assert (tmp_path / "Obsidian/Courses/34870 Electroacoustics/Slides/Lecture 2.pdf").exists()
    assert any("Lecture 1.pdf" in w for w in s.report.warnings)
    # The failed one must be retried next run.
    assert state.needs_download(topic("1")) is True


def test_successful_topic_is_recorded_in_state(tmp_path, sync):
    sync.process(COURSE, [topic()])

    assert sync.state.needs_download(topic(revision="a")) is False
    assert sync.state.vault_path_for("1").endswith("Slides/Lecture 1.pdf")


def test_parent_directories_are_created(tmp_path, sync):
    sync.process(COURSE, [topic(module=("Deep", "Nested"), filename="x.txt")])

    assert (tmp_path / "Obsidian/Courses/34870 Electroacoustics/_Learn/Deep/Nested/x.txt").exists()


def test_dry_run_downloads_nothing_and_writes_nothing(tmp_path):
    downloader = Downloader()
    s = Sync(rules=RULES, state=State.empty(), repo_root=tmp_path,
             download=downloader, dry_run=True)

    s.process(COURSE, [topic()])

    assert downloader.fetched == []
    assert not (tmp_path / "Obsidian").exists()
    # It still reports what it would have done.
    assert len(s.report.files_added) == 1
