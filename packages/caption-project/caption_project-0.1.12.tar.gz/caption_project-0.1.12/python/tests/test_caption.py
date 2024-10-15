from .utils import base_path
import os
import pytest

IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


test_cases = [("4275"), ("5778"), ("5790"), ("5865"), ("5912"), ("7357"), ("7366")]

@pytest.mark.skipif(IN_GITHUB_ACTIONS, reason="Temporarily disabling in GitHub Actions")
def test_results():
    from caption_project.caption import ImageCaption

    for case in test_cases:
        image_path = base_path / f"IMG_{case}.HEIC"

        image = ImageCaption(image_path)
        res = image.caption
        print("RES", res)
        assert res is not None
