import os
import cv2
import numpy as np
import faiss

# Load the face detection model (SSD ResNet)
try:
    face_net = cv2.dnn.readNetFromCaffe(
        "deploy.prototxt",  # Path to deploy.prototxt
        "res10_300x300_ssd_iter_140000.caffemodel"  # Path to res10_300x300_ssd_iter_140000.caffemodel
    )
except cv2.error as e:
    print("Error loading SSD model:", e)
    exit()

# Load the face recognition model (OpenFace)
recognition_net = cv2.dnn.readNetFromTorch('nn4.small2.v1.t7')  # Path to OpenFace model

# Function to detect faces using SSD ResNet model
def detect_faces(image):
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    
    face_net.setInput(blob)
    detections = face_net.forward()

    face_images = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Confidence threshold for face detection
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            
            # Extract the face region
            face = image[startY:endY, startX:endX]
            face_images.append(face)

    return face_images

# Function to recognize faces using OpenCV DNN (OpenFace)
def recognize_face(face):
    face_resized = cv2.resize(face, (96, 96))  # Ensure consistent face size
    face_blob = cv2.dnn.blobFromImage(face_resized, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
    recognition_net.setInput(face_blob)
    vec = recognition_net.forward()
    return vec

# Store face embeddings in FAISS
def store_embeddings_in_faiss(dataset_folder, faiss_index_file, dimension=128):
    # Create a FAISS index with L2 distance (128-dimensional embeddings)
    index = faiss.IndexFlatL2(dimension)
    filenames = []

    # Process each image in the dataset
    for image_file in os.listdir(dataset_folder):
        image_path = os.path.join(dataset_folder, image_file)
        
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image {image_path}")
            continue
        
        faces = detect_faces(image)

        # Only process the first face detected (you can modify to handle multiple faces)
        if faces:
            face = faces[0]
            embedding = recognize_face(face).flatten().astype('float32')

            # Add embedding to the FAISS index
            index.add(np.expand_dims(embedding, axis=0))
            filenames.append(image_file)
            print(f"Processed {image_file}")

    # Save the FAISS index
    faiss.write_index(index, faiss_index_file)

    # Save filenames corresponding to the embeddings
    with open("filenames.txt", "w") as f:
        for filename in filenames:
            f.write(f"{filename}\n")

    print(f"All face embeddings have been stored in FAISS index and filenames.txt.")

# Example usage: Store embeddings in FAISS
dataset_folder = "img2"  # Replace with your dataset folder path
faiss_index_file = "face_embeddings_faiss.index"  # Path to save the FAISS index
store_embeddings_in_faiss(dataset_folder, faiss_index_file)
