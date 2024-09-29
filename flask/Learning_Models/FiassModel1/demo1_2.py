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
    print(f"Error loading SSD model: {e}")
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

# Load filenames corresponding to embeddings
def load_filenames(filename_file):
    with open(filename_file, "r") as f:
        filenames = [line.strip() for line in f.readlines()]
    return filenames

# Compare an uploaded image with the FAISS index
def compare_uploaded_image_with_faiss(uploaded_image_path, faiss_index_file, filenames_file):
    # Load the FAISS index
    index = faiss.read_index(faiss_index_file)

    # Load the filenames
    filenames = load_filenames(filenames_file)

    # Load and process the uploaded image
    uploaded_image = cv2.imread(uploaded_image_path)
    if uploaded_image is None:
        print(f"Error: Could not load uploaded image {uploaded_image_path}")
        return

    faces = detect_faces(uploaded_image)

    if faces:
        face = faces[0]  # Use the first detected face
        uploaded_embedding = recognize_face(face).flatten().astype('float32')

        # Query the FAISS index for the nearest neighbors
        k = 1  # Find the closest match
        D, I = index.search(np.expand_dims(uploaded_embedding, axis=0), k)

        # Retrieve the best match
        best_match_index = I[0][0]
        best_match_distance = D[0][0]

        # Print the result
        if best_match_index != -1 and best_match_distance < 0.4:  # Adjust the distance threshold as needed
            print(f"Best match found: {filenames[best_match_index]} with distance {best_match_distance}")
        else:
            print("No matching face found in the dataset.")
    else:
        print("No face detected in the uploaded image.")

# Example usage: Compare an uploaded image with the FAISS index
uploaded_image_path = "4.jpeg"  # Replace with your uploaded image path
faiss_index_file = "face_embeddings_faiss.index"   # The FAISS index created in Step 1
filenames_file = "filenames.txt"                   # The filenames file created in Step 1
compare_uploaded_image_with_faiss(uploaded_image_path, faiss_index_file, filenames_file)
