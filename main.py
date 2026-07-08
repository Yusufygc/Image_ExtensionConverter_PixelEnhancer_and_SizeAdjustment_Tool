import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from utils.logger import setup_logging

def main():
    setup_logging()
    app = QApplication(sys.argv)
    
    # Create Main Window, passing app instance for theming
    window = MainWindow(app)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
