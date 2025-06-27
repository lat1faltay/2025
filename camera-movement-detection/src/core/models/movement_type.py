from enum import Enum

class MovementType(Enum):
    """
    Enum representing different types of movement detected in the frames.

    Each movement type corresponds to a specific kind of transformation detected between consecutive frames,
    such as translation, rotation, scaling, or homography.

    Values:
        NONE: No movement detected.
        TRANSLATION: Movement due to translation (shifting position).
        ROTATION: Movement due to rotation.
        SCALE: Movement due to scaling.
        PERSPECTIVE: Movement due to perspective change.
        OBJECT: Movement involving an object (not just the camera).
        UNKNOWN: Movement type is unknown.
        HOMOGRAPHY: Movement detected through homography transformation.
        CAMERA: Movement involving the camera itself.
        SHIFT: A small shift in the frame.
    """
    NONE = "none"
    TRANSLATION = "translation"
    ROTATION = "rotation"
    SCALE = "scale"
    PERSPECTIVE = "perspective"
    OBJECT = "object"
    UNKNOWN = "unknown"
    HOMOGRAPHY = "homography"
    CAMERA = "camera"
    SHIFT = "shift"
