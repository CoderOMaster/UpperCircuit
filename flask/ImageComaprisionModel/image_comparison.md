
# Image Comparison with FAISS

This guide explains how to use two scripts to compare images from a large dataset by converting them into embeddings and saving them in a FAISS index. The first script processes the dataset images to create the FAISS index, while the second script allows you to upload an image and find the best 5 matches from the dataset.

## Step 1: Convert Dataset Images to FAISS Index

### Script 1: Create FAISS Index from Dataset

This script extracts features from a directory of images and saves them as a FAISS index.

### Instructions:

1. **Prepare Your Environment**:
   - Ensure you have the necessary libraries installed:
     ```bash
     pip install opencv-python numpy faiss-cpu keras
     ```
   - Place your dataset images in a folder.

2. **Script Configuration**:
   - Open `script_1.py` and set the `dataset_folder` variable to the path of your image dataset directory.
   ```python
   dataset_folder = "path/to/your/dataset_folder"  # Replace with your dataset folder path
   ```

3. **Run the Script**:
   - Execute the script to convert all dataset images into embeddings and save them in a FAISS index file:
   ```bash
   python script_1.py
   ```

4. **Output**:
   - After running, the script will generate:
     - `face_embeddings_faiss.index`: The FAISS index file containing the image embeddings.
     - `filenames.txt`: A text file listing the filenames of the images corresponding to the embeddings.

---

## Step 2: Find Best 5 Images

### Script 2: Compare Uploaded Image with FAISS Index

This script allows you to upload an image and find the top 5 closest matches from the dataset.

### Instructions:

1. **Prepare Your Environment**:
   - Ensure that the required models (`deploy.prototxt`, `res10_300x300_ssd_iter_140000.caffemodel`, and `nn4.small2.v1.t7`) are available in your working directory.

2. **Script Configuration**:
   - Open `script_2.py` and set the `uploaded_image_path`, `faiss_index_file`, and `filenames_file` variables:
   ```python
   uploaded_image_path = "path/to/uploaded/image.jpg"  # Replace with your uploaded image path
   faiss_index_file = "face_embeddings_faiss.index"   # The FAISS index file created in Step 1
   filenames_file = "filenames.txt"                   # The filenames file created in Step 1
   ```

3. **Run the Script**:
   - Execute the script to compare the uploaded image against the FAISS index:
   ```bash
   python script_2.py
   ```

4. **Output**:
   - The script will output the top 5 matches, showing the filenames of the closest images from the dataset along with their distances.
