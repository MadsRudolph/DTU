"""Sync bookkeeping: what has been downloaded, and at which revision.

The state file is committed to git alongside the vault, so any machine can see
what the sync believes it has done and a rebuilt container resumes instead of
re-downloading everything. That makes a stable on-disk layout part of the
contract -- see `test_saved_file_is_stable_json_with_schema`.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA = 1


class State:
    def __init__(self, topics: dict[str, dict[str, Any]], announcements: dict[str, str]) -> None:
        self._topics = topics
        self._announcements = announcements

    @classmethod
    def empty(cls) -> "State":
        return cls(topics={}, announcements={})

    @classmethod
    def load(cls, path: Path) -> "State":
        """Load state, or start fresh if this is the first run."""
        try:
            raw = json.loads(Path(path).read_text(encoding="utf-8"))
        except FileNotFoundError:
            return cls.empty()
        return cls(
            topics=raw.get("topics") or {},
            announcements=raw.get("announcements") or {},
        )

    def save(self, path: Path) -> None:
        payload = {
            "schema": SCHEMA,
            "topics": self._topics,
            "announcements": self._announcements,
        }
        Path(path).write_text(
            json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def needs_download(self, topic) -> bool:
        known = self._topics.get(topic.topic_id)
        return known is None or known.get("revision") != topic.revision

    def content_unchanged(self, topic, sha256: str) -> bool:
        """True when the bytes match what we already hold, despite a new revision."""
        known = self._topics.get(topic.topic_id)
        return known is not None and known.get("sha256") == sha256

    def record(self, topic, sha256: str, vault_path: str) -> None:
        self._topics[topic.topic_id] = {
            "revision": topic.revision,
            "sha256": sha256,
            "vault_path": vault_path,
            "synced_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        }

    def vault_path_for(self, topic_id: str) -> str | None:
        known = self._topics.get(topic_id)
        return known.get("vault_path") if known else None

    def known_vault_paths(self) -> set[str]:
        """Every path the sync has already written, for collision detection."""
        return {
            entry["vault_path"]
            for entry in self._topics.values()
            if entry.get("vault_path")
        }

    def newest_announcement(self, course_code: str) -> str | None:
        return self._announcements.get(course_code)

    def set_newest_announcement(self, course_code: str, announcement_id: str) -> None:
        self._announcements[course_code] = announcement_id
