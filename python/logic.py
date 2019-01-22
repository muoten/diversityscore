import io
import os

from PIL import Image, ImageFilter, ImageDraw, ImageFont

import uuid

#RACE_THRESHOLD = 0.3
RACE_THRESHOLD = 0.4

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
    result["score"] = "{0:.1f}".format(score)

    mytext = "{0}% female. Score: {1:.1f}".format(percent, score)

    result["text"] = mytext

    return result

def diversity_stats(json_faces):
    # data is binary, but can be URI
    #faces = self.detect_faces(data)
    faces = json_faces

    females = 0
    non_white = 0
    for face in faces:
        fa = face["faceAttributes"]
        if fa["gender"] == "female":
            females = females + 1

        if (fa["race"] != 'white') and (max(fa["race_score"]) > RACE_THRESHOLD):
            non_white = non_white+1

    result = {}
    result["female"] = females
    result["total"] = len(faces)
    result["non_white"] = non_white

    result = update_stats_helper(result)

    return result

def update_stats_helper(result):
    n_faces = result["total"]
    females = result["female"]
    non_white = result["non_white"]

    # Get women percentage
    percent = 0

    if (n_faces) > 0:
        percent = 100 * females / n_faces
    percent = int(percent)

    # Get race percentage
    race_percent = 0

    if (n_faces) > 0:
        race_percent = 100 * non_white / n_faces
    race_percent = int(race_percent)

    result["percent"] = percent
    result["race_percent"] = race_percent
    gender_score = (50-abs(50-percent))*0.2
    race_score = (100-abs(20-race_percent))*0.1
    score = (gender_score + race_score)/2.0
    result["score"] = "{0:.1f}".format(score)

    mytext = "{0}% female, {1}% non caucasian. Score: {2:.1f}".format(percent, race_percent, score)

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


def process_face(img, rect, gender, race, race_score):
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
    color = "white"

    # Label face
    # Gender with first letter
    label = gender[:1].upper()

    width = int(max(race_score)*20)
    if (race != 'white') and (max(race_score) > RACE_THRESHOLD):
        color = 'green'

    draw_label(draw, (left, top), label)
    draw_rect(draw, box_drawrect, outline=color, width=width)
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
        race = face['faceAttributes']['race']
        imgpil = process_face(imgpil, rect, gender, race, face['faceAttributes']['race_score'])

    stats = diversity_stats(faces_raw)


    # Pillow image to PNG bytearray
    imgbuffer = io.BytesIO()
    imgpil.save(imgbuffer, 'PNG')
    imgpng = imgbuffer.getvalue()
    return (imgpng, stats)
