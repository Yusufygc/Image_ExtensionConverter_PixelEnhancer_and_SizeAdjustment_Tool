import os
import sys
import logging

from PySide6.QtGui import QIcon

logger = logging.getLogger(__name__)

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for dev and for PyInstaller/Nuitka.
    
    Args:
        relative_path (str): The relative path to the resource (e.g., "assets/icons/icon.png").
        
    Returns:
        str: The absolute path to the resource.
    """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            # Works for development and Nuitka (Standalone & Onefile)
            # In Nuitka Onefile, __file__ points to the temporary extracted directory,
            # whereas sys.executable points to the original exe file.
            # Since our assets are bundled inside the temp dir, we must use __file__.
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        return os.path.join(base_path, relative_path)
    except Exception:
        logger.exception("Error resolving path for %s", relative_path)
        return relative_path


def get_icon(relative_path):
    """
    Resolves relative_path via get_resource_path() and returns a QIcon,
    or None if the file doesn't exist - callers decide on a text/emoji fallback.
    """
    path = get_resource_path(relative_path)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return QIcon(path)
    logger.warning("Icon not found or is empty: %s", path)
    return None
