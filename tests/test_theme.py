import os
import re

from ui.styles.theme import render_qss
from ui.styles.tokens import DARK_TOKENS, LIGHT_TOKENS

PLACEHOLDER_PATTERN = re.compile(r"@(color|icon)_[a-zA-Z0-9_]+")
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def test_dark_and_light_tokens_have_identical_keys():
    assert set(DARK_TOKENS.keys()) == set(LIGHT_TOKENS.keys())


def test_render_qss_leaves_no_placeholders():
    qss_template_path = os.path.join(REPO_ROOT, "assets", "style", "main.qss")
    with open(qss_template_path, encoding="utf-8") as f:
        qss_template = f.read()

    icon_paths = {"down_arrow": "x", "spin_up": "y", "spin_down": "z"}

    for tokens in (DARK_TOKENS, LIGHT_TOKENS):
        rendered = render_qss(qss_template, tokens, icon_paths)
        leftover = PLACEHOLDER_PATTERN.findall(rendered)
        assert not leftover, f"Unresolved placeholders: {leftover}"


def test_render_qss_replaces_known_placeholder():
    result = render_qss("QWidget { color: @color_text_primary; }", {"text_primary": "#123456"}, {})
    assert result == "QWidget { color: #123456; }"


def test_render_qss_handles_prefix_collisions():
    # "border" is a prefix of "border_strong" - a naive dict-order replace
    # corrupts the longer placeholder into "#111111_strong". Regression for
    # the bug reported after the theme system shipped.
    template = "a { border-color: @color_border; } b { border-color: @color_border_strong; }"
    tokens = {"border": "#111111", "border_strong": "#222222"}

    result = render_qss(template, tokens, {})

    assert result == "a { border-color: #111111; } b { border-color: #222222; }"


def test_dark_tokens_render_without_leftover_suffix_fragments():
    # Broader guard: for every real DARK_TOKENS key that is a prefix of another
    # key, rendering must not leave a "<value>_<suffix>" fragment behind.
    icon_paths = {"down_arrow": "x", "spin_up": "y", "spin_down": "z"}
    template = " ".join(f"@color_{key}" for key in DARK_TOKENS)
    rendered = render_qss(template, DARK_TOKENS, icon_paths)

    for key, value in DARK_TOKENS.items():
        for other_key in DARK_TOKENS:
            if other_key != key and other_key.startswith(key):
                suffix = other_key[len(key):]
                assert f"{value}{suffix}" not in rendered, (
                    f"'{key}' leaked into '{other_key}': found '{value}{suffix}'"
                )
