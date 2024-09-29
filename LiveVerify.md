

# Verification Workflow Guide

Welcome to the **Verification Workflow Guide**. This document provides step-by-step instructions to set up and run the verification system, which utilizes live face detection, captcha verification, and eye blink monitoring to authenticate users securely.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Running the Verification Script](#running-the-verification-script)
5. [Verification Workflow](#verification-workflow)
6. [Troubleshooting](#troubleshooting)
7. [Additional Information](#additional-information)

---

## Introduction

The verification system is designed to authenticate users through a combination of real-time face detection, captcha challenges, and eye blink monitoring. This multi-factor authentication ensures that the user is actively participating, enhancing security and preventing automated or fraudulent access.

**Key Features:**

- **Live Face Detection:** Monitors the user's face within a defined bounding box in real-time.
- **Captcha Challenge:** Displays a captcha that the user must verbally reproduce.
- **Eye Blink Detection:** Requires continuous eye blinking while speaking the captcha to confirm active engagement.
- **Image Saving:** Captures and saves the user's image upon successful verification for record-keeping or further processing.

---

## Prerequisites

Before setting up the verification system, ensure that your environment meets the following requirements:

1. **Operating System:** Windows, macOS, or Linux.
2. **Python Version:** Python 3.7 or higher.
3. **Hardware:**
   - **Webcam:** A functional webcam for live face detection.
   - **Microphone:** A working microphone for voice input.
4. **Software Dependencies:** All required Python libraries (listed in `requirements.txt`).

---

## Installation

Follow these steps to set up the verification system on your local machine.

### 1. Clone the Repository

First, clone the repository containing the verification scripts and related files.

```bash
git clone [https://github.com//prasukjain07/UpperCircuit.git]
cd your-repo
```

### 2. Set Up a Virtual Environment (Recommended)

Creating a virtual environment helps manage dependencies and avoid conflicts.

- **Using `venv`:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

- **Using `conda`:**

  ```bash
  conda create -n verify_env python=3.9
  conda activate verify_env
  ```

### 3. Install Required Libraries

Install all necessary Python libraries using the provided `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**Contents of `requirements.txt`:**

```plaintext
faiss-cpu
numpy
torch
torchvision
Pillow
tqdm
opencv-python
speechrecognition
pyaudio
face_recognition
```

**Notes:**

- **`faiss-cpu`:** For efficient similarity search and clustering.
- **`numpy`:** Fundamental package for numerical operations.
- **`torch` & `torchvision`:** For deep learning models used in feature extraction.
- **`Pillow`:** For image processing.
- **`tqdm`:** For displaying progress bars.
- **`opencv-python`:** For real-time face detection and video processing.
- **`speechrecognition` & `pyaudio`:** For capturing and processing voice input.
- **`face_recognition`:** Simplifies face detection and recognition tasks.

**Installation Tips:**

- Ensure you have a stable internet connection as some libraries may require significant download sizes.
- If you encounter issues installing `pyaudio`, refer to the [PyAudio Installation Instructions](https://people.csail.mit.edu/hubert/pyaudio/#downloads) specific to your operating system.

---

## Running the Verification Script

Once all dependencies are installed, you can run the verification process using the `Verification.py` script.

### 1. Execute the Script

Navigate to the project directory and run the script:

```bash
python Verification.py
```

### 2. Script Execution Flow

Upon running the script, the following sequence of events will occur:

1. **Live Face Detection:**
   - The system activates your webcam and displays a live video feed.
   - A bounding box appears on the screen, indicating the area within which your face must remain.
   - The system continuously monitors your face position. If your face moves outside the bounding box, detection will fail.

2. **Successful Face Detection:**
   - Once your face is consistently detected within the bounding box, press the **`S`** key to proceed.

3. **Captcha Challenge:**
   - A captcha image is displayed on the screen.
   - The system prompts you to **speak the captcha aloud**.
   - **Eye Blink Detection:** While speaking the captcha, you must **blink your eyes continuously** to demonstrate active participation.

4. **Captcha Verification:**
   - Your spoken captcha is converted into text using speech recognition.
   - The system matches the spoken input against the displayed captcha.

5. **Result:**
   - **Successful Verification:**
     - If the spoken captcha matches the displayed captcha and eye blinking is detected, the system saves your image.
     - A confirmation message is displayed.
   - **Failed Verification:**
     - If the captcha does not match or eye blinking is not detected, the verification fails, and an error message is shown.

---

## Verification Workflow

Here's a detailed breakdown of each step in the verification process:

### 1. Live Face Detection

- **Bounding Box Display:**
  - A rectangular box appears on the live video feed.
  - Your face must remain within this box for successful detection.

- **Detection Criteria:**
  - The system uses facial recognition algorithms to detect and track your face.
  - If your face exits the bounding box, the system will alert you to reposition.

- **Proceeding to Next Step:**
  - Once your face is securely within the bounding box, press the **`S`** key to continue.

### 2. Captcha Challenge

- **Captcha Display:**
  - A randomly generated captcha image appears on the screen.
  - The captcha is designed to prevent automated bots from passing verification.

- **Voice Input:**
  - You are prompted to **speak the captcha aloud**.
  - Ensure that your microphone is functioning correctly for accurate voice capture.

- **Eye Blink Detection:**
  - While speaking the captcha, the system monitors your eye movements.
  - **Continuous Blinking:** You must blink your eyes intermittently to confirm active participation.

### 3. Captcha Verification

- **Speech Recognition:**
  - The system captures your spoken captcha and converts it into text using speech recognition libraries.

- **Matching Process:**
  - The converted text is compared against the original captcha string.
  - **Success Criteria:** The spoken input must exactly match the captcha.

- **Verification Outcome:**
  - **Success:**
    - Your spoken captcha matches the displayed captcha.
    - Your image is saved for record-keeping or further processing.
    - A success message is displayed.
  - **Failure:**
    - The spoken captcha does not match.
    - Eye blinking was not detected as required.
    - An error message prompts you to retry the verification process.

### 4. Image Saving

- **Successful Verification:**
  - Upon passing all verification steps, the system captures your current frame from the webcam.
  - The image is saved to a predefined directory with a unique identifier.

- **Usage of Saved Images:**
  - These images can be used for future verifications, record-keeping, or security audits.

---

## Troubleshooting

If you encounter issues during the verification process, consider the following troubleshooting steps:

### 1. Library Installation Issues

- **Problem:** Errors during `pip install` for specific libraries.
- **Solution:**
  - Ensure you are using the correct Python version (3.7 or higher).
  - For `pyaudio` installation issues, refer to the [PyAudio Installation Guide](https://people.csail.mit.edu/hubert/pyaudio/#downloads) specific to your OS.
  - Use pre-compiled binaries if available.

### 2. Webcam Not Detected

- **Problem:** The script cannot access your webcam.
- **Solution:**
  - Ensure your webcam is properly connected and not being used by another application.
  - Check your system's privacy settings to allow the script access to the webcam.

### 3. Microphone Issues

- **Problem:** The system cannot capture audio input.
- **Solution:**
  - Verify that your microphone is connected and functioning.
  - Check system privacy settings to allow microphone access.
  - Test your microphone with another application to ensure it's working.

### 4. Speech Recognition Failures

- **Problem:** The system cannot accurately recognize spoken captcha.
- **Solution:**
  - Speak clearly and at a moderate pace.
  - Ensure minimal background noise during the verification.
  - Retry the verification if speech recognition fails multiple times.

### 5. Eye Blink Detection Problems

- **Problem:** The system fails to detect continuous eye blinking.
- **Solution:**
  - Ensure your face is well-lit and clearly visible to the webcam.
  - Avoid rapid or inconsistent blinking.
  - Maintain a natural blinking pattern while speaking the captcha.

### 6. General Script Errors

- **Problem:** Unexpected errors or crashes during script execution.
- **Solution:**
  - Review the error message for specific issues.
  - Ensure all dependencies are correctly installed.
  - Consider updating libraries to their latest versions.
  - Reach out for support with detailed error logs.

---

## Additional Information

### Customizing Verification Parameters

You can modify certain parameters in the `Verification.py` script to better suit your needs:

- **Bounding Box Size and Position:**
  - Adjust the dimensions and placement of the bounding box for face detection.

- **Captcha Complexity:**
  - Change the difficulty level of the captcha by altering its complexity, length, or format.

- **Eye Blink Sensitivity:**
  - Modify the sensitivity settings for eye blink detection to accommodate different user behaviors.

### Security Considerations

- **Data Privacy:**
  - Ensure that saved images and verification data are stored securely.
  - Implement access controls to protect sensitive information.

- **Data Retention:**
  - Define policies for how long verification data is retained and when it should be deleted.

### Extending Functionality

Consider adding the following features to enhance the verification system:

- **Multi-Factor Authentication:**
  - Combine facial recognition and captcha with other authentication methods like passwords or biometric data.

- **User Feedback:**
  - Provide real-time feedback to users during the verification process to improve usability.

- **Logging and Monitoring:**
  - Implement logging mechanisms to monitor verification attempts and detect suspicious activities.

---

## Conclusion

This guide provides a comprehensive overview of setting up and running the verification system using the `Verification.py` script. By following the installation steps and understanding the verification workflow, you can effectively implement a robust authentication mechanism that leverages live face detection, captcha challenges, and eye blink monitoring.

For further assistance or inquiries, feel free to reach out to the project maintainers or consult the official documentation of the utilized libraries.


---
