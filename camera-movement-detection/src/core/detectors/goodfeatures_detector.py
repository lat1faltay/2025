import cv2
import numpy as np
from src.core.detectors.base_detector import BaseDetector
from src.core.models.detection_result import DetectionResult
from src.core.models.movement_type import MovementType
from src.core.utils.logger import get_logger

logger = get_logger()

class GoodFeaturesDetector(BaseDetector):
    """
    A detector class that identifies significant movement in frames using the good features-to-track method.
    This method uses corner detection to track features between consecutive frames, and detects movement based on feature count changes.
    """
    
    def __init__(self, threshold=100):
        """
        Initializes the detector with the given threshold for feature count difference.

        Args:
            threshold (int): The threshold value for detecting significant movement based on feature count difference.
        """
        self.threshold = threshold

    def detect(self, frames):
        """
        Detects significant movement in a list of frames using the good features-to-track method.

        The method compares the number of good features detected in consecutive frames and registers movement if 
        the difference in feature count exceeds a certain threshold.

        Args:
            frames (list): A list of frames (images) to process for detecting movement.

        Returns:
            list: A list of `DetectionResult` objects containing the detected movements, with frame indices,
                  movement type, and score (difference in feature count).
        """
        logger.info("GoodFeaturesDetector started.")
        results = []
        prev_pts = None
        prev_gray = None
        diff = 0 

        for idx, frame in enumerate(frames):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            pts = cv2.goodFeaturesToTrack(gray, maxCorners=200, qualityLevel=0.01, minDistance=30)

            if prev_pts is not None and pts is not None:
                diff = abs(len(pts) - len(prev_pts)) 

                logger.info(f"Frame {idx}: Feature count difference = {diff}")

            if diff > self.threshold:
                if diff < self.threshold * 1.5:
                    movement_type = MovementType.TRANSLATION
                else:
                    movement_type = MovementType.OBJECT

                results.append(DetectionResult(
                    frame_index=idx,
                    movement_type=movement_type,
                    score=float(diff)
                ))

            prev_pts = pts
            prev_gray = gray

        return results
