from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QPixmap, QImageReader
from utils.path_helper import get_resource_path, get_icon
from utils.image_loader import load_image
from utils.constants import AppIcons
from utils.strings import UIStrings
import os

class FileListItemWidget(QWidget):
    remove_clicked = Signal(str) # Emits file path to remove

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # Thumbnail
        self.thumb_label = QLabel()
        self.thumb_label.setObjectName("ThumbLabel")
        self.thumb_label.setFixedSize(48, 48)
        self.thumb_label.setAlignment(Qt.AlignCenter)
        
        self.load_thumbnail()
        layout.addWidget(self.thumb_label)

        # File Info Container
        info_layout = QHBoxLayout() # Or VBox for name + size
        
        # Name & Size
        try:
            name = os.path.basename(self.file_path)
            size_bytes = os.path.getsize(self.file_path)
            size_str = self.format_size(size_bytes)
            
            self.name_label = QLabel(name)
            self.name_label.setObjectName("FileNameLabel")

            self.size_label = QLabel(f"({size_str})")
            self.size_label.setObjectName("FileSizeLabel")
            
            info_layout.addWidget(self.name_label)
            info_layout.addWidget(self.size_label)
            info_layout.addStretch()
        except Exception:
            self.name_label = QLabel(os.path.basename(self.file_path))
            self.name_label.setObjectName("FileNameLabel")
            info_layout.addWidget(self.name_label)
        
        layout.addLayout(info_layout, stretch=1)

        # Processing status badge (empty until the worker touches this file)
        self.status_label = QLabel()
        self.status_label.setFixedWidth(20)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # Remove Button
        self.btn_remove = QPushButton()
        self.btn_remove.setFixedSize(24, 24)
        self.btn_remove.setCursor(Qt.PointingHandCursor)
        self.btn_remove.setObjectName("IconOnlyButton")
        self.btn_remove.setToolTip(UIStrings.TOOLTIP_REMOVE_FILE)
        
        delete_icon = get_icon(AppIcons.DELETE)
        if delete_icon:
            self.btn_remove.setIcon(delete_icon)
            self.btn_remove.setIconSize(QSize(16, 16))
        else:
            self.btn_remove.setText(UIStrings.FALLBACK_REMOVE)
            
        self.btn_remove.clicked.connect(self.on_remove)

        layout.addWidget(self.btn_remove)

    def load_thumbnail(self):
        # Async loading would be better but keeping it simple for now
        # Small performance hit if many large files.
        try:
            # First check if it's an image
            ext = os.path.splitext(self.file_path)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.ico', '.webp', '.svg']:
                # Decode directly at target size instead of loading full resolution
                reader = QImageReader(self.file_path)
                original_size = reader.size()
                if original_size.isValid():
                    reader.setScaledSize(original_size.scaled(40, 40, Qt.KeepAspectRatio))
                image = reader.read()
                if not image.isNull():
                    self.thumb_label.setPixmap(QPixmap.fromImage(image))
                    return

            # Fallback icon
            fallback_path = get_resource_path(AppIcons.FILE)
            if os.path.exists(fallback_path):
                 self.thumb_label.setPixmap(QPixmap(fallback_path).scaled(28, 28, Qt.KeepAspectRatio))
            else:
                 self.thumb_label.setText(UIStrings.FALLBACK_THUMB_FILE)

        except Exception:
            self.thumb_label.setText(UIStrings.FALLBACK_THUMB_UNKNOWN)

    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def on_remove(self):
        self.remove_clicked.emit(self.file_path)

    def set_status(self, status: str):
        """status: 'processing' | 'success' | 'error' | '' (reset)"""
        glyphs = {
            "processing": UIStrings.FILE_STATUS_PROCESSING,
            "success": UIStrings.FILE_STATUS_SUCCESS,
            "error": UIStrings.FILE_STATUS_ERROR,
        }
        self.status_label.setText(glyphs.get(status, ""))
