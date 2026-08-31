import json

from learn_sync.models import Topic
from learn_sync.state import State


def topic(topic_id="1", revision="a") -> Topic:
    return Topic(
        topic_id=topic_id,
        course_code="34870",
        module_path=("Week 1",),
        title="t",
        filename="handout.pdf",
        download_url="https://example/1",
        revision=revision,
    )


def test_unseen_topic_needs_download():
    state = State.empty()

    assert state.needs_download(topic()) is True


def test_topic_with_unchanged_revision_is_skipped():
    state = State.empty()
    state.record(topic(revision="a"), sha256="abc", vault_path="Obsidian/x.pdf")

    assert state.needs_download(topic(revision="a")) is False


def test_topic_with_new_revision_needs_download():
    state = State.empty()
    state.record(topic(revision="a"), sha256="abc", vault_path="Obsidian/x.pdf")

    assert state.needs_download(topic(revision="b")) is True


def test_reupload_with_identical_bytes_is_not_rewritten():
    """A lecturer re-uploading the same file bumps the revision but changes nothing."""
    state = State.empty()
    state.record(topic(revision="a"), sha256="abc", vault_path="Obsidian/x.pdf")

    assert state.content_unchanged(topic(revision="b"), sha256="abc") is True
    assert state.content_unchanged(topic(revision="b"), sha256="different") is False


def test_content_unchanged_is_false_for_unseen_topic():
    state = State.empty()

    assert state.content_unchanged(topic(), sha256="abc") is False


def test_record_stores_vault_path():
    state = State.empty()
    state.record(topic(), sha256="abc", vault_path="Obsidian/Courses/x/Slides/a.pdf")

    assert state.vault_path_for("1") == "Obsidian/Courses/x/Slides/a.pdf"


def test_announcement_watermark_round_trips():
    state = State.empty()

    assert state.newest_announcement("34870") is None

    state.set_newest_announcement("34870", "news-7")

    assert state.newest_announcement("34870") == "news-7"


def test_state_survives_save_and_load(tmp_path):
    path = tmp_path / "state.json"
    state = State.empty()
    state.record(topic(), sha256="abc", vault_path="Obsidian/x.pdf")
    state.set_newest_announcement("34870", "news-7")
    state.save(path)

    reloaded = State.load(path)

    assert reloaded.needs_download(topic(revision="a")) is False
    assert reloaded.newest_announcement("34870") == "news-7"
    assert reloaded.vault_path_for("1") == "Obsidian/x.pdf"


def test_load_of_missing_file_gives_empty_state(tmp_path):
    state = State.load(tmp_path / "absent.json")

    assert state.needs_download(topic()) is True


def test_saved_file_is_stable_json_with_schema(tmp_path):
    """The state file is committed to git, so its layout must not churn."""
    path = tmp_path / "state.json"
    state = State.empty()
    state.record(topic(), sha256="abc", vault_path="Obsidian/x.pdf")
    state.save(path)

    written = json.loads(path.read_text(encoding="utf-8"))

    assert written["schema"] == 1
    assert set(written["topics"]["1"]) == {"revision", "sha256", "vault_path", "synced_at"}
