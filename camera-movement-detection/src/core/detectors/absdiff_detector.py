import cv2
from .base_detector import BaseDetector
from src.core.utils.logger import get_logger
from src.core.models.detection_result import DetectionResult
from src.core.models.movement_type import MovementType

logger = get_logger()

class AbsDiffDetector(BaseDetector):
    """
    A detector class that uses absolute difference (AbsDiff) method for detecting movement between frames.
    This detector compares consecutive frames and detects movement if the difference exceeds a certain threshold.

    Args:
        threshold (int): The threshold value for detecting movement based on the difference in pixel values (default is 50000).
        threshold_value (int): The pixel intensity threshold for binarizing the absolute difference (default is 25).
    """

    def __init__(self, threshold=50000, threshold_value=25):
        """
        Initializes the AbsDiffDetector with given thresholds.

        Args:
            threshold (int): The minimum number of non-zero pixels in the thresholded difference to register as movement.
            threshold_value (int): The threshold value used to create a binary image from the absolute difference.
        """
        self.threshold = threshold
        self.threshold_value = threshold_value
        logger.info(f"AbsDiffDetector initialized with threshold: {self.threshold}, threshold_value: {self.threshold_value}")


    def detect(self, frames):
        """
        Detects movement in a sequence of frames using the absolute difference method. It compares each frame 
        with the previous one and registers movement if the difference exceeds the set thresholds.

        Args:
            frames (list): A list of frames (images) to process for movement detection.

        Returns:
            list: A list of `DetectionResult` objects containing the frame index, movement type, and score (non-zero pixel count).
        """
        logger.info(f"Starting AbsDiff detection on {len(frames)} frames.")
        results = []
        prev_frame = None

        # Iterate through frames and compare each with the previous frame
        for idx, frame in enumerate(frames):
            logger.debug(f"Processing frame index: {idx}")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if prev_frame is not None:
                # Compute the absolute difference between consecutive frames
                diff = cv2.absdiff(prev_frame, gray)
                _, thresh = cv2.threshold(diff, self.threshold_value, 255, cv2.THRESH_BINARY)
                non_zero = cv2.countNonZero(thresh)
                logger.debug(f"Frame {idx}: non-zero diff count = {non_zero}")

                if non_zero > self.threshold:  # Check if movement is detected
                    logger.info(f"Movement detected at frame {idx} (diff count: {non_zero})")
                    results.append(
                        DetectionResult(
                            frame_index=idx,
                            movement_type=MovementType.TRANSLATION,
                            score=float(non_zero)
                        )
                    )

            prev_frame = gray

        logger.info(f"AbsDiff detection complete. Movement detected at frames: {results}")
        return results
