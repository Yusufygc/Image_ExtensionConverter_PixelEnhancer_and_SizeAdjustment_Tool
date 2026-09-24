import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtCore import QUrl

from ui.bridge import AppBridge
from utils.logger import setup_logging
from utils.path_helper import get_resource_path, get_icon
from utils.constants import AppIcons, AppConstants


def main():
    setup_logging()
    QQuickStyle.setStyle("Basic")
    app = QApplication(sys.argv)
    app.setApplicationName(AppConstants.APP_NAME)

    app_icon = get_icon(AppIcons.APP)
    if app_icon:
        app.setWindowIcon(app_icon)

    # Parent bridge to app so its C++ lifecycle is safely managed
    bridge = AppBridge(app)

    engine = QQmlApplicationEngine()

    # Gracefully stop worker thread if window is closed during operation
    def on_about_to_quit():
        if bridge.current_worker and bridge.current_worker.isRunning():
            bridge.cancelProcessing()
            bridge.current_worker.wait(1000)

    app.aboutToQuit.connect(on_about_to_quit)

    qml_dir = get_resource_path("ui/qml")
    engine.addImportPath(qml_dir)
    engine.rootContext().setContextProperty("bridge", bridge)

    main_qml_path = os.path.join(qml_dir, "Main.qml")
    engine.load(QUrl.fromLocalFile(main_qml_path))

    if not engine.rootObjects():
        sys.exit(-1)

    exit_code = app.exec()

    # Explicitly destroy QML engine and root objects while bridge is still alive
    del engine

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
