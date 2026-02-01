from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QPixmap, QPainter
from utils.path_helper import get_resource_path
import os

class DropZone(QFrame):
    files_dropped = Signal(list)
    clicked = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("DropZone")
        self.setAcceptDrops(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(200)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        # Icon
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_path = get_resource_path("assets/icons/upload_icon.svg")
        if os.path.exists(self.icon_path):
            pixmap = QPixmap(self.icon_path)
            scaled_pixmap = pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            # Recolor pixmap to match theme? SVG usually handles color, 
            # but if we want specific color we might need QIcon + paint. 
            # For now relying on SVG color.
            self.icon_label.setPixmap(scaled_pixmap)
        
        layout.addWidget(self.icon_label)

        # Text
        self.text_label = QLabel("Resimleri Buraya Sürükleyin\nveya\nTıklayın")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("font-size: 16px; color: #a6adc8; font-weight: bold;")
        layout.addWidget(self.text_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.text_label.setText("Bırak Gelsin! 📂")
            self.setStyleSheet("#DropZone { border-color: #a6e3a1; background-color: rgba(166, 227, 161, 0.1); }")

    def dragLeaveEvent(self, event):
        self.text_label.setText("Resimleri Buraya Sürükleyin\nveya\nTıklayın")
        self.setStyleSheet("") # Revert to stylesheet default
        
    def dropEvent(self, event: QDropEvent):
        self.text_label.setText("Resimleri Buraya Sürükleyin\nveya\nTıklayın")
        self.setStyleSheet("")
        
        files = []
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path:
                    files.append(file_path)
            
            if files:
                self.files_dropped.emit(files)
