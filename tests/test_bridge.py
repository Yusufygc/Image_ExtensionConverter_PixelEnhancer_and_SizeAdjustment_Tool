import os
import pytest
from ui.bridge import AppBridge, format_size
from utils.constants import AppConstants

def test_format_size():
    assert "500.0 B" in format_size(500)
    assert "1.0 KB" in format_size(1024)
    assert "1.5 MB" in format_size(int(1.5 * 1024 * 1024))

def test_bridge_initial_state(tmp_path):
    bridge = AppBridge()
    assert bridge.totalCount == 0
    assert bridge.selectedCount == 0
    assert bridge.currentOp == 0
    assert bridge.targetFormat == "PNG"
    assert bridge.resizeType == 0
    assert bridge.resizeWidth == 1920
    assert bridge.resizeHeight == 1080
    assert bridge.resizePercent == 50
    assert bridge.enhanceFactor == 2.0
    assert bridge.isProcessing is False
    assert bridge.viewMode == "grid"

def test_bridge_add_remove_clear_files(tmp_path):
    # Create dummy files
    f1 = tmp_path / "img1.png"
    f1.write_bytes(b"dummy1")
    f2 = tmp_path / "img2.jpg"
    f2.write_bytes(b"dummy222")

    bridge = AppBridge()
    bridge.addFiles([str(f1), str(f2)])

    assert bridge.totalCount == 2
    assert bridge.selectedCount == 0
    assert len(bridge.fileList) == 2

    # Toggle selection
    bridge.toggleFileSelection(str(f1))
    assert bridge.selectedCount == 1

    bridge.selectAllFiles(True)
    assert bridge.selectedCount == 2

    # Remove selected
    bridge.toggleFileSelection(str(f2)) # deselect f2
    assert bridge.selectedCount == 1
    bridge.removeSelectedFiles()
    assert bridge.totalCount == 1
    assert bridge.fileList[0]["path"] == str(f2)

    # Clear all
    bridge.clearFiles()
    assert bridge.totalCount == 0

def test_bridge_sorting(tmp_path):
    f_b = tmp_path / "b.png"
    f_b.write_bytes(b"1000") # 4 bytes
    f_a = tmp_path / "a.png"
    f_a.write_bytes(b"10") # 2 bytes
    f_c = tmp_path / "c.png"
    f_c.write_bytes(b"100000") # 6 bytes

    bridge = AppBridge()
    bridge.addFiles([str(f_b), str(f_a), str(f_c)])

    # Name asc
    bridge.sortFiles("name_asc")
    names = [f["name"] for f in bridge.fileList]
    assert names == ["a.png", "b.png", "c.png"]

    # Name desc
    bridge.sortFiles("name_desc")
    names = [f["name"] for f in bridge.fileList]
    assert names == ["c.png", "b.png", "a.png"]

    # Size asc
    bridge.sortFiles("size_asc")
    sizes = [f["size"] for f in bridge.fileList]
    assert sizes == [2, 4, 6]

    # Size desc
    bridge.sortFiles("size_desc")
    sizes = [f["size"] for f in bridge.fileList]
    assert sizes == [6, 4, 2]

def test_bridge_operation_setters():
    bridge = AppBridge()
    bridge.setCurrentOp(1)
    assert bridge.currentOp == 1
    bridge.setTargetFormat("WEBP")
    assert bridge.targetFormat == "WEBP"
    bridge.setResizeType(1)
    assert bridge.resizeType == 1
    bridge.setResizeWidth(800)
    assert bridge.resizeWidth == 800
    bridge.setResizeHeight(600)
    assert bridge.resizeHeight == 600
    bridge.setResizePercent(75)
    assert bridge.resizePercent == 75
    bridge.setEnhanceFactor(3.0)
    assert bridge.enhanceFactor == 3.0
    bridge.setViewMode("list")
    assert bridge.viewMode == "list"

def test_bridge_processing_flow(tmp_path):
    import time
    from PIL import Image
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])

    test_file = tmp_path / "img_test.png"
    img = Image.new("RGB", (64, 64), color="red")
    img.save(str(test_file))

    out_dir = tmp_path / "converted_out"

    bridge = AppBridge()
    bridge.addFiles([str(test_file)])
    bridge.setCurrentOp(0)
    bridge.setTargetFormat("JPEG")
    bridge.setOutputDir(str(out_dir))

    bridge.startProcessing()

    start_t = time.time()
    while bridge.isProcessing and (time.time() - start_t) < 5:
        app.processEvents()
        time.sleep(0.05)

    assert bridge.fileList[0]["status"] == "success"
    assert (out_dir / "img_test_converted.jpeg").exists()

def test_bridge_toggle_theme():
    bridge = AppBridge()
    init_theme = bridge.currentTheme
    bridge.toggleTheme()
    assert bridge.currentTheme != init_theme
    bridge.toggleTheme()
    assert bridge.currentTheme == init_theme

