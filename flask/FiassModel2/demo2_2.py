import cv2
import numpy as np
import faiss

# Load the face recognition model (OpenFace)
recognition_net = cv2.dnn.readNetFromTorch('nn4.small2.v1.t7')  # Path to OpenFace model

# Function to recognize faces using OpenCV DNN (OpenFace)
def recognize_face(image):
    # Resize the image to the required input size of the face recognition model
    face_resized = cv2.resize(image, (96, 96))  # Resize to the size expected by the OpenFace model
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

    # Directly use the entire image for face recognition (assuming it is tightly cropped)
    uploaded_embedding = recognize_face(uploaded_image).flatten().astype('float32')

    # Query the FAISS index for the nearest neighbors
    k = 1  # Find the closest match
    D, I = index.search(np.expand_dims(uploaded_embedding, axis=0), k)

    # Retrieve the best match
    best_match_index = I[0][0]
    best_match_distance = D[0][0]

    # Print the result
    if best_match_index != -1 and best_match_distance < 0.6:  # Adjust the distance threshold as needed
        print(f"Best match found: {filenames[best_match_index]} with distance {best_match_distance}")
    else:
        print("No matching face found in the dataset.")

# Example usage: Compare an uploaded image with the FAISS index
uploaded_image_path = "3.jpeg"  # Replace with your uploaded image path
faiss_index_file = "face_embeddings_faiss.index"   # The FAISS index created in Step 1
filenames_file = "filenames.txt"                   # The filenames file created in Step 1
compare_uploaded_image_with_faiss(uploaded_image_path, faiss_index_file, filenames_file)
