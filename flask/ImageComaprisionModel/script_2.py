import cv2
import numpy as np
import faiss

try:
    face_net = cv2.dnn.readNetFromCaffe(
        "deploy.prototxt", 
        "res10_300x300_ssd_iter_140000.caffemodel"  
    )
except cv2.error as e:
    print(f"Error loading SSD model: {e}")
    exit()

recognition_net = cv2.dnn.readNetFromTorch('nn4.small2.v1.t7')  

def detect_faces(image):
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_net.setInput(blob)
    detections = face_net.forward()

    face_images = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            
           
            face = image[startY:endY, startX:endX]
            face_images.append(face)

    return face_images

def recognize_face(face):
    face_resized = cv2.resize(face, (96, 96)) 
    face_blob = cv2.dnn.blobFromImage(face_resized, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
    recognition_net.setInput(face_blob)
    vec = recognition_net.forward()
    return vec

def load_filenames(filename_file):
    with open(filename_file, "r") as f:
        filenames = [line.strip() for line in f.readlines()]
    return filenames

def compare_uploaded_image_with_faiss(uploaded_image_path, faiss_index_file, filenames_file):
    index = faiss.read_index(faiss_index_file)

    filenames = load_filenames(filenames_file)

    uploaded_image = cv2.imread(uploaded_image_path)
    if uploaded_image is None:
        print(f"Error: Could not load uploaded image {uploaded_image_path}")
        return

    faces = detect_faces(uploaded_image)

    if faces:
        face = faces[0]  
        uploaded_embedding = recognize_face(face).flatten().astype('float32')

        k = 5  # Find the top 5 matches
        D, I = index.search(np.expand_dims(uploaded_embedding, axis=0), k)

        print("Top matches:")
        for i in range(k):
            best_match_index = I[0][i]
            best_match_distance = D[0][i]

            if best_match_index != -1 and best_match_distance < 0.4:  # Adjust the distance threshold as needed
                print(f"{i + 1}: {filenames[best_match_index]} with distance {best_match_distance}")
            else:
                print(f"{i + 1}: No matching face found in the dataset.")
    else:
        print("No face detected in the uploaded image.")

uploaded_image_path = "000004.jpg"  # Replace with your uploaded image path
faiss_index_file = "face_embeddings_faiss.index"   
filenames_file = "filenames.txt"                   
compare_uploaded_image_with_faiss(uploaded_image_path, faiss_index_file, filenames_file)

