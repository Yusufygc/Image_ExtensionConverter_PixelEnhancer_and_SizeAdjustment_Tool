import os
import re
import tempfile
import logging
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QByteArray

logger = logging.getLogger(__name__)

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
            
        # Replace stroke (ignoring none)
        svg_content = re.sub(r'stroke="#[0-9a-fA-F]{3,6}"', f'stroke="{color_hex}"', svg_content)
        # Replace fill (ignoring none)
        svg_content = re.sub(r'fill="#[0-9a-fA-F]{3,6}"', f'fill="{color_hex}"', svg_content)
        
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
    returning the temporary file path.
    """
    if not os.path.exists(path):
        return path
        
    try:
        with open(path, "r", encoding="utf-8") as f:
            svg_content = f.read()
            
        svg_content = re.sub(r'stroke="#[0-9a-fA-F]{3,6}"', f'stroke="{color_hex}"', svg_content)
        svg_content = re.sub(r'fill="#[0-9a-fA-F]{3,6}"', f'fill="{color_hex}"', svg_content)
        
        fd, temp_path = tempfile.mkstemp(suffix=".svg")
        with os.fdopen(fd, 'w', encoding="utf-8") as f:
            f.write(svg_content)
            
        return temp_path
    except Exception as e:
        logger.exception(f"Error creating tinted svg {path}: {e}")
        return path
