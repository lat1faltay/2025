import logging
import tempfile
from src.core.utils.queue_manager import QueueManager

logger = logging.getLogger(__name__)

class MovementDetector:
    """
    A class for detecting movement in frames and videos using multiple detectors.

    Args:
        factory: The detector factory used to create detectors.
        max_video_queue (int): The maximum number of videos allowed in the video queue (default is 5).
        max_frame_queue (int): The maximum number of frames allowed in the frame queue (default is 100).
    """
    def __init__(self, factory, max_video_queue=5, max_frame_queue=100):
        """
        Initializes the MovementDetector with specified video and frame queue sizes.

        Args:
            factory: The detector factory used to create detectors.
            max_video_queue (int): The maximum number of videos allowed in the video queue.
            max_frame_queue (int): The maximum number of frames allowed in the frame queue.
        """
        self.factory = factory
        self.video_queue = QueueManager(max_size=max_video_queue)
        self.frame_queue = QueueManager(max_size=max_frame_queue)
        self.detectors = []  # List to hold the detectors created by the factory

    def enqueue_video(self, video_file):
        """
        Adds a video file to the video queue.

        Args:
            video_file: The video file to be added to the queue.

        Returns:
            bool: Returns `True` if the video was successfully enqueued, `False` if the queue was full.
        """
        if not self.video_queue.enqueue(video_file):
            logger.warning(f"Video queue full. Skipped video: {video_file.name}")
            return False
        logger.info(f"Video enqueued: {video_file.name}")
        return True

    def enqueue_frames(self, frames):
        """
        Adds frames to the frame queue.

        Args:
            frames: A list of frames to be added to the queue.
        """
        for frame in frames:
            if not self.frame_queue.enqueue(frame):
                logger.warning("Frame queue full. Stopping frame enqueue.")
                break
        logger.info(f"Enqueued frames to frame queue.")

    def set_detectors(self, detectors_with_thresholds: dict):
        """
        Sets the detectors with specified thresholds.

        Args:
            detectors_with_thresholds (dict): A dictionary of detector names and their corresponding threshold values.
            Example: {"orb": 30, "absdiff": 50000}
        """
        self.detectors.clear()
        for detector_name, threshold in detectors_with_thresholds.items():
            self.factory.config.detector.default = detector_name
            if threshold is not None:
                if detector_name.lower() == "absdiff":
                    self.factory.set_absdiff_threshold(threshold)
                elif detector_name.lower() == "orb":
                    self.factory.set_orb_threshold(threshold)
                elif detector_name.lower() == "opticalflow":
                    self.factory.set_opticalflow_threshold(threshold)
                elif detector_name.lower() == "homography":
                    self.factory.set_homography_threshold(threshold)
                elif detector_name.lower() == "goodfeatures":
                    self.factory.set_goodfeatures_threshold(threshold)
                logger.info(f"Threshold set to {threshold} for detector {detector_name}")
            detector_instance = self.factory.create_detector()
            self.detectors.append(detector_instance)
        logger.info(f"Total detectors set: {len(self.detectors)}")

    def process_frames(self):
        """
        Processes frames in the frame queue and applies all detectors to them.

        Returns:
            list: A list of results, each containing the detector's name and the movement events detected.
        """
        frame_list = []
        while not self.frame_queue.is_empty():
            frame_list.append(self.frame_queue.dequeue())

        if not self.detectors:
            logger.error("No detectors set before processing frames!")
            return []

        all_results = []
        logger.info(f"Detecting movement on {len(frame_list)} frames with {len(self.detectors)} detectors.")
        for detector in self.detectors:
            results = detector.detect(frame_list)
            logger.info(f"Detector {detector.__class__.__name__} found {len(results)} movement events.")
            all_results.append((detector.__class__.__name__, results))

        return all_results

    def process_videos(self, extractor):
        """
        Processes videos in the video queue, extracting frames and applying detectors.

        Args:
            extractor: The extractor instance used to extract frames from videos.

        Returns:
            list: A list of results for each video processed, including frames and movement detections.
        """
        results_per_file = []
        while not self.video_queue.is_empty():
            video_file = self.video_queue.dequeue()
            logger.info(f"Processing video: {video_file.name}")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(video_file.read())
                temp_video_path = tmp.name

            frames = extractor.extract_frames_from_video(temp_video_path)
            self.frame_queue.clear()
            self.enqueue_frames(frames)

            detector_results = self.process_frames()
            results_per_file.append((video_file.name, frames, detector_results))
        return results_per_file

    def process_images(self, image_files, extractor):
        """
        Processes images, extracting frames and applying detectors.

        Args:
            image_files: A list of image files to process.
            extractor: The extractor instance used to extract frames from images.

        Returns:
            list: A list containing the results of the detection for the uploaded images.
        """
        frames = extractor.extract_frames_from_images(image_files)
        self.frame_queue.clear()
        self.enqueue_frames(frames)
        detector_results = self.process_frames()
        return [("Uploaded Images", frames, detector_results)]
