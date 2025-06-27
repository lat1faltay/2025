import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.core.validators.input_validator import InputValidator
from src.core.exceptions.custom_exceptions import InvalidInputException

def test_invalid_file_type():
    """
    Test that verifies the InputValidator raises an InvalidInputException for unsupported file types.

    This test checks that when an unsupported image or video file type is uploaded, 
    the appropriate exception is raised with the correct error message.
    """
    validator = InputValidator(allowed_types={"images": ["jpg", "jpeg", "png"], "videos": ["mp4", "avi"]})

    invalid_image = "image.bmp"
    invalid_video = "video.mov"

    # Test for invalid image file type
    with pytest.raises(InvalidInputException) as exc_info:
        validator.validate_files([invalid_image])
    assert str(exc_info.value) == f"File type not allowed: {invalid_image} (Allowed Types: ['jpg', 'jpeg', 'png', 'mp4', 'avi'])"
    
    # Test for invalid video file type
    with pytest.raises(InvalidInputException) as exc_info:
        validator.validate_files([invalid_video])
    assert str(exc_info.value) == f"File type not allowed: {invalid_video} (Allowed Types: ['jpg', 'jpeg', 'png', 'mp4', 'avi'])"
