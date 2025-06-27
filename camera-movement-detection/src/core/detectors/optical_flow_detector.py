import cv2
import numpy as np
from src.core.utils.logger import get_logger
from src.core.models.detection_result import DetectionResult
from src.core.models.movement_type import MovementType
from src.core.detectors.base_detector import BaseDetector

logger = get_logger()

class OpticalFlowDetector(BaseDetector):
    """
    A detector class that identifies significant movement using optical flow.
    The optical flow method tracks the movement of feature points between consecutive frames.

    Args:
        threshold (float): The threshold value for detecting movement based on the mean movement of feature points.
    """
    
    def __init__(self, threshold: float = 2.0):
        """
        Initializes the OpticalFlowDetector with the given threshold.

        Args:
            threshold (float): The threshold value to detect movement based on the mean movement of feature points.
        """
        self.threshold = threshold

    def detect(self, frames):
        """
        Detects significant movement in a list of frames using optical flow.

        The method tracks the movement of feature points between consecutive frames using the Lucas-Kanade optical flow algorithm.
        If the mean movement of valid points exceeds the threshold, movement is detected.

        Args:
            frames (list): A list of frames (images) to process for detecting movement.

        Returns:
            list: A list of `DetectionResult` objects containing the detected movements, with frame indices,
                  movement type, and score (mean movement).
        """
        logger.info("OpticalFlowDetector started.")
        detected = []
        prev_gray = None
        prev_points = None

        # Iterate through each frame to detect movement
        for idx, frame in enumerate(frames):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            logger.debug(f"Frame {idx} converted to grayscale.")

            if prev_gray is not None and prev_points is not None:
                # Calculate optical flow between previous and current frame
                next_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_points, None)

                if next_points is not None and status is not None:
                    movement = np.abs(next_points - prev_points)
                    valid_movement = movement[status.flatten() == 1]
                    mean_movement = valid_movement.mean() if len(valid_movement) > 0 else 0.0

                    logger.debug(f"Frame {idx}: mean movement = {mean_movement:.4f}")

                    # Detect movement if mean movement exceeds the threshold
                    if mean_movement > self.threshold:
                        logger.info(f"Movement detected at frame {idx} with score {mean_movement:.2f}")
                        detected.append(DetectionResult(
                            frame_index=idx,
                            movement_type=MovementType.SHIFT,
                            score=float(mean_movement)
                        ))

            # Track new feature points in the current frame
            prev_gray = gray
            prev_points = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.3, minDistance=7)
            if prev_points is not None:
                logger.debug(f"Frame {idx}: {len(prev_points)} keypoints detected.")
            else:
                logger.debug(f"Frame {idx}: No keypoints detected.")

        logger.info(f"OpticalFlowDetector completed. Detected {len(detected)} frame(s).")
        return detected
