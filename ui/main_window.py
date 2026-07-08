import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QFileDialog, QComboBox,
                               QSpinBox, QDoubleSpinBox, QProgressBar, QMessageBox, QGroupBox, QListWidget,
                               QStackedWidget, QListWidgetItem, QLineEdit)
from PySide6.QtCore import Qt, Slot, QSize, QSettings
from PySide6.QtGui import QShortcut, QKeySequence

from ui.widgets.drop_zone import DropZone
from ui.styles.theme import ThemeManager, SETTINGS_ORGANIZATION
from ui.views.info_view import InfoView
from ui.worker import ProcessingWorker
from core.converter import ConverterService
from core.resizer import ResizerService
from core.enhancer import EnhancerService
from ui.widgets.file_list_item import FileListItemWidget
from utils.constants import AppConstants, AppIcons, UISpacing
from utils.strings import UIStrings
from utils.path_helper import get_icon

dir_output_default = os.path.join(os.path.expanduser("~"), "Desktop", "Conventor_Output")

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app_instance = app
        self.setWindowTitle(AppConstants.APP_NAME)
        self.setMinimumSize(AppConstants.WINDOW_WIDTH, AppConstants.WINDOW_HEIGHT)

        # Set Application Icon
        app_icon = get_icon(AppIcons.APP)
        if app_icon:
            self.app_instance.setWindowIcon(app_icon)
            self.setWindowIcon(app_icon)

        # Services
        self.converter_service = ConverterService()
        self.resizer_service = ResizerService()
        self.enhancer_service = EnhancerService()
        self.current_worker = None

        self.selected_files = [] # List of paths
        self.file_item_widgets = {} # file_path -> FileListItemWidget, for per-file status updates
        self.output_dir = dir_output_default

        # Resolve/apply the persisted theme before building widgets, so the
        # header's theme-toggle button starts with the correct icon (no flash).
        ThemeManager.apply_theme(self.app_instance)
        self.setup_ui()
        self._restore_window_geometry()

        QShortcut(QKeySequence("Ctrl+O"), self, activated=self.browse_files)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(UISpacing.LG)
        main_layout.setContentsMargins(UISpacing.XL, UISpacing.XL, UISpacing.XL, UISpacing.XL)

        main_layout.addLayout(self._build_header())

        # Stacked Widget for Pages
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Page 1: Home (Original Content)
        self.page_home = QWidget()
        self.setup_home_page(self.page_home)
        self.stack.addWidget(self.page_home)

        # Page 2: Info
        self.page_info = InfoView()
        self.stack.addWidget(self.page_info)

    def _build_header(self):
        header_layout = QHBoxLayout()

        # Theme Toggle Button (balances the info button on the right)
        self.btn_theme_toggle = QPushButton()
        self.btn_theme_toggle.setFixedSize(40, 40)
        self.btn_theme_toggle.setObjectName("IconOnlyButton")
        self.btn_theme_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_theme_toggle.clicked.connect(self.toggle_theme)
        self._update_theme_toggle_icon()
        header_layout.addWidget(self.btn_theme_toggle)

        header_layout.addStretch() # Spacer Left

        title = QLabel(AppConstants.APP_NAME)
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)

        header_layout.addStretch() # Spacer Right

        # Info Button
        self.btn_info = QPushButton()
        self.btn_info.setFixedSize(40, 40)
        self.btn_info.setObjectName("IconOnlyButton")
        self.btn_info.setCursor(Qt.PointingHandCursor)
        self.btn_info.setToolTip(UIStrings.TOOLTIP_INFO)
        self.btn_info.clicked.connect(self.toggle_info_page)

        info_icon = get_icon(AppIcons.INFO)
        if info_icon:
            self.btn_info.setIcon(info_icon)
            self.btn_info.setIconSize(QSize(24, 24))
        else:
            self.btn_info.setText(UIStrings.FALLBACK_INFO)

        header_layout.addWidget(self.btn_info)
        return header_layout

    def setup_home_page(self, parent_widget):
        layout = QVBoxLayout(parent_widget)
        layout.setContentsMargins(UISpacing.NONE, UISpacing.NONE, UISpacing.NONE, UISpacing.NONE)
        layout.setSpacing(UISpacing.LG)

        layout.addWidget(self._build_file_selection_group(), stretch=1)
        layout.addWidget(self._build_operation_group())
        layout.addLayout(self._build_action_bar())
        layout.addLayout(self._build_progress_section())

    def _build_file_selection_group(self):
        group = QGroupBox(UIStrings.GROUP_FILE_SELECTION)
        h_layout = QHBoxLayout()

        # Left side: Drop Zone + Browse Button
        left_layout = QVBoxLayout()
        self.drop_zone = DropZone()
        self.drop_zone.files_dropped.connect(self.add_files)

        self.btn_browse = QPushButton(UIStrings.BTN_BROWSE)
        self.btn_browse.clicked.connect(self.browse_files)

        left_layout.addWidget(self.drop_zone, stretch=1)
        left_layout.addSpacing(UISpacing.SM)
        left_layout.addWidget(self.btn_browse)

        # Right side: File list + Clear Button
        right_layout = QVBoxLayout()
        lbl_files = QLabel(UIStrings.LBL_SELECTED_FILES)
        lbl_files.setObjectName("SectionLabel")
        right_layout.addWidget(lbl_files)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.NoSelection)
        right_layout.addWidget(self.file_list, stretch=1)

        right_layout.addSpacing(UISpacing.SM)
        self.btn_clear = QPushButton(UIStrings.BTN_CLEAR_FILES)
        self.btn_clear.setObjectName("DangerButton")
        self.btn_clear.setMinimumHeight(40)
        self.btn_clear.setCursor(Qt.PointingHandCursor)
        self.btn_clear.clicked.connect(self.clear_files)
        right_layout.addWidget(self.btn_clear)

        h_layout.addLayout(left_layout, stretch=1)
        h_layout.addSpacing(UISpacing.LG)
        h_layout.addLayout(right_layout, stretch=2)

        group.setLayout(h_layout)
        return group

    def _build_operation_group(self):
        op_group = QGroupBox(UIStrings.GROUP_OPERATION)
        op_layout = QVBoxLayout()

        self._build_option_widgets()
        self._register_operations()

        self.combo_operation = QComboBox()
        self.combo_operation.addItems([op["label"] for op in self.operations])
        self.combo_operation.currentIndexChanged.connect(self.update_options_ui)
        op_layout.addWidget(self.combo_operation)

        self.options_container = QWidget()
        self.options_layout = QVBoxLayout(self.options_container)
        self.options_layout.setContentsMargins(UISpacing.NONE, UISpacing.NONE, UISpacing.NONE, UISpacing.NONE)
        for op in self.operations:
            self.options_layout.addWidget(op["widget"])
        op_layout.addWidget(self.options_container)
        self.update_options_ui(0)

        op_group.setLayout(op_layout)
        return op_group

    def _build_action_bar(self):
        # Output folder + start button apply regardless of the chosen operation,
        # so they live below both columns instead of being squeezed into the
        # (naturally shorter) operation panel.
        action_layout = QVBoxLayout()
        action_layout.addWidget(self._build_output_folder_selector())

        self.btn_process = QPushButton(UIStrings.BTN_PROCESS)
        self.btn_process.setObjectName("PrimaryButton")
        self.btn_process.setMinimumHeight(50)
        self.btn_process.clicked.connect(self.start_processing)
        action_layout.addWidget(self.btn_process)

        return action_layout

    def _build_option_widgets(self):
        # --- Conversion Options ---
        self.widget_convert = QWidget()
        wc_layout = QHBoxLayout(self.widget_convert)
        wc_layout.addWidget(QLabel(UIStrings.LBL_TARGET_FORMAT))
        self.combo_format = QComboBox()
        self.combo_format.addItems(AppConstants.SUPPORTED_FORMATS)
        wc_layout.addWidget(self.combo_format)

        # --- Resize Options ---
        self.widget_resize = QWidget()
        wr_layout = QVBoxLayout(self.widget_resize)

        type_layout = QHBoxLayout()
        self.combo_resize_type = QComboBox()
        self.combo_resize_type.addItems([UIStrings.RESIZE_METHOD_DIMENSIONS, UIStrings.RESIZE_METHOD_PERCENT])
        self.combo_resize_type.currentIndexChanged.connect(self.toggle_resize_inputs)
        type_layout.addWidget(QLabel(UIStrings.LBL_RESIZE_METHOD))
        type_layout.addWidget(self.combo_resize_type)
        wr_layout.addLayout(type_layout)

        self.input_resize_dims = QWidget()
        ird_layout = QHBoxLayout(self.input_resize_dims)
        self.spin_width = QSpinBox()
        self.spin_width.setRange(1, 10000)
        self.spin_width.setValue(1920)
        self.spin_height = QSpinBox()
        self.spin_height.setRange(1, 10000)
        self.spin_height.setValue(1080)
        ird_layout.addWidget(QLabel(UIStrings.LBL_WIDTH))
        ird_layout.addWidget(self.spin_width)
        ird_layout.addWidget(QLabel(UIStrings.LBL_HEIGHT))
        ird_layout.addWidget(self.spin_height)

        self.input_resize_percent = QWidget()
        self.input_resize_percent.setVisible(False)
        irp_layout = QHBoxLayout(self.input_resize_percent)
        self.spin_percent = QSpinBox()
        self.spin_percent.setRange(1, 500)
        self.spin_percent.setValue(50)
        irp_layout.addWidget(QLabel(UIStrings.LBL_PERCENT))
        irp_layout.addWidget(self.spin_percent)

        wr_layout.addWidget(self.input_resize_dims)
        wr_layout.addWidget(self.input_resize_percent)

        # --- Enhance Options ---
        self.widget_enhance = QWidget()
        we_layout = QHBoxLayout(self.widget_enhance)
        we_layout.addWidget(QLabel(UIStrings.LBL_ENHANCE_FACTOR))
        self.spin_factor = QDoubleSpinBox()
        self.spin_factor.setRange(1.1, 4.0)
        self.spin_factor.setSingleStep(0.5)
        self.spin_factor.setValue(2.0)
        we_layout.addWidget(self.spin_factor)

    def _register_operations(self):
        # Single source of truth for the combo box, options panel visibility and
        # kwargs collection - adding a new operation only means appending one entry here.
        self.operations = [
            {
                "label": UIStrings.OP_LABEL_CONVERT,
                "service": self.converter_service,
                "widget": self.widget_convert,
                "collect_kwargs": self._collect_convert_kwargs,
            },
            {
                "label": UIStrings.OP_LABEL_RESIZE,
                "service": self.resizer_service,
                "widget": self.widget_resize,
                "collect_kwargs": self._collect_resize_kwargs,
            },
            {
                "label": UIStrings.OP_LABEL_ENHANCE,
                "service": self.enhancer_service,
                "widget": self.widget_enhance,
                "collect_kwargs": self._collect_enhance_kwargs,
            },
        ]

    def _collect_convert_kwargs(self):
        return {"output_format": self.combo_format.currentText()}

    def _collect_resize_kwargs(self):
        if self.combo_resize_type.currentIndex() == 0:
            return {"width": self.spin_width.value(), "height": self.spin_height.value()}
        return {"percentage": self.spin_percent.value()}

    def _collect_enhance_kwargs(self):
        return {"factor": self.spin_factor.value()}

    def _build_output_folder_selector(self):
        self.widget_output = QWidget()
        wo_layout = QVBoxLayout(self.widget_output)
        wo_layout.setContentsMargins(UISpacing.NONE, UISpacing.SM, UISpacing.NONE, UISpacing.NONE)

        wo_layout.addWidget(QLabel(UIStrings.LBL_TARGET_FOLDER))

        path_layout = QHBoxLayout()
        self.line_output = QLineEdit()
        self.line_output.setPlaceholderText(UIStrings.OUTPUT_PLACEHOLDER)
        self.line_output.setText(self.output_dir)
        self.line_output.setReadOnly(True)

        self.btn_output_select = QPushButton()
        self.btn_output_select.setFixedSize(36, 36)
        self.btn_output_select.setCursor(Qt.PointingHandCursor)
        self.btn_output_select.setToolTip(UIStrings.TOOLTIP_OUTPUT_SELECT)
        self.btn_output_select.clicked.connect(self.select_output_folder)

        folder_icon = get_icon(AppIcons.FOLDER)
        if folder_icon:
            self.btn_output_select.setIcon(folder_icon)
        else:
            self.btn_output_select.setText(UIStrings.FALLBACK_FOLDER)

        path_layout.addWidget(self.line_output)
        path_layout.addWidget(self.btn_output_select)
        wo_layout.addLayout(path_layout)
        return self.widget_output

    def _build_progress_section(self):
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.status_label = QLabel(UIStrings.STATUS_READY)
        progress_layout.addWidget(self.status_label)
        progress_layout.addWidget(self.progress_bar)
        return progress_layout

    def set_app_instance(self, app):
        self.app_instance = app
        ThemeManager.apply_theme(app)

        # Connect DropZone click
        self.drop_zone.clicked.connect(self.browse_files)

    @Slot()
    def toggle_theme(self):
        ThemeManager.toggle_theme(self.app_instance)
        self._update_theme_toggle_icon()

    def _update_theme_toggle_icon(self):
        # Icon/tooltip show the theme a click will switch TO (mirrors toggle_info_page's back-arrow swap).
        if ThemeManager.current_theme == "dark":
            icon = get_icon(AppIcons.THEME_SUN)
            fallback = UIStrings.FALLBACK_THEME_SUN
            tooltip = UIStrings.TOOLTIP_THEME_TOGGLE_TO_LIGHT
        else:
            icon = get_icon(AppIcons.THEME_MOON)
            fallback = UIStrings.FALLBACK_THEME_MOON
            tooltip = UIStrings.TOOLTIP_THEME_TOGGLE_TO_DARK

        if icon:
            self.btn_theme_toggle.setIcon(icon)
            self.btn_theme_toggle.setIconSize(QSize(24, 24))
        else:
            self.btn_theme_toggle.setText(fallback)
        self.btn_theme_toggle.setToolTip(tooltip)

    @Slot()
    def toggle_info_page(self):
        if self.stack.currentIndex() == 0:
            self.stack.setCurrentIndex(1)
            # Switch to Back Arrow
            back_icon = get_icon(AppIcons.BACK_ARROW)
            if back_icon:
                self.btn_info.setIcon(back_icon)
            else:
                self.btn_info.setText(UIStrings.FALLBACK_BACK)
        else:
            self.stack.setCurrentIndex(0)
            # Switch back to Info Icon
            info_icon = get_icon(AppIcons.INFO)
            if info_icon:
                self.btn_info.setIcon(info_icon)
            else:
                self.btn_info.setText(UIStrings.FALLBACK_INFO)

    @Slot()
    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, UIStrings.DIALOG_SELECT_IMAGES_TITLE, "", UIStrings.DIALOG_IMAGE_FILTER)
        if files:
            self.add_files(files)

    @Slot()
    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, UIStrings.DIALOG_SELECT_OUTPUT_FOLDER_TITLE)
        if folder:
            self.output_dir = folder
            self.line_output.setText(folder)

    def add_files(self, file_paths):
        for path in file_paths:
            if path not in self.selected_files:
                self.selected_files.append(path)

                # Add Item to List Widget using Custom Widget
                item = QListWidgetItem(self.file_list)
                item.setSizeHint(QSize(0, 68)) # Set height for the item (48px thumbnail + padding)

                item_widget = FileListItemWidget(path)
                item_widget.remove_clicked.connect(self.remove_file)
                self.file_item_widgets[path] = item_widget

                self.file_list.setItemWidget(item, item_widget)

    def remove_file(self, file_path):
        if file_path in self.selected_files:
            self.selected_files.remove(file_path)
            self.file_item_widgets.pop(file_path, None)

            # Find and remove from list widget
            # Efficient way: iterate and find match (since we don't have direct mapping)
            for i in range(self.file_list.count()):
                item = self.file_list.item(i)
                widget = self.file_list.itemWidget(item)
                if widget and widget.file_path == file_path:
                    self.file_list.takeItem(i)
                    break

    def clear_files(self):
        self.selected_files.clear()
        self.file_item_widgets.clear()
        self.file_list.clear()

    @Slot(int)
    def update_options_ui(self, index):
        for i, op in enumerate(self.operations):
            op["widget"].setVisible(i == index)

    @Slot(int)
    def toggle_resize_inputs(self, index):
        self.input_resize_dims.setVisible(index == 0)
        self.input_resize_percent.setVisible(index == 1)

    @Slot()
    def start_processing(self):
        if not self.selected_files:
            QMessageBox.warning(self, UIStrings.MSG_WARNING_TITLE, UIStrings.MSG_NO_FILES_SELECTED)
            return

        operation_idx = self.combo_operation.currentIndex()
        op = self.operations[operation_idx]
        service = op["service"]
        kwargs = op["collect_kwargs"]()

        # Add output dir
        if self.output_dir:
            kwargs['output_dir'] = self.output_dir

        for widget in self.file_item_widgets.values():
            widget.set_status("")

        self.btn_process.setEnabled(False)
        self.current_worker = ProcessingWorker(service, self.selected_files, **kwargs)
        self.current_worker.signals.progress.connect(self.update_progress)
        self.current_worker.signals.finished.connect(self.processing_finished)
        self.current_worker.signals.error.connect(self.processing_error)
        self.current_worker.signals.file_started.connect(self.on_file_started)
        self.current_worker.signals.file_done.connect(self.on_file_done)
        self.current_worker.start()

    def on_file_started(self, file_path):
        widget = self.file_item_widgets.get(file_path)
        if widget:
            widget.set_status("processing")

    def on_file_done(self, file_path, success):
        widget = self.file_item_widgets.get(file_path)
        if widget:
            widget.set_status("success" if success else "error")

    def update_progress(self, val, msg):
        self.progress_bar.setValue(val)
        self.status_label.setText(msg)

    def processing_finished(self):
        self.btn_process.setEnabled(True)
        errors = self.current_worker.errors if self.current_worker else []
        if errors:
            self.status_label.setText(UIStrings.STATUS_PARTIAL_ERROR_TEMPLATE.format(count=len(errors)))
            QMessageBox.warning(self, UIStrings.MSG_PARTIAL_ERROR_TITLE,
                UIStrings.MSG_PARTIAL_ERROR_BODY_PREFIX + "\n".join(errors))
        else:
            self.status_label.setText(UIStrings.STATUS_COMPLETED)
            QMessageBox.information(self, UIStrings.MSG_SUCCESS_TITLE, UIStrings.MSG_SUCCESS_BODY)

    def processing_error(self, err_msg):
        self.status_label.setText(UIStrings.STATUS_ERROR_GENERIC)
        QMessageBox.critical(self, UIStrings.MSG_ERROR_TITLE, err_msg)

    def _window_settings(self):
        return QSettings(SETTINGS_ORGANIZATION, AppConstants.APP_NAME)

    def _restore_window_geometry(self):
        geometry = self._window_settings().value("window_geometry")
        if geometry:
            self.restoreGeometry(geometry)

    def closeEvent(self, event):
        self._window_settings().setValue("window_geometry", self.saveGeometry())

        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.stop()
            self.current_worker.wait(3000)
        event.accept()
