#for liveness detection

import cv2
import random
import string
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import time
import threading
import os
import dlib


model = whisper.load_model('medium')

# Load the dlib face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor_path = "shape_predictor_68_face_landmarks.dat"
if not os.path.isfile(predictor_path):
    print("Error: shape_predictor_68_face_landmarks.dat not found.")
    print("Please download it from https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat")
    exit()

predictor = dlib.shape_predictor(predictor_path)

# Function to generate random captcha
def generate_captcha(length=5):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Function to draw text on the frame
def draw_text(img, text, position, font_scale=1, color=(255, 255, 255), thickness=2):
    cv2.putText(img, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness)

# Function to record audio
def record_audio(duration=5, fs=44100):
    print("Recording...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print("Recording complete.")
    write('output.wav', fs, recording)

# Function to transcribe audio using Whisper
def transcribe_audio(filename='output.wav', model=None):
    result = model.transcribe(filename)
    transcript = result['text'].strip().upper()
    return transcript

# Function to calculate Eye Aspect Ratio (EAR) for blink detection
def calculate_EAR(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    EAR = (A + B) / (2.0 * C)
    return EAR

# Function to detect blinks based on EAR
def detect_blinks(shape, blink_threshold=0.25, consecutive_frames_threshold=3):
    left_eye_indices = list(range(42, 48))
    right_eye_indices = list(range(36, 42))

    left_eye = np.array([(shape.part(i).x, shape.part(i).y) for i in left_eye_indices])
    right_eye = np.array([(shape.part(i).x, shape.part(i).y) for i in right_eye_indices])

    left_EAR = calculate_EAR(left_eye)
    right_EAR = calculate_EAR(right_eye)

    EAR = (left_EAR + right_EAR) / 2.0
    return EAR

# Thread function to handle recording, transcription, and blink detection while recording
def record_and_transcribe(captcha, model, result_dict, cap, EAR_threshold, blink_required):
    try:
        # Recording countdown
        for i in range(3, 0, -1):
            print(f"Recording in {i} seconds...")
            time.sleep(1)

        blink_counter = 0
        consecutive_frames = 0
        recording_duration = 5  # 5 seconds recording duration
        start_time = time.time()

        # Start audio recording in a separate thread
        audio_thread = threading.Thread(target=record_audio, args=(recording_duration,))
        audio_thread.start()

        while time.time() - start_time < recording_duration:
            ret, frame = cap.read()
            if not ret:
                print("Failed to read frame during recording.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)

            if len(faces) > 0:
                face = faces[0]
                shape = predictor(gray, face)
                EAR = detect_blinks(shape)

                # Blink detection logic
                if EAR < EAR_threshold:
                    consecutive_frames += 1
                else:
                    if consecutive_frames >= 3:
                        blink_counter += 1
                        consecutive_frames = 0

            cv2.putText(frame, f"Blinks: {blink_counter}", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow('Recording - Press Q to stop early', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Early termination of recording.")
                break

        audio_thread.join()  # Ensure audio recording is finished
        sd.wait()  # Wait until the sound device is done

        # Check if blinks are sufficient
        if blink_counter < blink_required:
            print(f"Failed. Insufficient blinks detected ({blink_counter}/{blink_required}). Not verified.")
            result_dict['result'] = False
            return

        print("Transcribing audio...")
        transcription = transcribe_audio('output.wav', model)

        if transcription:
            print(f"You said: {transcription}")
            print(f"Original CAPTCHA: {captcha}")
            if ''.join(transcription.split()).upper() == ''.join(captcha.split()).upper():
                print("Success! CAPTCHA and blinks verified.")
                result_dict['result'] = True
                cap.release()
                cv2.destroyAllWindows()
            else:
                print("Failed. The spoken CAPTCHA does not match.")
                result_dict['result'] = False
        else:
            print("Failed to transcribe audio.")
            result_dict['result'] = False
    except Exception as e:
        print(f"An error occurred during recording or transcription: {e}")
        result_dict['result'] = False
    finally:
        if os.path.exists('output.wav'):
            os.remove('output.wav')

# Main function to handle face detection, frame updates, and CAPTCHA verification with blink detection
def main():
    cap = cv2.VideoCapture(0)

    captcha = None
    face_detected = False
    recording_available = True
    verification_result = None
    result_dict = {}

    EAR_threshold = 0.25  # EAR threshold for blink detection
    blink_required = 6  # Minimum number of blinks required for verification

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to access webcam.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        if len(faces) > 0:
            face = faces[0]
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            if x > 10 and y > 10 and x + w < frame.shape[1] - 10 and y + h < frame.shape[0] - 10:
                if not face_detected:
                    face_detected = True
                    captcha = generate_captcha()
                    recording_available = True
                    verification_result = None

                draw_text(frame, f"CAPTCHA: {captcha}", (10, 30))
                if recording_available:
                    draw_text(frame, "Press 'S' to speak and blink", (10, 60))
                elif verification_result is not None:
                    result_text = "CAPTCHA Verified!" if verification_result else "CAPTCHA Failed!"
                    result_color = (0, 255, 0) if verification_result else (0, 0, 255)
                    draw_text(frame, result_text, (10, 60), color=result_color)
                    cv2.imwrite('verified_image.jpg', frame)

            else:
                face_detected = False
                captcha = None
                draw_text(frame, "Face not in frame", (10, 30))
        else:
            face_detected = False
            captcha = None
            draw_text(frame, "No face detected", (10, 30))

        cv2.imshow('CAPTCHA Verification', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s') and captcha and recording_available:
            recording_available = False
            # Start a separate thread for recording, transcription, and blink detection
            verification_thread = threading.Thread(target=record_and_transcribe, args=(captcha, model, result_dict, cap, EAR_threshold, blink_required))
            verification_thread.start()
            verification_thread.join()  # Wait for the thread to complete
            verification_result = result_dict.get('result', None)

            if verification_result is False:
                print("CAPTCHA and blink verification failed.")
                break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
