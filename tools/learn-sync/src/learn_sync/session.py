"""HTTP against DTU Learn, reusing the authenticated browser context.

Playwright's request context shares cookies with the browser, so this is the
same session the login produced -- no cookie copying, no second auth path.

Every call goes through `_wait`, which keeps the run looking like a person
clicking around rather than a crawler.
"""

from __future__ import annotations

import logging
import time

LEARN_BASE = "https://learn.inside.dtu.dk"
DELAY_SECONDS = 1.5

log = logging.getLogger(__name__)


class Session:
    def __init__(self, context, base: str = LEARN_BASE, delay: float = DELAY_SECONDS) -> None:
        self._request = context.request
        self._base = base
        self._delay = delay
        self._last_call = 0.0

    def _wait(self) -> None:
        elapsed = time.monotonic() - self._last_call
        if elapsed < self._delay:
            time.sleep(self._delay - elapsed)
        self._last_call = time.monotonic()

    def _url(self, path: str) -> str:
        return path if path.startswith("http") else f"{self._base}{path}"

    def get_text(self, path: str) -> str:
        self._wait()
        response = self._request.get(self._url(path))
        log.debug("GET %s -> %s", path, response.status)
        return response.text()

    def get_json(self, path: str):
        """Return parsed JSON, or None if the endpoint did not serve JSON."""
        self._wait()
        response = self._request.get(self._url(path))
        log.debug("GET %s -> %s", path, response.status)
        if not response.ok:
            return None
        try:
            return response.json()
        except Exception:
            return None

    def download(self, url: str) -> bytes:
        self._wait()
        response = self._request.get(self._url(url))
        if not response.ok:
            raise IOError(f"{response.status} fetching {url}")
        return response.body()
