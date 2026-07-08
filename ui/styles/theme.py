from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSettings
from utils.path_helper import get_resource_path
from utils.constants import AppIcons, AppConstants
from ui.styles.tokens import THEMES
from utils.svg_colorizer import get_tinted_icon, create_tinted_svg_file
from PySide6.QtGui import QIcon
import os
import logging

logger = logging.getLogger(__name__)

SETTINGS_ORGANIZATION = "MYY Yazılım"
SETTINGS_KEY_THEME = "theme"
DEFAULT_THEME = "light"


def render_qss(qss_template: str, color_tokens: dict, icon_paths: dict) -> str:
    """
    Replaces @icon_<key> and @color_<key> placeholders in a QSS template.
    Pure string operation - no QApplication/Qt widget dependency, so it's
    directly unit-testable (see tests/test_theme.py).

    Keys are processed longest-first: several token names share a prefix
    (e.g. "border" / "border_strong"), so replacing the short key first would
    corrupt the longer placeholder (leaves a stray "@color_border" match
    inside "@color_border_strong", producing "#hex_strong").
    """
    qss = qss_template
    for key, value in sorted(icon_paths.items(), key=lambda kv: -len(kv[0])):
        qss = qss.replace(f"@icon_{key}", value)
    for key, value in sorted(color_tokens.items(), key=lambda kv: -len(kv[0])):
        qss = qss.replace(f"@color_{key}", value)
    return qss


class ThemeManager:
    current_theme = DEFAULT_THEME

    @staticmethod
    def _settings() -> QSettings:
        return QSettings(SETTINGS_ORGANIZATION, AppConstants.APP_NAME)

    @staticmethod
    def apply_theme(app: QApplication, theme: str = None):
        """
        Loads main.qss, resolves @icon_*/@color_* placeholders for the given
        (or persisted) theme, and applies it to the application.
        """
        if theme is None:
            theme = ThemeManager._settings().value(SETTINGS_KEY_THEME, DEFAULT_THEME)
        if theme not in THEMES:
            theme = DEFAULT_THEME

        try:
            qss_path = get_resource_path(AppIcons.MAIN_QSS)

            if os.path.exists(qss_path):
                with open(qss_path, "r", encoding='utf-8') as f:
                    qss_template = f.read()

                # For QSS, we need forward slashes even on Windows
                arrow_color = THEMES[theme].get("text_muted", "#666666")
                icon_paths = {
                    "down_arrow": create_tinted_svg_file(get_resource_path(AppIcons.DOWN_ARROW), arrow_color).replace("\\", "/"),
                    "spin_up": create_tinted_svg_file(get_resource_path(AppIcons.UP_ARROW), arrow_color).replace("\\", "/"),
                    "spin_down": create_tinted_svg_file(get_resource_path(AppIcons.DOWN_ARROW), arrow_color).replace("\\", "/"),
                }

                qss = render_qss(qss_template, THEMES[theme], icon_paths)
                app.setStyleSheet(qss)

                ThemeManager.current_theme = theme
                ThemeManager._settings().setValue(SETTINGS_KEY_THEME, theme)
            else:
                logger.warning("Stylesheet not found at %s", qss_path)
        except Exception:
            logger.exception("Error applying theme")

    @staticmethod
    def toggle_theme(app: QApplication) -> str:
        """Flips light<->dark, applies it, and returns the new theme name."""
        new_theme = "light" if ThemeManager.current_theme == "dark" else "dark"
        ThemeManager.apply_theme(app, new_theme)
        return ThemeManager.current_theme

    @staticmethod
    def get_themed_icon(relative_path: str, color_token: str = "text_primary") -> QIcon:
        """
        Returns a dynamically tinted QIcon based on the current theme.
        """
        color_hex = THEMES[ThemeManager.current_theme].get(color_token, "#000000")
        abs_path = get_resource_path(relative_path)
        return get_tinted_icon(abs_path, color_hex)
