import os
import cv2
import numpy as np
import faiss

# Load the face recognition model (OpenFace)
recognition_net = cv2.dnn.readNetFromTorch('nn4.small2.v1.t7')  # Path to OpenFace model

# Function to preprocess the image (keeping 3 channels RGB)
def preprocess_image(image):
    # Resize the image to the required input size of the face recognition model
    face_resized = cv2.resize(image, (96, 96))  # Ensure it stays in 3 channels (RGB)
    
    return face_resized

# Function to recognize faces using OpenCV DNN (OpenFace) after preprocessing
def recognize_face(image):
    # Preprocess the image
    preprocessed_image = preprocess_image(image)
    
    # Create a blob from the preprocessed image
    face_blob = cv2.dnn.blobFromImage(preprocessed_image, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
    recognition_net.setInput(face_blob)
    vec = recognition_net.forward()
    return vec

# Function to extract additional features like age, gender (using pre-trained models)
def extract_additional_features(image):
    # Example placeholders for features:
    age = 25  # Predicted age
    gender = 1  # Gender: 1 for Male, 0 for Female
    return np.array([age, gender])

# Store face embeddings in FAISS, including additional features
def store_embeddings_with_additional_features(dataset_folder, faiss_index_file, dimension=128, batch_size=100):
    # Create a FAISS index with L2 distance (128-dimensional embeddings)
    index = faiss.IndexFlatL2(dimension + 2)  # Extra 2 dimensions for age and gender
    filenames = []

    # Prepare a batch of embeddings
    embeddings = []
    
    # Process each image in the dataset
    for image_file in os.listdir(dataset_folder):
        image_path = os.path.join(dataset_folder, image_file)

        # Load the image (assuming the image is already a cropped face)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Could not load image {image_path}")
            continue

        # Generate the face embedding
        embedding = recognize_face(image).flatten().astype('float32')
        
        # Extract additional features (e.g., age, gender)
        additional_features = extract_additional_features(image)
        
        # Combine the face embedding with additional features
        combined_embedding = np.concatenate((embedding, additional_features), axis=0)
        
        # Add combined embedding to the batch
        embeddings.append(combined_embedding)
        filenames.append(image_file)

        # Once batch is ready, add to FAISS index
        if len(embeddings) == batch_size:
            index.add(np.array(embeddings))  # Add a batch to FAISS index
            embeddings = []  # Clear the batch for the next round
            print(f"Processed batch of {batch_size} images")

    # Add remaining embeddings if any
    if embeddings:
        index.add(np.array(embeddings))
        print(f"Processed final batch of {len(embeddings)} images")

    # Save the FAISS index
    faiss.write_index(index, faiss_index_file)

    # Save filenames corresponding to the embeddings
    with open("filenames.txt", "w") as f:
        for filename in filenames:
            f.write(f"{filename}\n")

    print(f"All face embeddings (with additional features) have been stored in FAISS index and filenames.txt.")

# Example usage: Store embeddings in FAISS
dataset_folder = "img_align_celeba/img_align_celeba"  # Replace with your dataset folder path
faiss_index_file = "face_embeddings_faiss.index"  # Path to save the FAISS index
store_embeddings_with_additional_features(dataset_folder, faiss_index_file)
