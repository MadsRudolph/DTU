"""Turn a Brightspace table of contents into downloadable Topics.

Source: `/d2l/api/le/1.67/{orgUnitId}/content/toc`, confirmed against a live
course. The payload has no top-level "Topics" key -- everything hangs off
"Modules" -- and `Link` topics carry a `Url` exactly like `File` topics do, so
`TypeIdentifier` is the only safe way to tell a downloadable file from a link
out to Panopto or a website.
"""

from __future__ import annotations

from urllib.parse import unquote

from ..models import Course, Topic

LEARN_BASE = "https://learn.inside.dtu.dk"
TOC_PATH = "/d2l/api/le/1.67/{org_unit_id}/content/toc"
FILE_TYPE = "File"


def _download_url(org_unit_id: str, topic_id: str) -> str:
    return (
        f"{LEARN_BASE}/d2l/le/content/{org_unit_id}/topics/files/download/"
        f"{topic_id}/DirectFileTopicDownload"
    )


def _filename(url: str) -> str:
    """The stored filename. Titles are prose and often differ from the file."""
    return unquote(url.rsplit("/", 1)[-1])


def parse_toc(toc: dict, course: Course) -> list[Topic]:
    """Flatten the module tree into downloadable topics, carrying module paths."""
    topics: list[Topic] = []

    def walk(node: dict, path: tuple[str, ...]) -> None:
        for raw in node.get("Topics") or []:
            if raw.get("TypeIdentifier") != FILE_TYPE:
                continue
            if raw.get("IsBroken") or raw.get("IsHidden"):
                continue

            url = raw.get("Url") or ""
            if not url:
                continue

            topic_id = str(raw["TopicId"])
            topics.append(
                Topic(
                    topic_id=topic_id,
                    course_code=course.code,
                    module_path=path,
                    title=raw.get("Title") or _filename(url),
                    filename=_filename(url),
                    download_url=_download_url(course.org_unit_id, topic_id),
                    revision=str(raw.get("LastModifiedDate") or ""),
                )
            )

        for module in node.get("Modules") or []:
            if module.get("IsHidden"):
                continue
            walk(module, path + (module.get("Title") or "Untitled",))

    walk(toc, ())
    return topics
