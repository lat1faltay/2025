import cv2
import tempfile
import numpy as np
from src.core.utils.logger import get_logger
import os

logger = get_logger()

class Extractor:
    """
    A class for extracting frames from video files or image files.

    Args:
        max_frames_per_video (int): The maximum number of frames to extract from each video (default is 1000).
    """
    def __init__(self, max_frames_per_video=1000):
        """
        Initializes the Extractor with the specified maximum number of frames per video and a temporary directory.

        Args:
            max_frames_per_video (int): The maximum number of frames to extract from each video.
        """
        self.temp_dir = tempfile.mkdtemp()
        self.max_frames = max_frames_per_video
        logger.info(f"Extractor initialized with temp directory: {self.temp_dir} and max frames: {self.max_frames}")

    def extract_frames_from_video(self, video_file):
        """
        Extracts frames from a video file. It supports both video file paths and file-like objects.

        Args:
            video_file: The video file (either a file path or a file-like object) from which frames will be extracted.

        Returns:
            list: A list of frames extracted from the video.
        """
        if hasattr(video_file, "read"):  # Check if the video file is a file-like object
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(video_file.read())  
                tmp_path = tmp.name  
            cap = cv2.VideoCapture(tmp_path) 
        else:
            cap = cv2.VideoCapture(video_file)

        frames = []
        count = 0
        while count < self.max_frames:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
            count += 1

        cap.release()
        logger.info(f"Extracted {len(frames)} frames from video: {video_file.name if hasattr(video_file, 'name') else video_file}")
        return frames

    def extract_frames_from_images(self, image_files):
        """
        Extracts frames from a list of image files.

        Args:
            image_files (list): A list of image files (file-like objects) to extract frames from.

        Returns:
            list: A list of frames extracted from the images.
        """
        frames = []
        for image_file in image_files:
            try:
                image_file.seek(0)  # Reset file pointer
                file_bytes = image_file.read()  # Read the image content
                if not file_bytes:
                    logger.warning(f"Empty file: {image_file.name}")
                    continue
                
                np_arr = np.frombuffer(file_bytes, np.uint8)
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                
                if frame is None:
                    logger.warning(f"Failed to decode image: {image_file.name}")
                    continue
                
                frames.append(frame)
            except Exception as e:
                logger.warning(f"Error processing file {image_file.name}: {e}")

        logger.info(f"Extracted {len(frames)} frames from images.")
        return frames

    def get_file_extension(self, file):
        """
        Gets the file extension from a file-like object or file path.

        Args:
            file: The file object or file path to extract the extension from.

        Returns:
            str: The file extension (lowercase).
        """
        if hasattr(file, 'name'):
            return os.path.splitext(file.name)[-1].lower().replace('.', '')
        else:
            logger.warning("File does not have a 'name' attribute")
            return ""
