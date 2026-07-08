import sys
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor

class ToastNotification(QWidget):
    def __init__(self, parent, message, duration=2500):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        self.duration = duration
        self.setup_ui(message)
        
    def setup_ui(self, message):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(40, 40, 40, 230);
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 500;
            }
        """)
        layout.addWidget(self.label)
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)
        
    def show_toast(self):
        # Center horizontally at the bottom of the parent
        if self.parent():
            parent_rect = self.parent().rect()
            parent_pos = self.parent().mapToGlobal(parent_rect.topLeft())
            
            # Use sizeHint since the widget might not be shown yet
            self.adjustSize()
            
            # Position it horizontally centered and vertically near the bottom
            x = parent_pos.x() + (parent_rect.width() - self.width()) // 2
            y = parent_pos.y() + parent_rect.height() - self.height() - 50
            
            self.move(x, y)
        
        self.show()
        
        # Fade In
        self.anim_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim_in.setDuration(300)
        self.anim_in.setStartValue(0.0)
        self.anim_in.setEndValue(1.0)
        self.anim_in.setEasingCurve(QEasingCurve.OutCubic)
        self.anim_in.start()
        
        # Start timer for Fade Out
        QTimer.singleShot(self.duration, self.hide_toast)
        
    def hide_toast(self):
        self.anim_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim_out.setDuration(400)
        self.anim_out.setStartValue(1.0)
        self.anim_out.setEndValue(0.0)
        self.anim_out.setEasingCurve(QEasingCurve.InCubic)
        self.anim_out.finished.connect(self.close)
        self.anim_out.start()

    @staticmethod
    def show_message(parent, message, duration=2500):
        toast = ToastNotification(parent, message, duration)
        toast.show_toast()
        return toast
