from PySide6.QtWidgets import QApplication
from utils.path_helper import get_resource_path
from utils.constants import AppIcons
import os
import logging

logger = logging.getLogger(__name__)

class ThemeManager:
    @staticmethod
    def apply_theme(app: QApplication):
        """
        Loads the main.qss file, replaces placeholders with actual paths,
        and applies it to the application.
        """
        try:
            # Load QSS from assets/style folder
            qss_path = get_resource_path(AppIcons.MAIN_QSS)

            if os.path.exists(qss_path):
                with open(qss_path, "r", encoding='utf-8') as f:
                    qss = f.read()

                    # Dynamically replace resource paths
                    # For QSS, we need forward slashes even on Windows
                    # ComboBox Arrow
                    icon_down_path = get_resource_path(AppIcons.DOWN_ARROW).replace("\\", "/")
                    qss = qss.replace("@icon_down_arrow", icon_down_path)

                    # SpinBox Arrows
                    icon_spin_up = get_resource_path(AppIcons.UP_ARROW).replace("\\", "/")
                    icon_spin_down = get_resource_path(AppIcons.DOWN_ARROW).replace("\\", "/")
                    
                    qss = qss.replace("@icon_spin_up", icon_spin_up)
                    qss = qss.replace("@icon_spin_down", icon_spin_down)
                    
                    app.setStyleSheet(qss)
            else:
                logger.warning("Stylesheet not found at %s", qss_path)
        except Exception:
            logger.exception("Error applying theme")
