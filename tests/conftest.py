import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from PIL import Image


@pytest.fixture
def rgba_png(tmp_path):
    path = tmp_path / "sample_rgba.png"
    img = Image.new("RGBA", (100, 60), (255, 0, 0, 128))
    img.save(path)
    return str(path)


@pytest.fixture
def rgb_png(tmp_path):
    path = tmp_path / "sample_rgb.png"
    img = Image.new("RGB", (80, 40), (0, 255, 0))
    img.save(path)
    return str(path)
