import io
import os

from PIL import Image, ImageFilter, ImageDraw, ImageFont

import uuid


def gender_stats(json_faces):
    # data is binary, but can be URI
    #faces = self.detect_faces(data)
    faces = json_faces

    females = 0
    for face in faces:
        fa = face["faceAttributes"]
        if fa["gender"] == "female":
            females = females + 1

    result = {}
    result["female"] = females
    result["total"] = len(faces)


    # Get women percentage
    percent = 0
    n_faces = len(faces)
    if (n_faces) > 0:
        percent = 100 * females / n_faces
    percent = int(percent)

    result["percent"] = percent
    score = (50-abs(50-percent))*0.2
    result["score"] = score

    mytext = "{}% female. Score: {}".format(percent, score)

    result["text"] = mytext

    return result


def draw_rect(drawcontext, xy, outline=None, width=0):
    (x1, y1), (x2, y2) = xy
    points = (x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)
    drawcontext.line(points, fill=outline, width=width)
    return drawcontext

def draw_label(drawcontext, xy, text):
    # get a font
    fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 60)

    #xy = (xy[0]-20, xy[1]-70)
    xy = (xy[0] + 10, xy[1])

    drawcontext.text(xy, text, font=fnt, fill="black")
    return drawcontext


def process_face(img, rect, gender):
    left = int(rect['left'])
    top = int(rect['top'])
    width = int(rect['width'])
    height = int(rect['height'])

    # Blur face
    box = (left, top, left + width, top + height)
    ic = img.crop(box)
    ic = ic.filter(ImageFilter.GaussianBlur(radius=7))
    img.paste(ic, box)

    # Mark face in rectangle
    box_drawrect = [(left, top), (left+width, top + height)]

    draw = ImageDraw.Draw(img)
    draw_rect(draw, box_drawrect, outline='red', width=10)

    # Label face
    label = gender[:1].upper()
    draw_label(draw, (left, top), label)
    del draw

    return img

def my_logic(imgbytes, az_client):
    """Give an image, some annotations and return what you need in the template
    """

    #imgpil = Image.open(io.BytesIO(imgbytes))  # Pillow library

    imgpil = imgbytes

    # Detect faces
    img_path = '/tmp/{}.png'.format(uuid.uuid1())
    imgpil.save(img_path,'PNG')  # Better not to store in hard disk
    faces_raw = az_client.face_detect(img_path)
    os.remove(img_path)  # No longer needed


    for face in faces_raw:
        rect = face['faceRectangle']
        gender = face['faceAttributes']['gender']
        imgpil = process_face(imgpil, rect, gender)

    stats = gender_stats(faces_raw)


    # Pillow image to PNG bytearray
    imgbuffer = io.BytesIO()
    imgpil.save(imgbuffer, 'PNG')
    imgpng = imgbuffer.getvalue()
    return (imgpng, stats)
