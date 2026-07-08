from PIL import Image
from core.enhancer import EnhancerService


def test_enhance_resolution_scales_by_factor(rgb_png, tmp_path):
    service = EnhancerService()
    output_dir = str(tmp_path / "out")
    output_path = service.enhance_resolution(rgb_png, 2.0, output_dir=output_dir)

    with Image.open(output_path) as img:
        # source is 80x40
        assert img.size == (160, 80)
