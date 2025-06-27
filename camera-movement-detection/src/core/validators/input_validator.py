import os
from src.core.exceptions.custom_exceptions import InvalidInputException
from src.core.utils.logger import get_logger

logger = get_logger()

class InputValidator:
    """
    A class for validating uploaded files, ensuring they meet the required type, number, and video count constraints.

    Args:
        allowed_types (dict): A dictionary defining the allowed file types for images and videos.
        min_files (int): The minimum number of files that must be uploaded.
        max_files (int): The maximum number of files that can be uploaded.
        max_videos (int): The maximum number of video files that can be uploaded.
    """
    def __init__(self, allowed_types=None, min_files=1, max_files=100, max_videos=5):
        """
        Initializes the InputValidator with the provided settings.

        Args:
            allowed_types (dict): The allowed file types for images and videos.
            min_files (int): Minimum number of files allowed to upload.
            max_files (int): Maximum number of files allowed to upload.
            max_videos (int): Maximum number of video files allowed to upload.
        """
        self.allowed_types = allowed_types or {
            "images": ["jpg", "jpeg", "png"],
            "videos": ["mp4", "avi"]
        }

        self.min_files = min_files
        self.max_files = max_files
        self.max_videos = max_videos

        logger.info(
            f"InputValidator initialized. "
            f"Allowed types: {self.allowed_types}, "
            f"Min files: {self.min_files}, "
            f"Max files: {self.max_files}, "
            f"Max videos: {self.max_videos}"
        )

    def get_file_extension(self, file):
        """
        Extracts the file extension from a given file.

        Args:
            file: The file for which the extension is to be extracted. Can be a file object or a string.

        Returns:
            str: The file extension (without dot) in lowercase.
        """
        if hasattr(file, 'name'):
            return os.path.splitext(file.name)[-1].lower().replace('.', '')
        else:
            return os.path.splitext(file)[-1].lower().replace('.', '')

    def is_video(self, file):
        """
        Checks if the provided file is a video based on its extension.

        Args:
            file: The file to check.

        Returns:
            bool: True if the file is a video, False otherwise.
        """
        ext = self.get_file_extension(file)
        logger.debug(f"Checking if file is video: {file} (Extension: .{ext})")
        return ext in self.allowed_types.get("videos", [])

    def is_image(self, file):
        """
        Checks if the provided file is an image based on its extension.

        Args:
            file: The file to check.

        Returns:
            bool: True if the file is an image, False otherwise.
        """
        ext = self.get_file_extension(file)
        logger.debug(f"Checking if file is image: {file} (Extension: .{ext})")
        return ext in self.allowed_types.get("images", [])

    def validate_files(self, uploaded_files):
        """
        Validates a list of uploaded files based on file count, type, and video count restrictions.

        Args:
            uploaded_files (list): A list of uploaded files to validate.

        Raises:
            InvalidInputException: If any validation fails (e.g., wrong file count, unsupported file type, etc.).
        """
        logger.info(f"Validating {len(uploaded_files) if uploaded_files else 0} files...")

        if not uploaded_files:
            logger.warning("No files uploaded.")
            raise InvalidInputException("No files uploaded. Please select at least one file.")

        if not (self.min_files <= len(uploaded_files) <= self.max_files):
            logger.warning(f"File count {len(uploaded_files)} out of allowed range ({self.min_files}-{self.max_files}).")
            raise InvalidInputException(f"Please upload between {self.min_files} and {self.max_files} files.")

        video_files = [f for f in uploaded_files if self.is_video(f)]
        if len(video_files) > self.max_videos:
            logger.warning(f"Too many video files uploaded: {len(video_files)} (max {self.max_videos})")
            raise InvalidInputException(f"Maximum {self.max_videos} video files can be uploaded.")

        all_valid_types = self.allowed_types.get("images", []) + self.allowed_types.get("videos", [])

        for file in uploaded_files:
            ext = self.get_file_extension(file)
            logger.debug(f"Checking file type: {file} (.{ext})")

            if ext not in all_valid_types:
                logger.warning(f"Invalid file type: {file} (Allowed: {all_valid_types})")
                raise InvalidInputException(f"File type not allowed: {file} (Allowed Types: {all_valid_types})")

        logger.info("All files passed validation.")
