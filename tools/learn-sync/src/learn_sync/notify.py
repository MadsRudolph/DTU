"""Discord notification for what a run found.

Silent when there is nothing new -- the point is to be worth reading. A failure
to notify is never allowed to fail the run itself: the material is already
safely committed by the time we get here.
"""

from __future__ import annotations

import logging
from collections import defaultdict

log = logging.getLogger(__name__)

GREEN = 0x2ECC71
RED = 0xE74C3C
MAX_FIELD = 1024


def _post_via_requests(url: str, payload: dict) -> None:
    import requests

    requests.post(url, json=payload, timeout=15).raise_for_status()


def _clip(text: str) -> str:
    """Discord rejects fields over 1024 characters."""
    return text if len(text) <= MAX_FIELD else text[: MAX_FIELD - 4] + "\n..."


class DiscordNotifier:
    def __init__(self, webhook_url: str, post=_post_via_requests) -> None:
        # A placeholder or typo'd URL would otherwise look like working
        # notifications right up until the end of a run, when the post fails.
        if webhook_url and not webhook_url.startswith(("http://", "https://")):
            log.warning(
                "DISCORD_WEBHOOK_URL does not look like a URL (%r) — "
                "notifications are disabled for this run",
                webhook_url[:32],
            )
            webhook_url = ""

        self._url = webhook_url
        self._post = post

    def report(self, run) -> None:
        """Post a summary of the run, or stay quiet if it found nothing."""
        fields = []

        if run.files_added:
            by_course: dict[str, list[str]] = defaultdict(list)
            for course_code, path in run.files_added:
                by_course[course_code].append(path.rsplit("/", 1)[-1])
            for course_code, names in by_course.items():
                fields.append(
                    {
                        "name": f"{course_code} — {len(names)} new",
                        "value": _clip("\n".join(f"• {n}" for n in names)),
                    }
                )

        if run.announcements:
            fields.append(
                {
                    "name": "Announcements",
                    "value": _clip(
                        "\n".join(
                            f"• `{a.course_code}` {a.title}" for a in run.announcements
                        )
                    ),
                }
            )

        if run.events:
            fields.append(
                {
                    "name": "Deadlines",
                    "value": _clip(
                        "\n".join(
                            f"• {e.starts_at:%d %b} — `{e.course_code}` {e.title}"
                            for e in sorted(run.events, key=lambda e: e.starts_at)
                        )
                    ),
                }
            )

        if run.warnings:
            fields.append(
                {"name": "Warnings", "value": _clip("\n".join(f"• {w}" for w in run.warnings))}
            )

        if not fields:
            return

        self._send(
            {
                "embeds": [
                    {"title": "New on DTU Learn", "color": GREEN, "fields": fields}
                ]
            }
        )

    def alert(self, title: str, detail: str) -> None:
        """Always sent -- this is how a broken sync makes itself known."""
        self._send(
            {"embeds": [{"title": title, "description": _clip(detail), "color": RED}]}
        )

    def _send(self, payload: dict) -> None:
        if not self._url:
            return
        try:
            self._post(self._url, payload)
        except Exception:
            # The sync already succeeded; losing the notification is not fatal.
            log.exception("could not post to Discord")
