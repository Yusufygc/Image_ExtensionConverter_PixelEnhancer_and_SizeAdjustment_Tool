import os
import logging
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFileDialog

from core.converter import ConverterService
from core.resizer import ResizerService
from core.enhancer import EnhancerService
from ui.worker import ProcessingWorker
from ui.styles.theme import ThemeManager
from utils.constants import AppConstants, AppIcons
from utils.strings import UIStrings
from utils.path_helper import get_resource_path

logger = logging.getLogger(__name__)

dir_output_default = os.path.join(os.path.expanduser("~"), "Desktop", "Conventor_Output")


def format_size(size_bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


class AppBridge(QObject):
    """
    Bridge connecting QML presentation layer to the backend services.
    Adheres strictly to the layer rule: core/ is untouched.
    """

    # Signals for reactive property binding in QML
    filesChanged = Signal()
    countsChanged = Signal()
    outputDirChanged = Signal()
    currentOpChanged = Signal()
    targetFormatChanged = Signal()
    resizeTypeChanged = Signal()
    resizeWidthChanged = Signal()
    resizeHeightChanged = Signal()
    resizePercentChanged = Signal()
    enhanceFactorChanged = Signal()
    isProcessingChanged = Signal()
    progressValueChanged = Signal()
    progressMessageChanged = Signal()
    currentThemeChanged = Signal()
    viewModeChanged = Signal()
    sortOptionChanged = Signal()

    # Event signals
    toastRequested = Signal(str, str)  # message, type ("success", "error", "warning", "info")
    batchFinished = Signal(bool, list)  # success, errors

    def __init__(self, parent=None):
        super().__init__(parent)

        # Backend Services (Untouched)
        self.converter_service = ConverterService()
        self.resizer_service = ResizerService()
        self.enhancer_service = EnhancerService()

        self.current_worker = None

        # Data Model: list of dicts
        self._files = []
        self._output_dir = dir_output_default

        # Operation state
        self._current_op = 0  # 0: Convert, 1: Resize, 2: Enhance
        self._target_format = "PNG"
        self._resize_type = 0  # 0: Dimensions, 1: Percent
        self._resize_width = 1920
        self._resize_height = 1080
        self._resize_percent = 50
        self._enhance_factor = 2.0

        # Processing state
        self._is_processing = False
        self._progress_value = 0
        self._progress_message = UIStrings.STATUS_READY

        # View settings
        self._view_mode = "grid"  # "grid" or "list"
        self._sort_option = "name_asc"
        self._current_theme = ThemeManager.get_persisted_theme()

    # -------------------------------------------------------------------------
    # Properties exposed to QML
    # -------------------------------------------------------------------------
    @Property(list, notify=filesChanged)
    def fileList(self):
        return self._files

    @Property(int, notify=countsChanged)
    def totalCount(self):
        return len(self._files)

    @Property(int, notify=countsChanged)
    def selectedCount(self):
        return sum(1 for f in self._files if f.get("selected", False))

    @Property(str, notify=outputDirChanged)
    def outputDir(self):
        return self._output_dir

    @Property(int, notify=currentOpChanged)
    def currentOp(self):
        return self._current_op

    @Property(list, constant=True)
    def supportedFormats(self):
        return AppConstants.SUPPORTED_FORMATS

    @Property(dict, constant=True)
    def icons(self):
        return {
            "app": QUrl.fromLocalFile(get_resource_path(AppIcons.APP)).toString(),
            "upload": QUrl.fromLocalFile(get_resource_path(AppIcons.UPLOAD)).toString(),
            "delete": QUrl.fromLocalFile(get_resource_path(AppIcons.DELETE)).toString(),
            "info": QUrl.fromLocalFile(get_resource_path(AppIcons.INFO)).toString(),
            "folder": QUrl.fromLocalFile(get_resource_path(AppIcons.FOLDER)).toString(),
            "file": QUrl.fromLocalFile(get_resource_path(AppIcons.FILE)).toString(),
            "backArrow": QUrl.fromLocalFile(get_resource_path(AppIcons.BACK_ARROW)).toString(),
            "downArrow": QUrl.fromLocalFile(get_resource_path(AppIcons.DOWN_ARROW)).toString(),
            "upArrow": QUrl.fromLocalFile(get_resource_path(AppIcons.UP_ARROW)).toString(),
            "sun": QUrl.fromLocalFile(get_resource_path(AppIcons.THEME_SUN)).toString(),
            "moon": QUrl.fromLocalFile(get_resource_path(AppIcons.THEME_MOON)).toString(),
            "check": QUrl.fromLocalFile(get_resource_path(AppIcons.CHECK)).toString(),
            "error": QUrl.fromLocalFile(get_resource_path(AppIcons.ERROR)).toString(),
            "sort": QUrl.fromLocalFile(get_resource_path(AppIcons.SORT)).toString(),
            "grid": QUrl.fromLocalFile(get_resource_path(AppIcons.GRID)).toString(),
            "list": QUrl.fromLocalFile(get_resource_path(AppIcons.LIST)).toString(),
            "openFolder": QUrl.fromLocalFile(get_resource_path(AppIcons.OPEN_FOLDER)).toString(),
            "trash": QUrl.fromLocalFile(get_resource_path(AppIcons.TRASH)).toString(),
        }

    @Property(dict, constant=True)
    def strings(self):
        return {
            "appName": AppConstants.APP_NAME,
            "version": AppConstants.VERSION,
            "deleteSelected": UIStrings.BTN_DELETE_SELECTED,
            "clearAll": UIStrings.BTN_CLEAR_ALL,
            "selectAll": UIStrings.BTN_SELECT_ALL,
            "openOutputFolder": UIStrings.BTN_OPEN_OUTPUT_FOLDER,
            "tooltipSort": UIStrings.TOOLTIP_SORT,
            "tooltipGrid": UIStrings.TOOLTIP_VIEW_GRID,
            "tooltipList": UIStrings.TOOLTIP_VIEW_LIST,
            "tooltipOpenFolder": UIStrings.TOOLTIP_OPEN_OUTPUT_FOLDER,
            "tooltipAddFiles": UIStrings.TOOLTIP_ADD_FILES,
            "sortNameAsc": UIStrings.SORT_NAME_ASC,
            "sortNameDesc": UIStrings.SORT_NAME_DESC,
            "sortSizeAsc": UIStrings.SORT_SIZE_ASC,
            "sortSizeDesc": UIStrings.SORT_SIZE_DESC,
            "sortStatus": UIStrings.SORT_STATUS,
            "opConvert": UIStrings.OP_LABEL_CONVERT,
            "opResize": UIStrings.OP_LABEL_RESIZE,
            "opEnhance": UIStrings.OP_LABEL_ENHANCE,
            "tabConvert": UIStrings.OP_TAB_CONVERT,
            "tabResize": UIStrings.OP_TAB_RESIZE,
            "tabEnhance": UIStrings.OP_TAB_ENHANCE,
            "targetFormat": UIStrings.LBL_TARGET_FORMAT,
            "resizeMethod": UIStrings.LBL_RESIZE_METHOD,
            "methodDimensions": UIStrings.RESIZE_METHOD_DIMENSIONS,
            "methodPercent": UIStrings.RESIZE_METHOD_PERCENT,
            "width": UIStrings.LBL_WIDTH,
            "height": UIStrings.LBL_HEIGHT,
            "percent": UIStrings.LBL_PERCENT,
            "enhanceFactor": UIStrings.LBL_ENHANCE_FACTOR,
            "targetFolder": UIStrings.LBL_TARGET_FOLDER,
            "outputPlaceholder": UIStrings.OUTPUT_PLACEHOLDER,
            "btnProcess": UIStrings.BTN_PROCESS,
            "dropTitle": UIStrings.DROPZONE_DEFAULT_TITLE,
            "dropSub": UIStrings.DROPZONE_DEFAULT_SUB,
            "dropActive": UIStrings.DROPZONE_DRAG_ACTIVE,
            "browseFiles": UIStrings.BTN_BROWSE,
            "statusReady": UIStrings.STATUS_READY,
            "statusCompleted": UIStrings.STATUS_COMPLETED,
            "infoTooltip": UIStrings.TOOLTIP_INFO,
            "themeLightTooltip": UIStrings.TOOLTIP_THEME_TOGGLE_TO_LIGHT,
            "themeDarkTooltip": UIStrings.TOOLTIP_THEME_TOGGLE_TO_DARK,
            "footerText": UIStrings.FOOTER_TEXT,
            "infoHtml": UIStrings.INFO_HTML_CONTENT,
        }

    @Property(str, notify=targetFormatChanged)
    def targetFormat(self):
        return self._target_format

    @Property(int, notify=resizeTypeChanged)
    def resizeType(self):
        return self._resize_type

    @Property(int, notify=resizeWidthChanged)
    def resizeWidth(self):
        return self._resize_width

    @Property(int, notify=resizeHeightChanged)
    def resizeHeight(self):
        return self._resize_height

    @Property(int, notify=resizePercentChanged)
    def resizePercent(self):
        return self._resize_percent

    @Property(float, notify=enhanceFactorChanged)
    def enhanceFactor(self):
        return self._enhance_factor

    @Property(bool, notify=isProcessingChanged)
    def isProcessing(self):
        return self._is_processing

    @Property(int, notify=progressValueChanged)
    def progressValue(self):
        return self._progress_value

    @Property(str, notify=progressMessageChanged)
    def progressMessage(self):
        return self._progress_message

    @Property(str, notify=currentThemeChanged)
    def currentTheme(self):
        return self._current_theme

    @Property(str, notify=viewModeChanged)
    def viewMode(self):
        return self._view_mode

    @Property(str, notify=sortOptionChanged)
    def sortOption(self):
        return self._sort_option

    # -------------------------------------------------------------------------
    # Slots callable from QML
    # -------------------------------------------------------------------------
    @Slot(int)
    def setCurrentOp(self, op: int):
        if self._current_op != op:
            self._current_op = op
            self.currentOpChanged.emit()

    @Slot(str)
    def setTargetFormat(self, fmt: str):
        if self._target_format != fmt:
            self._target_format = fmt
            self.targetFormatChanged.emit()

    @Slot(int)
    def setResizeType(self, r_type: int):
        if self._resize_type != r_type:
            self._resize_type = r_type
            self.resizeTypeChanged.emit()

    @Slot(int)
    def setResizeWidth(self, w: int):
        if self._resize_width != w:
            self._resize_width = w
            self.resizeWidthChanged.emit()

    @Slot(int)
    def setResizeHeight(self, h: int):
        if self._resize_height != h:
            self._resize_height = h
            self.resizeHeightChanged.emit()

    @Slot(int)
    def setResizePercent(self, p: int):
        if self._resize_percent != p:
            self._resize_percent = p
            self.resizePercentChanged.emit()

    @Slot(float)
    def setEnhanceFactor(self, f: float):
        if self._enhance_factor != f:
            self._enhance_factor = f
            self.enhanceFactorChanged.emit()

    @Slot(str)
    def setViewMode(self, mode: str):
        if self._view_mode != mode:
            self._view_mode = mode
            self.viewModeChanged.emit()

    @Slot(str)
    def setOutputDir(self, path: str):
        if self._output_dir != path:
            self._output_dir = path
            self.outputDirChanged.emit()

    @Slot()
    def toggleTheme(self):
        new_theme = "light" if self._current_theme == "dark" else "dark"
        self._current_theme = new_theme
        ThemeManager.save_theme(new_theme)
        self.currentThemeChanged.emit()

    @Slot()
    def browseFiles(self):
        files, _ = QFileDialog.getOpenFileNames(
            None,
            UIStrings.DIALOG_SELECT_IMAGES_TITLE,
            "",
            UIStrings.DIALOG_IMAGE_FILTER
        )
        if files:
            self.addFiles(files)

    @Slot(list)
    def addFiles(self, file_paths: list):
        existing_paths = {f["path"] for f in self._files}
        added_count = 0

        for raw_path in file_paths:
            path = raw_path
            # Handle QML file:/// URL prefix if dropped directly
            if path.startswith("file:///"):
                path = QUrl(raw_path).toLocalFile()
            elif path.startswith("file://"):
                path = QUrl(raw_path).toLocalFile()

            path = os.path.normpath(path)
            if not os.path.isfile(path):
                continue

            ext = os.path.splitext(path)[1].lower()
            if ext not in AppConstants.SUPPORTED_EXTENSIONS:
                continue

            if path not in existing_paths:
                try:
                    size_bytes = os.path.getsize(path)
                    size_fmt = format_size(size_bytes)
                except OSError:
                    size_bytes = 0
                    size_fmt = "0 B"

                self._files.append({
                    "path": path,
                    "name": os.path.basename(path),
                    "size": size_bytes,
                    "sizeFormatted": size_fmt,
                    "ext": ext.replace(".", "").upper(),
                    "status": "",  # "", "processing", "success", "error"
                    "selected": False,
                    "url": QUrl.fromLocalFile(path).toString()
                })
                existing_paths.add(path)
                added_count += 1

        if added_count > 0:
            self._apply_sort()
            self.filesChanged.emit()
            self.countsChanged.emit()
            self.toastRequested.emit(f"{added_count} dosya eklendi.", "info")

    @Slot(str)
    def removeFile(self, path: str):
        self._files = [f for f in self._files if f["path"] != path]
        self.filesChanged.emit()
        self.countsChanged.emit()

    @Slot()
    def clearFiles(self):
        if self._files:
            self._files = []
            self.filesChanged.emit()
            self.countsChanged.emit()
            self.toastRequested.emit("Tüm dosyalar temizlendi.", "info")

    @Slot()
    def removeSelectedFiles(self):
        initial_len = len(self._files)
        self._files = [f for f in self._files if not f.get("selected", False)]
        removed = initial_len - len(self._files)
        if removed > 0:
            self.filesChanged.emit()
            self.countsChanged.emit()
            self.toastRequested.emit(f"{removed} dosya silindi.", "info")

    @Slot(str)
    def toggleFileSelection(self, path: str):
        for f in self._files:
            if f["path"] == path:
                f["selected"] = not f.get("selected", False)
                break
        self.filesChanged.emit()
        self.countsChanged.emit()

    @Slot(bool)
    def selectAllFiles(self, select: bool):
        for f in self._files:
            f["selected"] = select
        self.filesChanged.emit()
        self.countsChanged.emit()

    @Slot(str)
    def sortFiles(self, criteria: str):
        self._sort_option = criteria
        self._apply_sort()
        self.sortOptionChanged.emit()
        self.filesChanged.emit()

    def _apply_sort(self):
        crit = self._sort_option
        if crit == "name_asc":
            self._files.sort(key=lambda x: x["name"].lower())
        elif crit == "name_desc":
            self._files.sort(key=lambda x: x["name"].lower(), reverse=True)
        elif crit == "size_asc":
            self._files.sort(key=lambda x: x["size"])
        elif crit == "size_desc":
            self._files.sort(key=lambda x: x["size"], reverse=True)
        elif crit == "status":
            # order: processing -> error -> idle -> success
            order = {"processing": 0, "error": 1, "": 2, "success": 3}
            self._files.sort(key=lambda x: order.get(x["status"], 2))

    @Slot()
    def browseOutputDir(self):
        folder = QFileDialog.getExistingDirectory(
            None, UIStrings.DIALOG_SELECT_OUTPUT_FOLDER_TITLE, self._output_dir
        )
        if folder:
            self.setOutputDir(folder)

    @Slot()
    def openOutputFolder(self):
        """Opens the target output directory in Windows File Explorer."""
        folder = self._output_dir or dir_output_default
        os.makedirs(folder, exist_ok=True)
        try:
            os.startfile(folder)
        except Exception:
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder))

    # -------------------------------------------------------------------------
    # Processing Execution (Uses existing core/ & worker)
    # -------------------------------------------------------------------------
    @Slot()
    def startProcessing(self):
        if not self._files:
            self.toastRequested.emit(UIStrings.MSG_NO_FILES_SELECTED, "warning")
            return

        if self._is_processing:
            return

        # Prepare kwargs based on current operation
        if self._current_op == 0:
            service = self.converter_service
            kwargs = {"output_format": self._target_format}
        elif self._current_op == 1:
            service = self.resizer_service
            if self._resize_type == 0:
                kwargs = {"width": self._resize_width, "height": self._resize_height}
            else:
                kwargs = {"percentage": self._resize_percent}
        else:
            service = self.enhancer_service
            kwargs = {"factor": self._enhance_factor}

        if self._output_dir:
            kwargs["output_dir"] = self._output_dir

        # Reset statuses of files
        for f in self._files:
            f["status"] = ""
        self.filesChanged.emit()

        file_paths = [f["path"] for f in self._files]

        self._is_processing = True
        self._progress_value = 0
        self._progress_message = UIStrings.STATUS_PROCESSING
        self.isProcessingChanged.emit()
        self.progressValueChanged.emit()
        self.progressMessageChanged.emit()

        # Start ProcessingWorker (existing untouched thread)
        self.current_worker = ProcessingWorker(service, file_paths, **kwargs)
        self.current_worker.signals.progress.connect(self._on_worker_progress)
        self.current_worker.signals.file_started.connect(self._on_file_started)
        self.current_worker.signals.file_done.connect(self._on_file_done)
        self.current_worker.signals.finished.connect(self._on_worker_finished)
        self.current_worker.signals.error.connect(self._on_worker_error)
        self.current_worker.start()

    @Slot()
    def cancelProcessing(self):
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.stop()
            self._is_processing = False
            self.isProcessingChanged.emit()
            self._progress_message = "İşlem iptal edildi."
            self.progressMessageChanged.emit()
            self.toastRequested.emit("İşlem iptal edildi.", "warning")

    def _on_worker_progress(self, val: int, msg: str):
        self._progress_value = val
        self._progress_message = msg
        self.progressValueChanged.emit()
        self.progressMessageChanged.emit()

    def _on_file_started(self, file_path: str):
        for f in self._files:
            if f["path"] == file_path:
                f["status"] = "processing"
                break
        self.filesChanged.emit()

    def _on_file_done(self, file_path: str, success: bool):
        for f in self._files:
            if f["path"] == file_path:
                f["status"] = "success" if success else "error"
                break
        self.filesChanged.emit()

    def _on_worker_finished(self):
        self._is_processing = False
        self.isProcessingChanged.emit()

        errors = self.current_worker.errors if self.current_worker else []
        success = len(errors) == 0

        if success:
            self._progress_value = 100
            self._progress_message = UIStrings.STATUS_COMPLETED
            self.progressValueChanged.emit()
            self.progressMessageChanged.emit()
            self.toastRequested.emit(UIStrings.MSG_SUCCESS_BODY, "success")
        else:
            msg = UIStrings.STATUS_PARTIAL_ERROR_TEMPLATE.format(count=len(errors))
            self._progress_message = msg
            self.progressMessageChanged.emit()
            self.toastRequested.emit(msg, "error")

        self.batchFinished.emit(success, errors)

    def _on_worker_error(self, err_msg: str):
        logger.error("İşlem hatası: %s", err_msg)
