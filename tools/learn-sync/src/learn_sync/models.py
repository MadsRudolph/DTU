"""Data structures passed between collectors, filing, notes and delivery.

These are plain holders with no behaviour. Collectors build them from
Brightspace, everything downstream consumes them.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Course:
    """One enrolled course on DTU Learn."""

    org_unit_id: str
    code: str
    name: str


@dataclass(frozen=True)
class Topic:
    """A single downloadable item inside a course's content tree."""

    topic_id: str
    course_code: str
    module_path: tuple[str, ...]
    title: str
    filename: str
    download_url: str
    revision: str

    @property
    def module(self) -> str:
        """Module path joined for display and for rule matching."""
        return "/".join(self.module_path)


@dataclass(frozen=True)
class Announcement:
    """A news post on a course's announcement page."""

    announcement_id: str
    course_code: str
    posted_at: datetime
    title: str
    body_markdown: str


@dataclass(frozen=True)
class Event:
    """A calendar entry: an assignment deadline, a lecture, or anything else."""

    event_id: str
    course_code: str
    title: str
    starts_at: datetime
    kind: str = "other"


@dataclass
class RunReport:
    """What one sync run did, used to build the commit message and the Discord post."""

    files_added: list[tuple[str, str]] = field(default_factory=list)
    # Files already present in the vault that this run claimed. They are not news
    # to the reader, but Drive may never have seen them, so delivery still cares.
    files_adopted: list[tuple[str, str]] = field(default_factory=list)
    announcements: list[Announcement] = field(default_factory=list)
    events: list[Event] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_empty(self) -> bool:
        return not (self.files_added or self.announcements or self.events)
