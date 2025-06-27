from dataclasses import dataclass
from .movement_type import MovementType

@dataclass
class DetectionResult:
    """
    Represents the result of a movement detection for a specific frame.

    Args:
        frame_index (int): The index of the frame where movement was detected.
        movement_type (MovementType): The type of movement detected (e.g., translation, rotation).
        score (float): The score indicating the significance of the movement (default is 0.0).
    """
    frame_index: int
    movement_type: MovementType
    score: float = 0.0
