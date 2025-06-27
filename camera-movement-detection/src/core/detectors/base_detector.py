from abc import ABC, abstractmethod
from typing import List
from src.core.models.detection_result import DetectionResult

class BaseDetector(ABC):
    """
    An abstract base class for detectors that identify significant movement in a sequence of frames.

    All specific detector classes (such as `AbsDiffDetector`, `OpticalFlowDetector`, etc.) should inherit from this
    class and implement the `detect` method to provide their own movement detection logic.

    Methods:
        detect(frames): This method must be implemented in subclasses to detect movement in a list of frames.
    """
    
    @abstractmethod
    def detect(self, frames) -> List[DetectionResult]:
        """Detect significant movement in a list of frames."""
        pass
