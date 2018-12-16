from flask import Flask
from flask import jsonify
from gender_detector import GenderDetector
app = Flask(__name__)
import os
from PIL import Image
from io import BytesIO

@app.route("/")
def hello():

    return "Hello World!"

@app.route("/gender")
def gender():
    URI = r'/home/milhouse/projects/diversityscore/img/startmeapp2.jpg'

    result = detector.detect_gender(URI)
    json = jsonify(result)

    return json

@app.route("/gender2")
def gender2():
    URI = r'/home/milhouse/projects/diversityscore/img/startmeapp2.jpg'

    image_data = open(URI, "rb")
    result = detector.detect_gender_from_binary(image_data)
    json = jsonify(result)

    return json

if __name__ == "__main__":
    MY_KEY = os.environ["AZURE_FACE_API_KEY"]
    detector = GenderDetector(MY_KEY)
    app.run(host='0.0.0.0', port=5000)