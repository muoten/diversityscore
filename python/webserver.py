import base64
import uuid

import bottle
from PIL import Image
from bottle import route, run, request, view

from .vision.azure_api import Azure_API
from . import config
from . import logic


@route('/')
@view('capture')
def capture():
    return None


@route('/image', method='POST')
@view('result')
def result():
    # #imgb64 = request.forms.get("image")
    # imgb64 = request.files.get("image")
    # print(type(imgb64))
    # if imgb64.startswith('data:'):  # data:image/png;base64,iVB
    #     imgb64 = imgb64[imgb64.find(',')+1 : ]
    # imgbytes = base64.b64decode(imgb64)  # Image is bytes b''

    file = __getdata(request)
    img_file = open(file, "rb")
    imgbytes = Image.open(file)
    #imgbytes = open(request.files['image'].filename, "rb")
    img_png, stats = logic.my_logic(imgbytes, az_client)
    return {
        "image": b"data:image/png;base64,"+base64.b64encode(img_png),
        "stats": stats
    }


def __getdata(request):
    if request.method == 'POST':
        file = request.files['image']

    uid = uuid.uuid4()
    FILE_TMP = "/tmp/myimage_{}.png".format(uid)
    file.save(FILE_TMP)

    return FILE_TMP


if __name__=="__main__":
    #Clients you will need
    az_client = Azure_API(config.AZURE_KEY, config.AZURE_URL)

    # Webserver
    bottle.TEMPLATE_PATH = [config.BOTTLE_PATH_VIEWS]
    bottle.BaseRequest.MEMFILE_MAX = config.BOTTLE_MAX_BYTES_BODY
    run(host=config.BOTTLE_HOST, port=config.BOTTLE_PORT)
