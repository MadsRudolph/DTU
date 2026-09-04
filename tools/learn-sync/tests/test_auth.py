import pytest

from learn_sync.auth import Landing, classify_landing

LEARN = "https://learn.inside.dtu.dk/d2l/home"
ADFS = "https://sts.ait.dtu.dk/adfs/ls/?SAMLRequest=abc"


def test_landing_on_the_dashboard_is_a_good_session():
    assert classify_landing(LEARN, "My Home") is Landing.OK


def test_landing_on_any_learn_page_is_a_good_session():
    assert classify_landing("https://learn.inside.dtu.dk/d2l/le/content/123/Home",
                            "Content") is Landing.OK


def test_still_on_adfs_means_the_session_is_dead():
    assert classify_landing(ADFS, "Sign In") is Landing.NEEDS_LOGIN


def test_learn_login_page_means_the_session_is_dead():
    assert classify_landing("https://learn.inside.dtu.dk/d2l/login?noredirect=1",
                            "Login") is Landing.NEEDS_LOGIN


@pytest.mark.parametrize(
    "text",
    [
        "Enter the code from your authenticator app",
        "Approve the sign-in request",
        "Two-factor verification required",
        "For security reasons, we require additional information",
    ],
)
def test_an_mfa_challenge_is_recognised(text):
    assert classify_landing(ADFS, text) is Landing.MFA


def test_bad_credentials_are_distinguished_from_mfa():
    assert classify_landing(
        ADFS, "Incorrect user ID or password. Type the correct user ID and password."
    ) is Landing.BAD_CREDENTIALS


def test_password_expiry_is_called_out():
    assert classify_landing(ADFS, "Your password has expired") is Landing.PASSWORD_EXPIRED


def test_somewhere_entirely_unexpected_is_its_own_outcome():
    assert classify_landing("https://example.com/whoops", "Nope") is Landing.UNEXPECTED


def test_mfa_wins_over_a_generic_login_page():
    """A page that is both an ADFS form and an MFA prompt must report MFA."""
    assert classify_landing(ADFS, "Sign In\nEnter the code from your authenticator app") is Landing.MFA


# --- the ADFS login form ------------------------------------------------------


class FakePage:
    """Enough of a Playwright page to exercise the ADFS form filling."""

    def __init__(self, fail_on=None, known=()):
        self.fail_on = fail_on
        self.known = set(known)
        self.filled = {}
        self.clicked = []
        self.url = "https://learn.inside.dtu.dk/d2l/home"

    def _check(self, selector):
        if self.fail_on and self.fail_on in selector:
            raise RuntimeError(f"Timeout 30000ms exceeded waiting for {selector}")

    def fill(self, selector, value):
        self._check(selector)
        self.filled[selector] = value

    def click(self, selector, **kw):
        self._check(selector)
        self.clicked.append(selector)

    def wait_for_load_state(self, *a, **kw):
        pass

    def title(self):
        return "Sign In"


def test_login_fills_the_adfs_username_and_password_fields():
    from learn_sync.auth import submit_adfs_form

    page = FakePage()
    submit_adfs_form(page, "s000000@dtu.dk", "secret")

    assert "s000000@dtu.dk" in page.filled.values()
    assert "secret" in page.filled.values()


def test_login_clicks_the_span_submit_button():
    """ADFS renders <span id="submitButton" role="button">, not an <input>.

    Selecting input[type=submit] timed out after 30s and the run died.
    """
    from learn_sync.auth import submit_adfs_form

    page = FakePage()
    submit_adfs_form(page, "u", "p")

    assert any("submitButton" in c for c in page.clicked)


def test_a_broken_login_form_becomes_authfailed_not_a_raw_error():
    """An unhandled error here skipped the Discord alert and the status file."""
    from learn_sync.auth import AuthFailed, submit_adfs_form

    page = FakePage(fail_on="submitButton")

    try:
        submit_adfs_form(page, "u", "p")
    except AuthFailed as exc:
        assert exc.landing is Landing.UNEXPECTED
    else:
        raise AssertionError("expected AuthFailed")
