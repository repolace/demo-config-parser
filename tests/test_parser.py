import pytest

from src.parser import parse_file, parse_line, parse_text


def test_a_simple_pair():
    assert parse_line("name = demo") == ("name", "demo")


def test_whitespace_around_the_equals_sign_is_ignored():
    assert parse_line("  name   =   demo  ") == ("name", "demo")


def test_blank_and_comment_lines_are_skipped():
    assert parse_line("") is None
    assert parse_line("   ") is None
    assert parse_line("# a comment") is None


def test_a_trailing_comment_is_removed_from_an_unquoted_value():
    assert parse_line("path = /srv/app   # where it lives") == ("path", "/srv/app")


def test_quotes_around_a_value_are_removed():
    assert parse_line('greeting = "hello, world"') == ("greeting", "hello, world")


def test_a_later_key_replaces_an_earlier_one(tmp_path):
    path = tmp_path / "app.conf"
    path.write_text("name = first\nname = second\n")

    assert parse_file(path) == {"name": "second"}


def test_a_line_without_an_equals_sign_is_an_error():
    with pytest.raises(ValueError):
        parse_text("just words")


def test_a_hash_inside_a_quoted_value_is_not_a_comment():
    assert parse_line('url = "http://example.com/docs#intro"') == ("url", "http://example.com/docs#intro")
