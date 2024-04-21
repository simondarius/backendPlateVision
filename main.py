from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
import requests
import yolov5
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup

app = Flask(__name__)


model = yolov5.load('keremberke/yolov5m-license-plate')
model.conf = 0.25
model.iou = 0.45
model.agnostic = False
model.multi_label = False
model.max_det = 1000

API_URL = "https://api-inference.huggingface.co/models/microsoft/trocr-large-str"
headers = {"Authorization": "Bearer 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"}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///car_database.db'
db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serie_caroserie = db.Column(db.String(100))
    numar_inmatriculare = db.Column(db.String(20))
    model_name = db.Column(db.String(100))
    unitate = db.Column(db.String(100))
    data_furtului = db.Column(db.String(20))
    culoare = db.Column(db.String(20))
    detalii = db.Column(db.String(500))

def scrape_page(page_number):
    url = f"https://www.politiaromana.ro/ro/auto-furate&page={page_number}"
    response = requests.get(url,verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    car_list = []

    for listBoxAfisare in soup.find_all("div", class_="listBoxAfisare"):
        car_data = {}
        serie_caroserie = listBoxAfisare.find("div", class_="listBoxLeft2").find("b").text.strip()
        numar_inmatriculare = listBoxAfisare.find("div", class_="listBoxLeft3").find("b").text.strip()
        model_name = listBoxAfisare.find("div", class_="listBoxRight2").find("a").text.strip()
        car_data["serie_caroserie"] = serie_caroserie
        car_data["numar_inmatriculare"] = numar_inmatriculare
        car_data["model_name"] = model_name
        car_list.append(car_data)

    return car_list

@app.route('/scrape', methods=['GET'])
def scrape_and_save_to_database():
    try:
        db.create_all()
        for page_number in range(1, 2255):
            car_list = scrape_page(page_number)
            for car_data in car_list:
                car = Car(**car_data)
                db.session.add(car)

        db.session.commit()

        return jsonify({"message": "Scraping and saving to database successful."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/car-info/<license_plate>', methods=['GET'])
def get_car_info(license_plate):
    car = Car.query.filter_by(numar_inmatriculare=license_plate).first()

    if car:
        print(f"GOT A REQUEST FOR LICENSE PLATE {license_plate} . STOLEN!")
        return jsonify({
            'response':'STOLEN',
            'license_plate': car.numar_inmatriculare,
            'car_model': car.model_name,
            'car_color': car.culoare,
            'detalii':car.detalii,
            'serie_caroserie':car.serie_caroserie,
            'unitate': car.unitate,
            'data_furtului': car.data_furtului,
        })
    else:
        print(f"GOT A REQUEST FOR LICENSE PLATE {license_plate} . NOT STOLEN!")
        return jsonify({'response': 'CLEAN','license_plate':license_plate})



@app.route('/detect', methods=['POST'])
def detect_objects():
    try:
        data = request.json
        encoded_image = data[0]['image']
        image_bytes = base64.b64decode(encoded_image)
        image = Image.open(BytesIO(image_bytes))
        flipped_image = image.rotate(-90, expand=True)

        results = model(flipped_image)
        bounding_boxes_with_text = []
        predictions = results.pred[0]
        for box in predictions:
            x1, y1, x2, y2, score, category = box.tolist()
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            if int(category) == 0:
                plate_image = flipped_image.crop((x1, y1, x2, y2))
                plate_image=plate_image.convert('RGB')
                buffered = BytesIO()
                plate_image.save(buffered, format="JPEG")
                plate_image_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

                bounding_boxes_with_text.append({
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2,
                    'score': score,
                    'category': category,
                    'cropped_image_base64': plate_image_base64
                })
        return jsonify(bounding_boxes_with_text)
    except Exception as e:

        print(str(e))
        return jsonify(str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
