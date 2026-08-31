from datetime import datetime

from learn_sync.models import Announcement, Event, RunReport
from learn_sync.notify import DiscordNotifier


class Recorder:
    """Stands in for the HTTP transport and remembers what was posted."""

    def __init__(self, fail=False):
        self.posts = []
        self.fail = fail

    def __call__(self, url, payload):
        if self.fail:
            raise ConnectionError("discord is down")
        self.posts.append((url, payload))

    @property
    def text(self) -> str:
        return "\n".join(str(payload) for _, payload in self.posts)


WEBHOOK = "https://discord.example/webhook"


def announcement(code="34870", title="Lecture moved") -> Announcement:
    return Announcement("1", code, datetime(2026, 9, 1), title, "Body text here")


def event(code="62755", title="Report 2") -> Event:
    return Event("1", code, title, datetime(2026, 10, 5), kind="assignment")


def test_nothing_is_sent_when_the_run_found_nothing():
    recorder = Recorder()
    DiscordNotifier(WEBHOOK, post=recorder).report(RunReport())

    assert recorder.posts == []


def test_new_files_are_grouped_by_course():
    recorder = Recorder()
    report = RunReport(
        files_added=[("34870", "Slides/L03.pdf"), ("34870", "Labs/A.pdf"),
                     ("62755", "Slides/L08.pdf")]
    )

    DiscordNotifier(WEBHOOK, post=recorder).report(report)

    assert len(recorder.posts) == 1
    body = recorder.text
    assert "34870" in body and "62755" in body
    assert "L03.pdf" in body and "A.pdf" in body


def test_announcements_and_deadlines_are_listed():
    recorder = Recorder()
    report = RunReport(announcements=[announcement()], events=[event()])

    DiscordNotifier(WEBHOOK, post=recorder).report(report)

    assert "Lecture moved" in recorder.text
    assert "Report 2" in recorder.text


def test_warnings_are_included():
    recorder = Recorder()
    report = RunReport(
        files_added=[("34870", "a.pdf")],
        warnings=["unknown course 34871, filed under _Learn"],
    )

    DiscordNotifier(WEBHOOK, post=recorder).report(report)

    assert "unknown course 34871" in recorder.text


def test_warnings_alone_are_still_worth_sending():
    recorder = Recorder()

    DiscordNotifier(WEBHOOK, post=recorder).report(RunReport(warnings=["heads up"]))

    assert len(recorder.posts) == 1


def test_alert_is_sent_even_with_nothing_else_to_report():
    recorder = Recorder()

    DiscordNotifier(WEBHOOK, post=recorder).alert("Re-auth needed", "session expired")

    assert len(recorder.posts) == 1
    assert "Re-auth needed" in recorder.text


def test_no_webhook_configured_is_a_silent_no_op():
    """The sync must run fine on a box with no Discord set up."""
    recorder = Recorder()

    DiscordNotifier("", post=recorder).alert("title", "detail")

    assert recorder.posts == []


def test_transport_failure_never_breaks_the_run():
    """A Discord outage must not fail an otherwise successful sync."""
    notifier = DiscordNotifier(WEBHOOK, post=Recorder(fail=True))

    notifier.report(RunReport(files_added=[("34870", "a.pdf")]))
    notifier.alert("title", "detail")


def test_a_webhook_without_a_scheme_is_treated_as_unconfigured(caplog):
    """A typo'd or placeholder URL must not look like working notifications."""
    recorder = Recorder()

    DiscordNotifier("PASTE_NEW_WEBHOOK", post=recorder).report(
        RunReport(files_added=[("34870", "a.pdf")])
    )

    assert recorder.posts == []
    assert "does not look like a URL" in caplog.text


def test_a_valid_webhook_logs_no_warning(caplog):
    recorder = Recorder()

    DiscordNotifier(WEBHOOK, post=recorder).report(
        RunReport(files_added=[("34870", "a.pdf")])
    )

    assert len(recorder.posts) == 1
    assert "does not look like a URL" not in caplog.text
