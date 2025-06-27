import uuid
import streamlit as st
import cv2
import tempfile

from src.pipelines.extractor import Extractor
from src.core.utils.factory import DetectorFactory
from src.core.validators.input_validator import InputValidator 
from src.core.exceptions.custom_exceptions import InvalidInputException
from src.core.utils.logger import get_logger
from src.core.models.movement_type import MovementType 
from src.core.utils.queue_manager import QueueManager
from src.core.detectors.homography_detector import draw_matches
from src.core.utils.visualizer import annotate_frame
from movement_detector import MovementDetector 

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Initialize logger and essential classes
logger = get_logger()
extractor = Extractor()
factory = DetectorFactory()
validator = InputValidator(
    allowed_types=factory.config.allowed_types,
    max_videos=factory.config.queue_settings.max_video_items
)
movement_detector = MovementDetector(factory)

def sidebar_detector_selection(factory):
    """
    Displays a sidebar in the Streamlit app that allows the user to select the detection algorithms
    and set their thresholds for camera movement detection.

    Args:
        factory: A factory instance to access configuration for detection algorithms.

    Returns:
        selected_detectors (list): List of selected detectors from the sidebar.
        thresholds (dict): Dictionary with thresholds for each selected detector.
    """
    st.sidebar.header("Detection Algorithms (Multi-select)")

    detector_options = {
        "ORB": {
            "default": factory.config.orb_config.threshold,
            "min": 10,
            "max": 100,
            "step": 1,
            "type": int,
            "label": "ORB Threshold"
        },
        "AbsDiff": {
            "default": factory.config.absdiff_config.threshold,
            "min": 1000,
            "max": 200000,
            "step": 1000,
            "type": int,
            "label": "AbsDiff Threshold"
        },
        "OpticalFlow": {
            "default": factory.config.opticalflow_config.threshold,
            "min": 0.5,
            "max": 10.0,
            "step": 0.1,
            "type": float,
            "label": "Optical Flow Threshold"
        },
        "Homography": {
            "default": factory.config.homography_config.threshold,
            "min": 0.5,
            "max": 10.0,
            "step": 0.1,
            "type": float,
            "label": "Homography Threshold"
        },
        "GoodFeatures": {
            "default": factory.config.goodfeatures_config.threshold if hasattr(factory.config, "goodfeatures_config") else 100,
            "min": 10,
            "max": 300,
            "step": 5,
            "type": int,
            "label": "Good Features Threshold"
        }
    }

    selected_detectors = []
    thresholds = {}

    # Add detector selection and threshold sliders
    for det_name in detector_options.keys():
        checked = st.sidebar.checkbox(det_name, value=(factory.config.detector.default == det_name))
        if checked:
            selected_detectors.append(det_name)
            opt = detector_options[det_name]
            thresholds[det_name] = st.sidebar.slider(
                label=opt["label"],
                min_value=opt["min"],
                max_value=opt["max"],
                value=opt["default"],
                step=opt["step"]
            )

    if not selected_detectors:
        st.sidebar.warning("At least one detection algorithm must be selected.")
    return selected_detectors, thresholds

def display_results(results_per_file):
    """
    Displays the results of the camera movement detection on the Streamlit app.
    Shows frames with detected movements and provides detailed information about the detection.

    Args:
        results_per_file (list): A list of tuples containing file labels, frames, and detector results.
    """
    tabs = st.tabs([label for label, _, _ in results_per_file])

    for idx, (label, frames, all_detector_results) in enumerate(results_per_file):
        with tabs[idx]:
            st.subheader(f"Results for: {label}")
            
            st.image(frames[0], caption=f"Sample Frame from {label}", use_container_width=True)

            for det_name, results in all_detector_results:
                with st.expander(f"{det_name} Result"):
                    if not results:
                        st.success("No significant movement detected.")
                    else:
                        st.info(f"Detected movement in {len([r.frame_index for r in results])} frame(s).")
                        for r in results:
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                image_to_show = frames[r.frame_index]
                                label = f"{r.movement_type.value.upper()} (score={r.score:.2f})"
                                annotated_image = annotate_frame(image_to_show, text=label)
                                st.image(annotated_image, caption=f"Frame {r.frame_index}", use_container_width=True)
                            with col2:
                                st.markdown(f"**Method**: {det_name}")
                                st.markdown(f"**Type**: {r.movement_type.value}")
                                st.markdown(f"**Score**: {r.score:.2f}")
                                st.markdown("---")

def main():
    """
    Main function to run the Streamlit app for camera movement detection.
    Initializes the app, processes uploaded files, and displays the detection results.

    This function also handles user interactions, file uploads, validation, and error handling.
    """
    st.set_page_config(page_title="Camera Movement Detection", layout="wide")
    st.title("📹 Camera Movement Detection")
    st.write("Upload videos or image sequences to detect significant **camera movement** like pan, tilt or shift.")

    selected_detectors, thresholds = sidebar_detector_selection(factory)
    if not selected_detectors:
        return  

    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = str(uuid.uuid4())
    uploader_key = st.session_state["uploader_key"]

    if st.sidebar.button("Clear All Uploads"):
        movement_detector.video_queue.clear()
        movement_detector.frame_queue.clear()
        st.session_state["uploaded_files"] = []
        st.session_state["uploader_key"] = str(uuid.uuid4())
        st.rerun()

    allowed_all_types = factory.config.allowed_types.get("images", []) + factory.config.allowed_types.get("videos", [])

    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    uploaded_files = st.file_uploader(
        "Choose image or video files",
        type=allowed_all_types,
        accept_multiple_files=True,
        key=uploader_key
    )

    results_per_file = []

    if uploaded_files:
        try:
            validator.validate_files(uploaded_files)

            movement_detector.set_detectors({det: thresholds[det] for det in selected_detectors})

            image_files = []
            for file in uploaded_files:
                if validator.is_video(file):
                    if not movement_detector.enqueue_video(file):
                        logger.warning(f"File skipped due to queue limit: {file.name}")
                else:
                    image_files.append(file)

            if image_files:
                movement_detector.frame_queue.clear()
                movement_detector.enqueue_frames(extractor.extract_frames_from_images(image_files))
                results = movement_detector.process_frames()
                results_per_file.append(("Uploaded Images", extractor.extract_frames_from_images(image_files), results))

            video_results = movement_detector.process_videos(extractor)
            results_per_file.extend(video_results)

            display_results(results_per_file)

        except InvalidInputException as e:
            logger.warning(f"Validation error: {e}")
            st.error(f"Validation Error: {e}")

        except Exception as e:
            logger.exception(f"Unexpected error occurred. Exception: {e}")
            st.error("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    main()
