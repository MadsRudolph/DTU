from learn_sync.collectors.courses import parse_courses

HTML = """
<html><body>
  <div class="d2l-my-courses">
    <a href="/d2l/home/6789">34870 Electroacoustics E26</a>
    <a href="/d2l/home/1234">62755 Power Electronics</a>
    <a href="/d2l/le/content/6789/Home">Content shortcut</a>
    <a href="/d2l/home/9999">Study Administration</a>
  </div>
</body></html>
"""


def test_course_links_become_courses():
    courses = parse_courses(HTML)

    assert {c.code for c in courses} == {"34870", "62755"}


def test_org_unit_id_comes_from_the_link():
    courses = parse_courses(HTML)

    electro = next(c for c in courses if c.code == "34870")
    assert electro.org_unit_id == "6789"


def test_course_name_drops_the_code_and_semester_suffix():
    courses = parse_courses(HTML)

    electro = next(c for c in courses if c.code == "34870")
    assert electro.name == "Electroacoustics"


def test_entries_without_a_course_code_are_ignored():
    """Brightspace lists admin org units alongside real courses."""
    assert all(c.code != "" for c in parse_courses(HTML))
    assert "Study Administration" not in {c.name for c in parse_courses(HTML)}


def test_non_home_links_are_ignored():
    assert len(parse_courses(HTML)) == 2


def test_the_same_course_listed_twice_appears_once():
    html = HTML.replace(
        "</div>", '<a href="/d2l/home/6789">34870 Electroacoustics E26</a></div>'
    )

    assert len([c for c in parse_courses(html) if c.code == "34870"]) == 1


def test_no_courses_found_is_empty_not_an_error():
    assert parse_courses("<html><body>nothing here</body></html>") == []
