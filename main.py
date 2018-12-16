from flask import Flask, render_template, send_file, make_response
from flask import jsonify
from gender_detector import GenderDetector
app = Flask(__name__)
import os
from PIL import Image
from io import BytesIO

import random
from io import StringIO

from flask import Flask, make_response, request, flash, redirect
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import patches

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

@app.route('/plot.png')
def plot():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)

    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]

    axis.plot(xs, ys)
    canvas = FigureCanvas(fig)
    output = StringIO()
    canvas.print_png(output)
    response = make_response(output.getvalue())
    response.mimetype = 'image/png'
    return response



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

    print(file.filename)
    FILE_IN = "/tmp/myimage.png"
    file.save(FILE_IN)

    return send_file(FILE_IN, mimetype='image/png')


@app.route('/upload_tmp', methods=['GET', 'POST'])
def upload_tmp():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

    print(file.filename)
    FILE_IN = "/tmp/myimage"
    file.save(FILE_IN)


    #imagefile = file.filename

    #URI = r'/home/milhouse/projects/diversityscore/img/startmeapp2.jpg'
    URI = FILE_IN

    image_data = open(URI, "rb")

    #image_data = request.data
    #image_data = file
    faces = detector.detect_faces_from_binary(image_data)
    print(faces)

    #image = Image.open(FILE_IN)
    #image = Image.open(URI)
    #image = image_data
    plt.figure(figsize=(8, 8))
    #ax = plt.imshow(image, alpha=0.6)

    image = plt.imread(FILE_IN)
    ax = plt.subplots()
    #ax.imshow(image)
    for face in faces:
        fr = face["faceRectangle"]
        fa = face["faceAttributes"]
        origin = (fr["left"], fr["top"])
        p = patches.Rectangle(
            origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
        ax.add_patch(p)
        plt.text(origin[0], origin[1], "%s" % (fa["gender"].capitalize()),
                 fontsize=10, weight="bold", va="bottom")
    # plt.axis("off")

    FILE_OUT = "/tmp/myout"

    plt.savefig(FILE_OUT)

    return send_file(FILE_OUT, mimetype='image/png')


@app.route('/upload2', methods=['GET', 'POST'])
def upload2():
    print(request.files)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

    print(file.filename)
    FILE_IN = "/tmp/myimage.png"
    file.save(FILE_IN)

    image_data = open(FILE_IN, "rb")

    # image_data = request.data
    # image_data = file
    faces = detector.detect_gender_from_binary(image_data)
    print(faces)

    #headers = {'content-type': 'text/plain'}
    #response = make_response(faces, 200)
    #response.headers = headers

    percent = int(faces["female"])*1.0/int(faces["total"])
    print(percent)
    percent = percent * 100
    percent = int(percent)
    print(percent)
    mytext = "{}".format(percent)
    return mytext
    #return jsonify(faces)


if __name__ == "__main__":
    MY_KEY = os.environ["AZURE_FACE_API_KEY"]
    detector = GenderDetector(MY_KEY)
    app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'

    #sess.init_app(app)
    app.run(host='0.0.0.0', port=5000)