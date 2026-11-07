"""A tiny parser for `KEY = VALUE` settings files.

Supported syntax:

    # a comment line
    name = demo
    greeting = "hello, world"      # a trailing comment
    path = /srv/app
"""

from pathlib import Path


def _strip_inline_comment(value):
    in_quote = False
    quote_char = None
    
    for i, char in enumerate(value):
        if char in ('"', "'"):
            if not in_quote:
                in_quote = True
                quote_char = char
            elif quote_char == char:
                in_quote = False
                quote_char = None
        elif char == '#':
            if not in_quote:
                if i == 0 or value[i-1].isspace():
                    return value[:i].strip()
    return value.strip()


def _unquote(value):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def parse_line(line):
    """Return `(key, value)` for a settings line, or None for a blank or comment line."""
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    key, separator, value = stripped.partition("=")
    if not separator:
        raise ValueError(f"expected KEY = VALUE, got: {line!r}")
    return key.strip(), _unquote(_strip_inline_comment(value))


def parse_text(text):
    """Parse a whole settings file into a dict. A later key replaces an earlier one."""
    settings = {}
    for line in text.splitlines():
        parsed = parse_line(line)
        if parsed is not None:
            key, value = parsed
            settings[key] = value
    return settings


def parse_file(path):
    return parse_text(Path(path).read_text(encoding="utf-8"))
