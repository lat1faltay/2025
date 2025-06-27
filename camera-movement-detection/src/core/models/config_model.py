from dataclasses import dataclass
from typing import List, Dict

@dataclass
class DetectorConfig:
    """
    Configuration class for the detector settings.
    
    Args:
        default (str): The default detector to use.
        threshold (float): The threshold value for detection.
    """
    default: str
    threshold: float

@dataclass
class QueueConfig:
    """
    Configuration class for the queue settings.
    
    Args:
        max_video_items (int): The maximum number of video items allowed in the queue.
        max_frame_items (int): The maximum number of frame items allowed in the queue.
    """
    max_video_items: int
    max_frame_items: int

@dataclass
class AbsDiffConfig:
    """
    Configuration class for the AbsDiff detector settings.
    
    Args:
        threshold (float): The threshold for detecting significant movement.
        threshold_value (int): The pixel intensity threshold for binarizing the absolute difference.
    """
    threshold: float = 50000
    threshold_value: int = 25

@dataclass
class HomographyConfig:
    """
    Configuration class for the Homography detector settings.
    
    Args:
        threshold (float): The threshold for determining the movement based on the homography score.
    """
    threshold: float = 5.0

@dataclass
class OpticalFlowConfig:
    """
    Configuration class for the OpticalFlow detector settings.
    
    Args:
        threshold (float): The threshold for detecting movement based on the optical flow mean movement.
    """
    threshold: float = 2.0

@dataclass
class ORBConfig:
    """
    Configuration class for the ORB detector settings.
    
    Args:
        threshold (int): The minimum number of keypoint matches to consider significant movement.
    """
    threshold: int = 30

@dataclass
class GoodFeaturesConfig:
    """
    Configuration class for the Good Features detector settings.
    
    Args:
        threshold (int): The threshold for detecting significant movement based on feature count difference.
    """
    threshold: int = 100


@dataclass
class ConfigModel:
    """
    Configuration model that contains all the configuration settings for detectors, queues, and other parameters.
    
    Args:
        detector (DetectorConfig): The detector configuration.
        absdiff_config (AbsDiffConfig): The AbsDiff detector configuration.
        orb_config (ORBConfig): The ORB detector configuration.
        homography_config (HomographyConfig): The Homography detector configuration.
        opticalflow_config (OpticalFlowConfig): The OpticalFlow detector configuration.
        goodfeatures_config (GoodFeaturesConfig): The GoodFeatures detector configuration.
        language (str): The language for localization.
        allowed_types (Dict[str, List[str]]): A dictionary of allowed file types for detection.
        video_settings (Dict[str, int]): Settings related to video processing.
        queue_settings (QueueConfig): Configuration for the queue settings.
    """
    detector: DetectorConfig
    absdiff_config: AbsDiffConfig
    orb_config: ORBConfig
    homography_config: HomographyConfig
    opticalflow_config: OpticalFlowConfig
    goodfeatures_config: GoodFeaturesConfig
    language: str
    allowed_types: Dict[str, List[str]]
    video_settings: Dict[str, int]
    queue_settings: QueueConfig
