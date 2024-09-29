#driver file

from huggingface_hub import hf_hub_download
from ultralytics import YOLO
from supervision import Detections
from PIL import Image
import json
from deepface import DeepFace
from flask import Flask, request, jsonify
import os
import Verification


app = Flask(__name__)

model_path = hf_hub_download(repo_id="arnabdhar/YOLOv8-Face-Detection", filename="model.pt")
model = YOLO(model_path)

def faceDetc(image_id,model):

    Verification.main()
    
    image_path = image_id  #
    image = Image.open(image_path)

    output = model(image)

    # Convert the results to a usable format
    results = Detections.from_ultralytics(output[0])

    boxes = results.xyxy  # The bounding boxes in [x_min, y_min, x_max, y_max] format

    for i, box in enumerate(boxes):
        x_min, y_min, x_max, y_max = map(int, box[:4])
        
        # Crop the face from the original image
        cropped_face = image.crop((x_min, y_min, x_max, y_max))
        
        # Save the cropped face as a new image
        output_face_path = "face_1.jpeg"
        cropped_face.save(output_face_path)
        # print(f"Saved cropped face as {output_face_path}")


result = DeepFace.verify(img1_path="face_1.jpeg",img2_path="verified_image.jpg")
verified = result.get("verified", False)  # Defaults to False if key not found

UPLOAD_FOLDER = './received_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/receive-image', methods=['POST'])

def receive_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file in the request'})

    image_id = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image_id.filename)
    image_id.save(image_path)
    faceDetc(image_id,model)

    return result

if __name__ == '__main__':
    app.run(port=5000)
# output_json = json.dumps({"verified": verified}, indent=2)
# print(output_json) Choose how you want to output your results here we have used a verification bool
