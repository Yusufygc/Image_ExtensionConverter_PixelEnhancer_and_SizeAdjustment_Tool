import os
import pytest
from PIL import Image
from core.converter import ConverterService


def test_convert_rgba_to_jpeg_drops_alpha(rgba_png, tmp_path):
    service = ConverterService()
    output_dir = str(tmp_path / "out")
    output_path = service.convert(rgba_png, "JPEG", output_dir=output_dir)

    assert os.path.exists(output_path)
    with Image.open(output_path) as img:
        assert img.mode == "RGB"


def test_convert_to_ico_contains_multiple_sizes(rgb_png, tmp_path):
    service = ConverterService()
    output_dir = str(tmp_path / "out")
    output_path = service.convert(rgb_png, "ICO", output_dir=output_dir)

    with Image.open(output_path) as img:
        sizes = img.info.get("sizes") or [img.size]
        assert len(sizes) >= 2


def test_convert_missing_file_raises(tmp_path):
    service = ConverterService()
    with pytest.raises(FileNotFoundError):
        service.convert(str(tmp_path / "nope.png"), "PNG")
