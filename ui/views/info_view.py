from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextBrowser, QPushButton
from PySide6.QtCore import Qt
from utils.constants import AppConstants
from utils.strings import UIStrings

class InfoView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10) # Reduced spacing
        layout.setContentsMargins(20, 20, 20, 20) # Reduced margins

        # Version (Title removed as it is in header)
        version = QLabel(UIStrings.VERSION_TEMPLATE.format(version=AppConstants.VERSION))
        version.setObjectName("VersionLabel")
        version.setAlignment(Qt.AlignCenter)
        layout.addWidget(version)

        # Content (Instructions)
        content = QLabel()
        content.setObjectName("InfoContentLabel")
        content.setWordWrap(True)
        content.setOpenExternalLinks(True)
        content.setText(UIStrings.INFO_HTML_CONTENT)
        layout.addWidget(content)

        layout.addStretch()

        # Footer
        footer = QLabel(UIStrings.FOOTER_TEXT)
        footer.setObjectName("FooterLabel")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)
