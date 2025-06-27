import cv2
from .base_detector import BaseDetector
from src.core.utils.logger import get_logger
from src.core.models.detection_result import DetectionResult
from src.core.models.movement_type import MovementType

logger = get_logger()

class ORBDetector(BaseDetector):
    """
    A detector class that identifies significant movement using ORB (Oriented FAST and Rotated BRIEF).
    The ORB algorithm detects keypoints in frames and matches them between consecutive frames.
    Significant movement is detected when the number of keypoint matches exceeds a certain threshold.

    Args:
        threshold (int): The minimum number of keypoint matches to consider as significant movement.
    """
    
    def __init__(self, threshold=30):
        """
        Initializes the ORBDetector with the given threshold.

        Args:
            threshold (int): The threshold value for detecting significant movement based on keypoint matches.
        """
        self.orb = cv2.ORB_create()
        self.threshold = threshold
        logger.info(f"ORBDetector initialized with threshold={threshold}.")

    def detect(self, frames):
        """
        Detects significant movement in a list of frames using ORB keypoints and descriptor matching.

        The method computes keypoints and descriptors for each frame and matches them between consecutive frames.
        If the number of keypoint matches exceeds the threshold, movement is detected.

        Args:
            frames (list): A list of frames (images) to process for detecting movement.

        Returns:
            list: A list of `DetectionResult` objects containing the detected movements, with frame indices,
                  movement type, and score (number of keypoint matches).
        """
        logger.info(f"Starting ORB detection on {len(frames)} frames.")
        results = []
        prev_kp, prev_des = None, None

        for idx, frame in enumerate(frames):
            kp, des = self.orb.detectAndCompute(frame, None)
            if prev_kp is not None and prev_des is not None and des is not None:
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(prev_des, des)
                match_count = len(matches)
                logger.debug(f"Frame {idx}: {match_count} matches found.")

                if match_count > self.threshold:
                    logger.info(f"Significant movement detected at frame {idx}")
                    results.append(
                        DetectionResult(
                            frame_index=idx,
                            movement_type=MovementType.TRANSLATION,
                            score=float(match_count)
                        )
                    )
            prev_kp, prev_des = kp, des

        logger.info(f"ORB detection complete. Movement detected {len(results)} frames")
        return results
