import os
import re
import tempfile
import atexit
import logging
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QByteArray

logger = logging.getLogger(__name__)

# (path, color_hex) -> generated temp file path. Same icon+color pair is
# requested repeatedly (every theme apply/toggle) with identical output, so
# without this cache each call would leak a new temp SVG file on disk.
_tint_cache: dict[tuple[str, str], str] = {}


def _tint_svg_content(svg_content: str, color_hex: str) -> str:
    svg_content = re.sub(r'stroke="#[0-9a-fA-F]{3,6}"', f'stroke="{color_hex}"', svg_content)
    svg_content = re.sub(r'fill="#[0-9a-fA-F]{3,6}"', f'fill="{color_hex}"', svg_content)
    return svg_content


def _cleanup_tint_cache():
    for temp_path in _tint_cache.values():
        try:
            os.remove(temp_path)
        except OSError:
            pass


atexit.register(_cleanup_tint_cache)


def get_tinted_icon(path: str, color_hex: str) -> QIcon:
    """
    Reads an SVG file, replaces all 'stroke="#..."' and 'fill="#..."'
    (except none) with the given color_hex, and returns a QIcon.
    """
    if not os.path.exists(path):
        logger.warning(f"Tinted icon not found: {path}")
        return QIcon()

    try:
        with open(path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        svg_content = _tint_svg_content(svg_content, color_hex)

        byte_array = QByteArray(svg_content.encode("utf-8"))
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array, "SVG")
        return QIcon(pixmap)
    except Exception as e:
        logger.exception(f"Error tinting icon {path}: {e}")
        return QIcon(path)


def create_tinted_svg_file(path: str, color_hex: str) -> str:
    """
    Reads an SVG file, replaces colors, and writes it to a temp file,
    returning the temporary file path. Repeated calls with the same
    (path, color_hex) reuse the same cached temp file instead of
    creating a new one each time.
    """
    if not os.path.exists(path):
        return path

    cache_key = (path, color_hex)
    cached_path = _tint_cache.get(cache_key)
    if cached_path and os.path.exists(cached_path):
        return cached_path

    try:
        with open(path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        svg_content = _tint_svg_content(svg_content, color_hex)

        fd, temp_path = tempfile.mkstemp(suffix=".svg")
        with os.fdopen(fd, 'w', encoding="utf-8") as f:
            f.write(svg_content)

        _tint_cache[cache_key] = temp_path
        return temp_path
    except Exception as e:
        logger.exception(f"Error creating tinted svg {path}: {e}")
        return path
