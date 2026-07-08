import pytest
from utils.image_loader import load_image


def test_load_image_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_image(str(tmp_path / "nope.png"))


def test_load_image_invalid_content_raises(tmp_path):
    bad_file = tmp_path / "not_an_image.png"
    bad_file.write_text("this is not image data")
    with pytest.raises(Exception):
        load_image(str(bad_file))


def test_load_image_valid_png(rgb_png):
    img = load_image(rgb_png)
    try:
        assert img.size == (80, 40)
    finally:
        img.close()
