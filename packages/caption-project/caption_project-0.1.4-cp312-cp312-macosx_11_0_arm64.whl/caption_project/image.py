from pathlib import Path

from PIL import Image
from tempfile import NamedTemporaryFile


class BaseImage:
    """
    BaseImage class for handling image operations.
    Attributes:
        image_path (Path): Path to the image file.
    Methods:
        __init__(image_path: Path):
            Initializes the BaseImage instance with the given image path.
        get_extension():
            Returns the file extension of the image.
        convert_heic_to_jpg():
            Converts a HEIC image to a JPG image using the pyheif library.
            Returns:
                Image: The converted JPG image.
        get_temp_file(extension: str = ".jpg"):
            Creates a temporary file with the specified extension and saves the image to it.
            Returns:
                NamedTemporaryFile: The temporary file containing the image.
        get_image_name():
            Returns the name of the image file without the extension.
        get_image_id():
            Extracts and returns the image ID from the image name, assuming the ID is the second part of the name when split by an underscore.
        get_image():
            Opens and returns the image using the appropriate method based on the file extension.
            Raises:
                ValueError: If the image format is not supported.
    """

    def __init__(self, image_path: Path):
        self.image_path = image_path

    def get_extension(self):
        return self.image_path.suffix

    def convert_heic_to_jpg(self):
        import pyheif

        heif_file = pyheif.read(self.image_path)
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )
        return image

    def get_temp_file(self, extension: str = ".jpg"):
        file_path = NamedTemporaryFile(suffix=extension)
        image = self.get_image()

        image.save(file_path.name)

        return file_path

    def get_image_name(self):
        return self.image_path.stem

    def get_image_id(self):
        name = self.get_image_name()
        return name.split("_")[1]

    def get_image(self):
        if self.get_extension() in [".jpg", ".jpeg", ".png"]:
            return Image.open(self.image_path)
        elif self.get_extension() in [".heic", ".HEIC"]:
            return self.convert_heic_to_jpg()
        else:
            raise ValueError("Invalid image format")
