"""Turn a Brightspace table of contents into downloadable Topics.

`parse_toc` is pure so the shape of the payload can be pinned down by tests and
corrected in one place. Run `learn-sync discover` to capture a real response
into fixtures/ and confirm the shape against a live course.
"""

from __future__ import annotations

from urllib.parse import unquote

from ..models import Course, Topic

LEARN_BASE = "https://learn.inside.dtu.dk"


def _download_url(org_unit_id: str, topic_id: str) -> str:
    return (
        f"{LEARN_BASE}/d2l/le/content/{org_unit_id}/topics/files/download/"
        f"{topic_id}/DirectFileTopicDownload"
    )


def _filename(url: str) -> str:
    """The stored filename, which is what the Url field carries; titles are prose."""
    return unquote(url.rsplit("/", 1)[-1])


def parse_toc(toc: dict, course: Course) -> list[Topic]:
    """Flatten the module tree into topics, carrying each one's module path."""
    topics: list[Topic] = []

    def walk(node: dict, path: tuple[str, ...]) -> None:
        for raw in node.get("Topics") or []:
            url = raw.get("Url") or ""
            # Weblinks and other non-file topics have nothing to download.
            if not url:
                continue
            topics.append(
                Topic(
                    topic_id=str(raw["TopicId"]),
                    course_code=course.code,
                    module_path=path,
                    title=raw.get("Title") or _filename(url),
                    filename=_filename(url),
                    download_url=_download_url(course.org_unit_id, str(raw["TopicId"])),
                    revision=str(raw.get("LastModifiedDate") or ""),
                )
            )

        for module in node.get("Modules") or []:
            walk(module, path + (module.get("Title") or "Untitled",))

    walk(toc, ())
    return topics
