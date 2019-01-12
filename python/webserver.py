import base64
import uuid

import bottle
from PIL import Image
from bottle import route, run, request, view

from .vision.azure_api import Azure_API
from .vision.local_api import Local_API
from . import config
from . import logic
import json


@route('/')
@view('capture')
def capture():
    return None

@route('/image_web', method='POST')
@view('result')
def image_web():
    return result()

def merge_images_h(image1, image2):
    """Merge two images into one, displayed side by side
    :param file1: path to first image file
    :param file2: path to second image file
    :return: the merged Image object
    """
    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = width1 + width2
    result_height = max(height1, height2)

    if image1.height < result_height:
        hpercent = (result_height/float(height1))
        vsize = int((float(width1)*float(hpercent)))
        image1 = image1.resize((vsize,result_height), Image.ANTIALIAS)
        result_width = vsize + width2

    if image2.height < result_height:
        hpercent = (result_height/float(height2))
        vsize = int((float(width2)*float(hpercent)))
        image2 = image2.resize((vsize,result_height), Image.ANTIALIAS)
        result_width = vsize + width1

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(width1, 0))
    return result

def merge_images(image1, image2):
    """Merge two images into one, displayed side by side
    :param file1: path to first image file
    :param file2: path to second image file
    :return: the merged Image object
    """

    (width1, height1) = image1.size
    (width2, height2) = image2.size

    result_width = max(width1, width2)
    result_height = height1+ height2

    if image1.width < result_width:
        wpercent = (result_width/float(width1))
        hsize = int((float(height1)*float(wpercent)))
        image1 = image1.resize((result_width,hsize), Image.ANTIALIAS)

    if image2.width < result_width:
        wpercent = (result_width/float(width2))
        hsize = int((float(height2)*float(wpercent)))
        image2 = image2.resize((result_width,hsize), Image.ANTIALIAS)

    result = Image.new('RGB', (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(0, height1))
    return result

@route('/image', method='POST')
def result():

    file_list = __getdata(request)
    #img_file = open(file, "rb")

    imgbytes = Image.open(file_list[0])
    if (len(file_list) > 1):
        for i in range(len(file_list)-1):
            imgbytes = merge_images_h(imgbytes, Image.open(file_list[i+1]))

    #imgbytes = open(request.files['image'].filename, "rb")
    img_png, stats = logic.my_logic(imgbytes, az_client)
    result = {
        "image": r"data:image/png;base64,"+base64.b64encode(img_png).decode('ascii'),
        "stats": stats
    }

    return result


def __getdata(request):
    if request.method == 'POST':
        files = request.files.getall('image')
        mylist = []
        for file in files:

            uid = uuid.uuid4()
            FILE_TMP = "/tmp/myimage_{}.png".format(uid)
            file.save(FILE_TMP)
            mylist.append(FILE_TMP)

    return mylist


if __name__=="__main__":
    #Clients you will need
    #az_client = Azure_API(config.AZURE_KEY, config.AZURE_URL)
    az_client = Local_API()

    # Webserver
    bottle.TEMPLATE_PATH = [config.BOTTLE_PATH_VIEWS]
    bottle.BaseRequest.MEMFILE_MAX = config.BOTTLE_MAX_BYTES_BODY
    run(host=config.BOTTLE_HOST, port=config.BOTTLE_PORT)
