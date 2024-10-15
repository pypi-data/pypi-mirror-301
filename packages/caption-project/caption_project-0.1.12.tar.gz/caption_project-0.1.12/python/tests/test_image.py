

from .utils import base_path
from caption_project.image import BaseImage




def test_image():
    
    image_path = base_path / "IMG_5778.HEIC"
    # print(image_path.absolute().as_posix())    
    image = BaseImage(image_path)
    assert image.get_extension() == ".HEIC"
    assert image.get_image() is not None
    assert image.get_image_id() == "5778"
    assert image.get_image_name() == "IMG_5778"

    temp_file = image.get_temp_file()
    assert temp_file is not None
    print(temp_file.name)