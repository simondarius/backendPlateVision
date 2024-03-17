from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image,ImageOps
import pytesseract
import yolov5

# Initialize Flask application
app = Flask(__name__)

# Load YOLOv5 model
model = yolov5.load('keremberke/yolov5m-license-plate')
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False  # NMS multiple labels per box
model.max_det = 1000  # maximum number of detections per image


# Function to perform OCR on the detected license plate region
def perform_ocr(image):
    # Perform OCR using pytesseract
    text = pytesseract.image_to_string(image, config='--psm 7')
    return text


# Define endpoint for object detection and OCR
@app.route('/detect', methods=['POST'])
def detect_objects():
    # Receive base64 encoded image from request
    try:
        data = request.json
        encoded_image = data[0]['image']

        # Decode base64 image and convert to PIL image
        image_bytes = base64.b64decode(encoded_image)
        image = Image.open(BytesIO(image_bytes))
        flipped_image = image.rotate(-90, expand=True)
        # Perform inference
        results = model(flipped_image)
        #results.show()
        # Parse results and perform OCR on license plate regions
        bounding_boxes_with_text = []
        predictions = results.pred[0]
        for box in predictions:
            x1, y1, x2, y2, score, category = box.tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            if int(category) == 0:  # Assuming license plate category is 0
                license_plate_region = image.crop((x1, y1, x2, y2))
                plate_text = perform_ocr(license_plate_region)
                bounding_boxes_with_text.append({
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2,
                    'score': score,
                    'category': category,
                    'plate_text': plate_text
                })

    # Return JSON response with bounding box coordinates and plate text
        print("Bounding boxes with text:", bounding_boxes_with_text)
        return jsonify(bounding_boxes_with_text)
    except Exception as e:
        print(str(e))
        return jsonify(str(e))


# Run Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
