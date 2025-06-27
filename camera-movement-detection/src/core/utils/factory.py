import os
import yaml
from src.core.models.config_model import ConfigModel, DetectorConfig, QueueConfig, AbsDiffConfig
from src.core.detectors.orb_detector import ORBDetector
from src.core.detectors.absdiff_detector import AbsDiffDetector
from src.core.detectors.optical_flow_detector import OpticalFlowDetector
from src.core.detectors.homography_detector import HomographyDetector
from src.core.utils.logger import get_logger
from src.core.models.config_model import ConfigModel, DetectorConfig, QueueConfig, AbsDiffConfig, ORBConfig, HomographyConfig, OpticalFlowConfig
from src.core.detectors.goodfeatures_detector import GoodFeaturesDetector
from src.core.models.config_model import GoodFeaturesConfig

logger = get_logger()

class DetectorFactory:
    """
    Factory class to create and configure detectors based on the provided settings.

    Args:
        config_path (str): Path to the configuration file (default is "config/settings.yaml").
    """
    def __init__(self, config_path="config/settings.yaml"):
        """
        Initializes the DetectorFactory by loading configuration data from the given YAML file.

        Args:
            config_path (str): The path to the configuration file.
        """
        config_path = os.path.abspath(config_path)
        logger.info(f"Loading config from: {config_path}")

        if not os.path.exists(config_path):
            logger.error(f"Config file not found at: {config_path}")
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)

        default = data.get("detector", {}).get("default", "ORB")
        allowed_types = data.get("allowed_types", {
            "images": ["jpg", "jpeg", "png"],
            "videos": ["mp4", "avi"]
        })

        if "allowed_types" not in data:
            logger.warning("allowed_types not found in config. Using default types.")

        video_defaults = {"max_frames": 100, "max_uploads": 5}
        video_settings = data.get("video", video_defaults)
        for key in video_defaults:
            video_settings.setdefault(key, video_defaults[key])
            logger.info(f"Video settings loaded. Max frames: {video_settings['max_frames']}, Max uploads: {video_settings['max_uploads']}")

        detector_cfg = DetectorConfig(default=default, threshold=0)  

        queue_data = data.get("queue", {"max_video_items": 5, "max_frame_items": 100})
        queue_cfg = QueueConfig(
            max_video_items=int(queue_data.get("max_video_items", 5)),
            max_frame_items=int(queue_data.get("max_frame_items", 100))
        )

        absdiff_cfg = AbsDiffConfig(
            threshold=data.get("absdiff", {}).get("threshold", 50000),
            threshold_value=data.get("absdiff", {}).get("threshold_value", 25)
        )

        orb_cfg = ORBConfig(
            threshold=data.get("orb", {}).get("threshold", 30)
        )

        homography_cfg = HomographyConfig(
            threshold=data.get("homography", {}).get("threshold", 5.0)
        )

        opticalflow_cfg = OpticalFlowConfig(
            threshold=data.get("opticalflow", {}).get("threshold", 2.0)
        )

        goodfeatures_cfg = GoodFeaturesConfig(
            threshold=data.get("goodfeatures", {}).get("threshold", 100)
        )


        self.config = ConfigModel(
            detector=detector_cfg,
            absdiff_config=absdiff_cfg,
            orb_config=orb_cfg,
            homography_config=homography_cfg,
            opticalflow_config=opticalflow_cfg,
            goodfeatures_config=goodfeatures_cfg,
            language=data.get("language", "EN"),
            allowed_types=allowed_types,
            video_settings=video_settings,
            queue_settings=queue_cfg
        )
        logger.info(f"Configuration loaded. Detector: {default}")

    def create_detector(self):
        """
        Creates and returns the appropriate detector based on the current configuration.

        Returns:
            BaseDetector: The configured detector object (AbsDiffDetector, ORBDetector, etc.).
        """
        logger.info(f"Creating detector: {self.config.detector.default}")

        detector_type = self.config.detector.default.lower()

        if detector_type == "absdiff":
            logger.info(
                f"AbsDiffDetector selected with threshold={self.config.absdiff_config.threshold} "
                f"and threshold_value={self.config.absdiff_config.threshold_value}"
            )
            return AbsDiffDetector(
                threshold=self.config.absdiff_config.threshold,
                threshold_value=self.config.absdiff_config.threshold_value
            )

        elif detector_type == "orb":
            logger.info(f"ORBDetector selected with threshold {self.config.orb_config.threshold}")
            return ORBDetector(threshold=self.config.orb_config.threshold)

        elif detector_type == "opticalflow":
            logger.info(f"OpticalFlow selected with threshold {self.config.opticalflow_config.threshold}")
            return OpticalFlowDetector(threshold=self.config.opticalflow_config.threshold)

        elif detector_type == "homography":
            logger.info(f"HomographyDetector selected with threshold {self.config.homography_config.threshold}")
            return HomographyDetector(threshold=self.config.homography_config.threshold)
        
        elif detector_type == "goodfeatures":
            logger.info(f"GoodFeaturesDetector selected with threshold {self.config.goodfeatures_config.threshold}")
            return GoodFeaturesDetector(threshold=self.config.goodfeatures_config.threshold)

        else:
            logger.error(f"Unknown detector type: {self.config.detector.default}")
            raise ValueError(f"Unknown detector type: {self.config.detector.default}")

    def set_threshold(self, value: int):
        """
        Updates the threshold value for the current detector.

        Args:
            value (int): The new threshold value.
        """
        logger.info(f"Threshold updated via UI: {value}")
        self.config.detector.threshold = value

    def set_absdiff_threshold(self, value: int):
        """
        Updates the AbsDiff threshold value.

        Args:
            value (int): The new threshold value for AbsDiff detection.
        """
        logger.info(f"AbsDiff threshold updated via UI: {value}")
        self.config.absdiff_config.threshold = value

    def set_absdiff_threshold_value(self, value: int):
        """
        Updates the AbsDiff threshold value for pixel intensity.

        Args:
            value (int): The new threshold_value for AbsDiff detection.
        """
        logger.info(f"AbsDiff threshold_value updated via UI: {value}")
        self.config.absdiff_config.threshold_value = value

    def set_orb_threshold(self, value: float):
        """
        Updates the ORB threshold value.

        Args:
            value (float): The new threshold value for ORB detection.
        """
        logger.info(f"ORB threshold updated via UI: {value}")
        self.config.orb_config.threshold = value
    
    def set_opticalflow_threshold(self, value: float):
        """
        Updates the OpticalFlow threshold value.

        Args:
            value (float): The new threshold value for OpticalFlow detection.
        """
        logger.info(f"OpticalFlow threshold updated via UI: {value}")
        self.config.opticalflow_config.threshold = value

    def set_homography_threshold(self, value: float):
        """
        Updates the Homography threshold value.

        Args:
            value (float): The new threshold value for Homography detection.
        """
        logger.info(f"Homography threshold updated via UI: {value}")
        self.config.homography_config.threshold = value

    def set_goodfeatures_threshold(self, value: int):
        """
        Updates the GoodFeatures threshold value.

        Args:
            value (int): The new threshold value for GoodFeatures detection.
        """
        logger.info(f"GoodFeatures threshold updated via UI: {value}")
        self.config.goodfeatures_config.threshold = value
