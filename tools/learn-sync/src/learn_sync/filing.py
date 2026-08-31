"""Decide where a Brightspace topic lands in the vault.

Pure: no filesystem, no network. Given a topic, a course and the loaded rules,
`Rules.path_for` returns a repo-relative path. Every file lands in exactly one
place -- there is no mirror-plus-copy duplication.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePosixPath

import yaml

COURSES_ROOT = PurePosixPath("Obsidian/Courses")
DEFAULT_TARGET = "_Learn/{module}/"

# Characters that carry no meaning in a filename and are simply dropped.
_DROP = str.maketrans("", "", '"?*|')
# Characters that separate ideas and become a readable " - ".
_SEPARATORS = re.compile(r"[:/\\<>]")
_WHITESPACE = re.compile(r"\s+")


def sanitise(name: str) -> str:
    """Make a Brightspace module or file name safe for the filesystem.

    Glob and quote characters are dropped; structural punctuation becomes " - ".
    Existing hyphens are left alone so "Lecture-1.pdf" survives intact.
    """
    cleaned = _SEPARATORS.sub(" - ", name.translate(_DROP))
    cleaned = _WHITESPACE.sub(" ", cleaned)
    return cleaned.strip(" -")


@dataclass(frozen=True)
class Rule:
    """One filing rule. A rule with both patterns requires both to match."""

    to: str
    module: re.Pattern[str] | None = None
    file: re.Pattern[str] | None = None

    def matches(self, module: str, filename: str) -> bool:
        if self.module is not None and not self.module.search(module):
            return False
        if self.file is not None and not self.file.search(filename):
            return False
        # A rule with neither pattern would match everything; treat it as inert.
        return self.module is not None or self.file is not None


@dataclass(frozen=True)
class CourseRules:
    vault: str
    rules: tuple[Rule, ...]
    default: str

    def target_for(self, module: str, filename: str) -> str:
        for rule in self.rules:
            if rule.matches(module, filename):
                return rule.to
        return self.default


class Rules:
    """All per-course filing rules, keyed by DTU course code."""

    def __init__(self, courses: dict[str, CourseRules], semesters=None) -> None:
        self._courses = courses
        # Which DTU semester tokens ("e26") to sync. None means every course.
        self.semesters = semesters

    def is_known(self, course_code: str) -> bool:
        return course_code in self._courses

    def vault_folder(self, course) -> str:
        known = self._courses.get(course.code)
        return known.vault if known else f"{course.code} {course.name}"

    def path_for(self, topic, course) -> PurePosixPath:
        known = self._courses.get(course.code)
        target = (
            known.target_for(topic.module, topic.filename)
            if known
            else DEFAULT_TARGET
        )
        module_dirs = "/".join(sanitise(part) for part in topic.module_path)
        target = target.format(module=module_dirs).strip("/")

        path = COURSES_ROOT / self.vault_folder(course)
        if target:
            path = path / target
        return path / sanitise(topic.filename)


def load_rules(text: str) -> Rules:
    """Parse rules.yaml into a Rules object."""
    raw = yaml.safe_load(text) or {}
    courses: dict[str, CourseRules] = {}

    for code, spec in (raw.get("courses") or {}).items():
        rules = tuple(
            Rule(
                to=entry["to"],
                module=re.compile(entry["module"]) if "module" in entry else None,
                file=re.compile(entry["file"]) if "file" in entry else None,
            )
            for entry in (spec.get("rules") or [])
        )
        courses[str(code)] = CourseRules(
            vault=spec["vault"],
            rules=rules,
            default=spec.get("default", DEFAULT_TARGET),
        )

    return Rules(courses, semesters=raw.get("semesters"))


def resolve_collision(path: PurePosixPath, taken: set[PurePosixPath]) -> PurePosixPath:
    """Return `path`, or the first free " (n)" variant of it.

    Overwriting a different topic's file is never acceptable, so a clash is
    resolved by suffixing rather than replacing.
    """
    if path not in taken:
        return path

    counter = 2
    while True:
        candidate = path.with_name(f"{path.stem} ({counter}){path.suffix}")
        if candidate not in taken:
            return candidate
        counter += 1
