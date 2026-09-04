"""Getting an authenticated DTU Learn session.

learn.inside.dtu.dk sits behind on-prem Microsoft ADFS at sts.ait.dtu.dk, which
serves a plain HTML form (username@dtu.dk + password) and SAML-POSTs back to
Brightspace. So a stored browser session is enough, and a password is only
needed to refresh it unattended.

`classify_landing` is deliberately pure: deciding "did we get in, and if not,
why not" is the part that must never be guessed at, so it is tested directly.
"""

from __future__ import annotations

import enum
import logging
import re
from pathlib import Path

log = logging.getLogger(__name__)

LEARN_HOST = "learn.inside.dtu.dk"
ADFS_HOST = "sts.ait.dtu.dk"
LEARN_HOME = f"https://{LEARN_HOST}/d2l/home"

# DTU serves ADFS in Danish, so every pattern needs both languages. English-only
# matching classified "Forkert bruger-id eller adgangskode" as a plain expired
# session, which sent the wrong instruction to Discord.
_MFA = re.compile(
    r"authenticator|two-factor|2-factor|verification code|approve the sign-in"
    r"|additional information|multi-factor"
    r"|godkendelsesapp|godkend anmodningen|tofaktor|to-faktor|bekræftelseskode",
    re.IGNORECASE,
)
_BAD_CREDENTIALS = re.compile(
    r"incorrect user id or password|invalid username or password"
    r"|forkert bruger-?id|forkert adgangskode|ugyldigt brugernavn",
    re.IGNORECASE,
)
_EXPIRED = re.compile(
    r"password has expired|must change your password"
    r"|adgangskode er udløbet|skal ændre adgangskoden",
    re.IGNORECASE,
)


class Landing(enum.Enum):
    """Where we ended up after trying to reach Learn."""

    OK = "ok"
    NEEDS_LOGIN = "needs_login"
    MFA = "mfa"
    BAD_CREDENTIALS = "bad_credentials"
    PASSWORD_EXPIRED = "password_expired"
    UNEXPECTED = "unexpected"


class AuthFailed(RuntimeError):
    def __init__(self, landing: Landing, url: str, title: str) -> None:
        super().__init__(f"{landing.value} at {url} ({title})")
        self.landing = landing
        self.url = url
        self.title = title


def classify_landing(url: str, page_text: str) -> Landing:
    """Decide what the page we landed on means.

    Checked most-specific first: an MFA prompt rendered inside the ADFS form
    must report MFA, not a generic "session dead".
    """
    if _MFA.search(page_text):
        return Landing.MFA
    if _EXPIRED.search(page_text):
        return Landing.PASSWORD_EXPIRED
    if _BAD_CREDENTIALS.search(page_text):
        return Landing.BAD_CREDENTIALS

    if ADFS_HOST in url:
        return Landing.NEEDS_LOGIN
    if LEARN_HOST in url:
        return Landing.NEEDS_LOGIN if "/d2l/login" in url else Landing.OK

    return Landing.UNEXPECTED


# --- Playwright driver --------------------------------------------------------


def open_session(playwright, storage_state: Path, headless: bool = True):
    """Open a browser context, reusing a saved session when one exists."""
    browser = playwright.chromium.launch(headless=headless)
    state = str(storage_state) if Path(storage_state).exists() else None
    context = browser.new_context(storage_state=state)
    return browser, context


def ensure_authenticated(context, storage_state: Path, username: str = "",
                         password: str = "") -> None:
    """Make `context` an authenticated Learn session, or raise AuthFailed.

    Tries the stored session first and only touches the login form when it has
    actually expired, so a healthy session generates no login traffic at all.
    """
    page = context.new_page()
    try:
        page.goto(LEARN_HOME, wait_until="domcontentloaded")
        landing = classify_landing(page.url, page.inner_text("body"))

        if landing is Landing.OK:
            log.info("stored session still valid")
            return

        if landing is not Landing.NEEDS_LOGIN:
            raise AuthFailed(landing, page.url, page.title())

        if not (username and password):
            raise AuthFailed(Landing.NEEDS_LOGIN, page.url, page.title())

        submit_adfs_form(page, username, password)

        landing = classify_landing(page.url, page.inner_text("body"))
        if landing is not Landing.OK:
            raise AuthFailed(landing, page.url, page.title())

        context.storage_state(path=str(storage_state))
        log.info("refreshed session via ADFS")
    finally:
        page.close()


# Selectors verified against the live sts.ait.dtu.dk form. The submit control is
# a <span id="submitButton" role="button" onclick="Login.submitLoginRequest()">,
# NOT an input or button element -- selecting input[type=submit] simply timed out
# after 30s and killed the run.
USERNAME_FIELD = "#userNameInput, input[name='UserName']"
PASSWORD_FIELD = "#passwordInput, input[name='Password']"
SUBMIT_BUTTON = "#submitButton, span[role=button].submit"


def submit_adfs_form(page, username: str, password: str) -> None:
    """Fill the ADFS form and wait for the SAML round-trip to settle on Learn.

    Every failure becomes AuthFailed. Letting a raw Playwright TimeoutError
    escape meant the caller never sent the Discord alert nor wrote the status
    file -- the sync just died silently, which is the one outcome the design is
    supposed to make impossible.
    """
    try:
        page.fill(USERNAME_FIELD, username)
        page.fill(PASSWORD_FIELD, password)
        page.click(SUBMIT_BUTTON)
        page.wait_for_load_state("networkidle")
    except AuthFailed:
        raise
    except Exception as exc:
        raise AuthFailed(
            Landing.UNEXPECTED,
            getattr(page, "url", "unknown"),
            f"ADFS login form did not behave as expected: {exc}",
        ) from exc
