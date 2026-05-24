# AI Biomechanics & Kinetic Form Tracker

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Google-blue?style=for-the-badge)

## Overview
A real-time computer vision system engineered to map human skeletal structures and compute dynamic joint angles for athletic form analysis. Utilizing Google's MediaPipe Pose framework and OpenCV, the system translates live video feeds into 33 interconnected 3D spatial landmarks without the need for external physical sensors or MoCap suits.

---

## Core Architecture & Mathematical Logic

The system does not just track movement; it calculates biomechanical efficiency using continuous trigonometric processing.

1. **Skeletal Landmark Extraction:** * Processes frames via `cv2.VideoCapture` and maps the x, y, and z coordinates of major articulation points (e.g., shoulder, elbow, wrist).
2. **Dynamic Angle Computation:**
   * Calculates the exact angle of flexion/extension between three given coordinates (Vertex $B$, Points $A$ and $C$).
   * The core spatial logic relies on the arctangent function to determine the relative angle:
   
   $$\theta = \left| \text{atan2}(y_C - y_B, x_C - x_B) - \text{atan2}(y_A - y_B, x_A - x_B) \right| \times \frac{180}{\pi}$$

3. **Form State Machine:**
   * Uses calculated angles to trigger state transitions (e.g., "Down" vs "Up" phases in a pull-up or bicep curl).
   * Implements a repetition counter driven by kinematic boundary thresholds rather than simple motion detection.

---

## Tech Stack
* **Language:** Python
* **Vision Framework:** OpenCV (`cv2`)
* **ML/Skeletal Mapping:** MediaPipe (`mp_pose`, `mp_drawing`)
* **Mathematics:** NumPy (Trigonometric transformations)

---

## Project Structure

Ensure your project directory contains the following files:

* `tracker.py`: The core application engine containing the video capture, mathematical logic, and rendering code.
* `requirements.txt`: The list of library dependencies required to run the environment.

---

## Installation & Setup

1. **Clone or Download the Repository:**
   Navigate to your desired folder in your terminal.
   
2. **Set Up a Virtual Environment (Optional but Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
