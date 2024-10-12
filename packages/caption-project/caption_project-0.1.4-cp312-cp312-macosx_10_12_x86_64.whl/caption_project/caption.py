from pathlib import Path
from caption_project.image import BaseImage
from caption_project._lowlevel import caption_image


class ImageCaption(BaseImage):
    def __init__(self, image_path: Path):
        super().__init__(image_path)
        self._caption: str | None = None

    @property
    def caption(self) -> str:
        if not self._caption:
            with self.get_temp_file() as temp_file:
                self._caption = caption_image(temp_file.name)

        return self._caption
