# Camera Movement Detection

## Overview

The **Camera Movement Detection** project is a computer vision application designed to detect and analyze movements in video footage. This system identifies different types of movement such as translation, object motion, and camera shake, using various algorithms like **Good Features to Track**, **Optical Flow**, **Homography**, and **ORB**. The application supports real-time video analysis and provides visual feedback to the user through an interactive interface built with **Streamlit**.

The system is designed to be modular and scalable, allowing users to easily integrate new movement detection algorithms and customize the analysis process.


---

## Folder Structure

```bash
2025/
└── camera-movement-detection/
├── app.py # Main Streamlit app entry point
├── requirements.txt # Python dependencies
├── Dockerfile # Dockerfile for containerization
├── config/
│ └── settings.yaml # Configuration file for thresholds and settings
├── src/
│ ├── core/
│ │ ├── detectors/ # Movement detection algorithm implementations
│ │ ├── exceptions/ # Custom exception classes
│ │ ├── models/ # Data models like DetectionResult, MovementType
│ │ ├── utils/ # Utility classes like logger, factory, validators
│ │ └── validators/ # Input validation classes
│ ├── pipelines/ # Data processing pipelines like Extractor
│ └── tests/ # Unit and integration tests
└── logs/ # Log files directory (may be created at runtime)
```
---

## Features

- **Real-Time Detection:** Detects movement in real-time from video or image files.
- **Multiple Detection Algorithms:**
  - **Good Features to Track**
  - **Optical Flow**
  - **Homography**
  - **ORB (Oriented FAST and Rotated BRIEF)**
- **User-Friendly Interface:** A Streamlit-powered interface for easy interaction with the system.
- **Customizable:** Easily extendable with new detection algorithms or adjustments to existing ones.
- **Supports Multiple File Types:** Works with both video and image files.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/lat1faltay/2025.git
cd 2025/camera-movement-detection 
``````
### 2. Set up a Virtual Environment
```bash
- Linux or Mac
python3 -m venv venv
source venv/bin/activate 

- Windows
python -m venv venv
.\venv\Scripts\activate
``````

### Install Dependencies
Make sure you have requirements.txt in the root directory. Install the necessary dependencies:
```bash
pip install -r requirements.txt
``````

## Usage
### 1. Running the Application Locally
Once the dependencies are installed, you can start the Streamlit app:
```bash
streamlit run app.py
``````
The app will be available at: http://localhost:8501

### 2. Uploading Files
You can upload video or image files through the Streamlit UI. The system will detect and display the movement types in the uploaded frames.


### 3. Viewing the Results
Once a file is uploaded, the results for each algorithm will be displayed, showing the frames with detected movement types. You will also see the confidence score and the type of movement detected (e.g., Translation, Object, Camera).

## Configuration

### Custom Configurations

The project uses a config file to manage settings such as thresholds for detection and the detection algorithms used. This file can be customized by modifying `src/config/settings.yaml`.

- **Threshold values** for each algorithm.
- **Movement detection settings**.
- **Logging settings**.

### Example Configuration (settings.yaml):
```bash
thresholds:
  good_features: 100
  optical_flow: 0.5
  homography: 0.1

algorithms:
  - good_features
  - optical_flow
  - homography
  - orb
``````
Make sure the configuration file is placed in the correct directory (src/config/).

## Algorithms

The following movement detection algorithms are included in this project:

1. **Good Features to Track**  
   This algorithm tracks good features in consecutive video frames. It computes the difference in feature count between frames to detect motion.

2. **Optical Flow**  
   Using Lucas-Kanade Optical Flow, this method tracks the motion of pixels across consecutive frames.

3. **Homography Detection**  
   This algorithm computes the Homography Matrix between consecutive frames to detect camera motion or object motion.

4. **ORB (Oriented FAST and Rotated BRIEF)**  
   ORB is a feature detector and descriptor that combines the FAST corner detector and the BRIEF descriptor with orientation information.


## Running the Project
### Running with Docker (Optional)
If you prefer to run this project using Docker, the project is Dockerized and can be easily run in any environment that supports Docker.

### 1. Build the Docker image:
```bash
docker build -t camera-movement-detection .
```
### 2. Run the Docker container:

```bash
docker run -p 8501:8501 camera-movement-detection
```

##Testing
To run the tests:
```bash
pytest
```
Tests are located in the tests/ directory, and they are designed to check the functionality of different algorithms and the application itself.



## Acknowledgements
This project was made possible by the work of various contributors, libraries, and frameworks:
- OpenCV
- Streamlit
- NumPy
- PyYAML
- pytest


### Connection Information

### Streamlit
- https://atp-core-talent.streamlit.app/

### VPS Server
- http://37.148.211.134:8501/

