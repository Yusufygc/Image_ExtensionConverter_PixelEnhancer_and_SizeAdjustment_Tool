from PIL import Image
from core.resizer import ResizerService


def test_resize_by_percentage_scales_pixels(rgb_png, tmp_path):
    service = ResizerService()
    output_dir = str(tmp_path / "out")
    output_path = service.resize_by_percentage(rgb_png, 50, output_dir=output_dir)

    with Image.open(output_path) as img:
        # source is 80x40
        assert img.size == (40, 20)


def test_resize_by_dimensions_exact(rgb_png, tmp_path):
    service = ResizerService()
    output_dir = str(tmp_path / "out")
    output_path = service.resize_by_dimensions(rgb_png, 33, 17, output_dir=output_dir)

    with Image.open(output_path) as img:
        assert img.size == (33, 17)
