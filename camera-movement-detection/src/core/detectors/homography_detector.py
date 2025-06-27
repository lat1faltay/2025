import cv2
import numpy as np
from src.core.detectors.base_detector import BaseDetector
from src.core.models.detection_result import DetectionResult
from src.core.models.movement_type import MovementType
from src.core.utils.logger import get_logger

logger = get_logger()

class HomographyDetector(BaseDetector):
    """
    A detector class that identifies significant movement using homography.
    The homography method compares two sets of feature points in consecutive frames 
    and calculates a transformation matrix to identify motion.

    Args:
        threshold (float): The threshold value for determining the type of movement based on homography score.
    """
    
    def __init__(self, threshold=5.0):
        """
        Initializes the HomographyDetector with the given threshold.

        Args:
            threshold (float): The threshold value for detecting movement. Used to determine the movement type.
        """
        self.threshold = threshold  

    def detect(self, frames):
        """
        Detects significant movement between consecutive frames using homography.

        The method matches feature points between consecutive frames using optical flow and 
        calculates the homography matrix to assess movement.

        Args:
            frames (list): A list of frames (images) to process for detecting movement.

        Returns:
            list: A list of `DetectionResult` objects containing the detected movements, with frame indices,
                  movement type, and score.
        """
        logger.info("HomographyDetector started.")
        results = []
        prev_gray = None

        for idx, frame in enumerate(frames):
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if prev_gray is not None:
                prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=200, qualityLevel=0.01, minDistance=30)

                if prev_pts is not None:
                    next_pts, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_pts, None)

                    matched_prev = prev_pts[status.flatten() == 1]
                    matched_next = next_pts[status.flatten() == 1]

                    if len(matched_prev) > 10:
                        H, mask = cv2.findHomography(matched_prev, matched_next, cv2.RANSAC, self.threshold)
                        inliers = np.sum(mask)
                        total = len(mask)
                        score = 1 - (inliers / total)

                        logger.info(f"Frame {idx}: homography score = {score:.2f}")

                        if score < 0.1:
                            movement_type = MovementType.TRANSLATION
                        elif score <= self.threshold:
                            movement_type = MovementType.CAMERA
                        else:
                            movement_type = MovementType.OBJECT

                        results.append(DetectionResult(
                            frame_index=idx,
                            movement_type=movement_type,
                            score=score
                        ))

            prev_gray = gray

        return results

def draw_matches(frame, points):
    """
    Draws circles on the given frame at the specified points.

    Args:
        frame (numpy.ndarray): The frame (image) to draw the points on.
        points (numpy.ndarray): The points to mark on the frame.

    Returns:
        numpy.ndarray: The frame with the drawn circles at the points.
    """
    for pt in points:
        x, y = pt.ravel()
        cv2.circle(frame, (int(x), int(y)), radius=4, color=(0, 255, 0), thickness=-1)
    return frame
