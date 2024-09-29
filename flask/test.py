from huggingface_hub import hf_hub_download
from ultralytics import YOLO
from supervision import Detections
from PIL import Image
import json
from deepface import DeepFace

model_path = hf_hub_download(repo_id="arnabdhar/YOLOv8-Face-Detection", filename="model.pt")
model = YOLO(model_path)

image_path = "8.jpeg"  #
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
    output_face_path = f"face_{i+1}.jpeg"
    cropped_face.save(output_face_path)
    print(f"Saved cropped face as {output_face_path}")


result = DeepFace.verify(img1_path="face_1.jpeg",img2_path="9.jpeg")
verified = result.get("verified", False)  # Defaults to False if key not found

# output_json = json.dumps({"verified": verified}, indent=2)
# print(output_json) Choose how you want to output your results here we have used a verification bool
print("Result:", verified)
