"""The container must never rebuild the manifest.

drive-sync's own upload.py calls rebuild_manifest() after a successful upload,
which reconstructs the manifest from files present on local disk. The container
holds a partial checkout -- only the binaries learn-sync itself downloaded --
so that would truncate an 816-entry manifest to ~30 and push the result.

This uploader is therefore strictly additive: it appends entries for the files
it uploaded and never removes or rewrites an existing one.
"""

import json

import pytest

from learn_sync.drive import DriveUploader
from learn_sync.delivery import DriveSyncFailed

MANIFEST = {
    "version": 1,
    "description": "Large files stored in Google Drive",
    "drive_folder_id": "FOLDER",
    "files": [
        {"path": "Obsidian/old/a.pdf", "driveId": "id-a", "size": 10},
        {"path": "Obsidian/old/Løsning.pdf", "driveId": "id-b", "size": 20},
    ],
}


class FakeRclone:
    """Stands in for the rclone CLI."""

    def __init__(self, fail_for=()):
        self.uploaded = []
        self.fail_for = set(fail_for)
        self.id_calls = 0

    def copy(self, local, remote_dir):
        if local.name in self.fail_for:
            raise DriveSyncFailed(f"rclone failed for {local.name}")
        self.uploaded.append(local.name)

    def file_ids(self, rel_paths):
        """One lookup for the whole batch -- see test_ids_are_fetched_in_one_call."""
        self.id_calls += 1
        return {p: f"new-id-{p.rsplit('/', 1)[-1]}" for p in rel_paths}


@pytest.fixture
def repo(tmp_path):
    (tmp_path / "Obsidian/scripts/drive-sync").mkdir(parents=True)
    (tmp_path / "Obsidian/scripts/drive-sync/manifest.json").write_text(
        json.dumps(MANIFEST, indent=2), encoding="utf-8"
    )
    return tmp_path


def make(repo, rel, content=b"data"):
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content)
    return p


def read_manifest(repo):
    return json.loads(
        (repo / "Obsidian/scripts/drive-sync/manifest.json").read_text(encoding="utf-8")
    )


def test_a_new_file_is_uploaded_and_appended(repo):
    make(repo, "Obsidian/Courses/X/new.pdf")
    rclone = FakeRclone()

    DriveUploader(repo, rclone).upload(["Obsidian/Courses/X/new.pdf"])

    assert rclone.uploaded == ["new.pdf"]
    entry = next(e for e in read_manifest(repo)["files"] if e["path"].endswith("new.pdf"))
    assert entry["driveId"] == "new-id-new.pdf"
    assert entry["size"] == 4


def test_existing_entries_are_never_removed(repo):
    make(repo, "Obsidian/Courses/X/new.pdf")

    DriveUploader(repo, FakeRclone()).upload(["Obsidian/Courses/X/new.pdf"])

    paths = {e["path"] for e in read_manifest(repo)["files"]}
    assert "Obsidian/old/a.pdf" in paths
    assert "Obsidian/old/Løsning.pdf" in paths
    assert len(paths) == 3


def test_a_file_already_in_the_manifest_is_not_re_uploaded(repo):
    make(repo, "Obsidian/old/a.pdf")
    rclone = FakeRclone()

    DriveUploader(repo, rclone).upload(["Obsidian/old/a.pdf"])

    assert rclone.uploaded == []
    assert len(read_manifest(repo)["files"]) == 2


def test_danish_names_match_the_manifest_regardless_of_normalisation(repo):
    """NFD on disk must still match the NFC entry, or it uploads forever."""
    import unicodedata

    nfd = unicodedata.normalize("NFD", "Obsidian/old/Løsning.pdf")
    make(repo, nfd)
    rclone = FakeRclone()

    DriveUploader(repo, rclone).upload([nfd])

    assert rclone.uploaded == []


def test_top_level_manifest_keys_are_preserved(repo):
    make(repo, "Obsidian/Courses/X/new.pdf")

    DriveUploader(repo, FakeRclone()).upload(["Obsidian/Courses/X/new.pdf"])

    m = read_manifest(repo)
    assert m["version"] == 1
    assert m["drive_folder_id"] == "FOLDER"
    assert m["description"] == "Large files stored in Google Drive"


def test_entries_stay_sorted_by_path(repo):
    make(repo, "Obsidian/Courses/A/aaa.pdf")
    make(repo, "Obsidian/Courses/Z/zzz.pdf")

    DriveUploader(repo, FakeRclone()).upload(
        ["Obsidian/Courses/Z/zzz.pdf", "Obsidian/Courses/A/aaa.pdf"]
    )

    paths = [e["path"] for e in read_manifest(repo)["files"]]
    assert paths == sorted(paths)


def test_a_failed_upload_raises_and_leaves_the_manifest_alone(repo):
    make(repo, "Obsidian/Courses/X/bad.pdf")
    before = read_manifest(repo)

    with pytest.raises(DriveSyncFailed):
        DriveUploader(repo, FakeRclone(fail_for=["bad.pdf"])).upload(
            ["Obsidian/Courses/X/bad.pdf"]
        )

    assert read_manifest(repo) == before


def test_nothing_to_upload_touches_nothing(repo):
    rclone = FakeRclone()
    before = read_manifest(repo)

    DriveUploader(repo, rclone).upload([])

    assert rclone.uploaded == []
    assert read_manifest(repo) == before


def test_a_missing_local_file_is_skipped_rather_than_uploaded(repo):
    rclone = FakeRclone()

    DriveUploader(repo, rclone).upload(["Obsidian/Courses/X/absent.pdf"])

    assert rclone.uploaded == []
    assert len(read_manifest(repo)["files"]) == 2


def test_folder_id_is_read_from_the_manifest(repo):
    from learn_sync.drive import folder_id_from_manifest

    assert folder_id_from_manifest(repo) == "FOLDER"


def test_upload_covers_everything_state_knows_that_drive_does_not(repo):
    """Self-healing: a file recorded as synced but absent from the manifest.

    An aborted run leaves exactly that, and it would otherwise be stranded
    forever because no later run re-processes an already-recorded topic.
    """
    make(repo, "Obsidian/Courses/X/stranded.pdf")
    rclone = FakeRclone()

    DriveUploader(repo, rclone).upload(
        ["Obsidian/old/a.pdf", "Obsidian/Courses/X/stranded.pdf"]
    )

    assert rclone.uploaded == ["stranded.pdf"]


def test_ids_are_fetched_in_one_call_not_one_per_file(repo):
    """Each rclone invocation pays full auth cost; 30 files took 9 minutes."""
    for n in ("a", "b", "c"):
        make(repo, f"Obsidian/Courses/X/{n}.pdf")
    rclone = FakeRclone()

    DriveUploader(repo, rclone).upload(
        [f"Obsidian/Courses/X/{n}.pdf" for n in ("a", "b", "c")]
    )

    assert len(rclone.uploaded) == 3
    assert rclone.id_calls == 1
