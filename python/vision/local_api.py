import requests
import json
from .face_aligner import *
from PIL import Image
import pprint

# docker run -p 8501:8501 -v ~/projects/race_gender_recognition/export:/models/my_model -e MODEL_NAME=my_model -t tensorflow/serving

class Local_API:
    def __init__(self):
        self.image_size = 200

        self.gender_categories = ['male', 'female']
        self.race_categories = ['white', 'black', 'asian', 'indian', 'others']


    def _normalize(self,x):
        """
        Normalize a list of sample image data in the range of 0 to 1
        : x: List of image data.  The image shape is (32, 32, 3)
        : return: Numpy array of normalized data
        """
        return np.array((x - np.min(x)) / (np.max(x) - np.min(x)))


    def _detect_faces(self,img):

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("/home/milhouse/projects/diversityscore/resources/mdl/shape_predictor_68_face_landmarks.dat")

        fa = FaceAligner(predictor, desiredFaceWidth=200)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.uint8)

        rects = detector(gray, 2)
        # loop over the face detections

        max_area = 0

        for rect in rects:
            # extract the ROI of the *original* face, then align the face
            # using facial landmarks

            (x, y, w, h) = rect_to_bb(rect)

            if w * h > max_area:
                max_area = w * h
                faceAligned = fa.align(img, gray, rect)

        return rects

    def face_detect(self, file_url=None):

        with open('resources/dummy4.json') as f:
            data = json.load(f)
        #pprint.pprint(data)
        #print(type(data))
        return data


    def _face_detect(self, file_url=None):



        image = cv2.imread(file_url)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = image.astype(np.float32)

        # image = load_image(image_path)

        img = Image.fromarray(image.astype('uint8'), 'RGB')
        #img.show()

        faces = self._detect_faces(image)
        predictor = dlib.shape_predictor(
            "/home/milhouse/projects/diversityscore/resources/mdl/shape_predictor_68_face_landmarks.dat")


        fa = FaceAligner(predictor, desiredFaceWidth=200)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.uint8)
        instances = []
        rectangles = []
        for face in faces:
            faceAligned = fa.align(image, gray, face)
            image_aligned = np.reshape(faceAligned, (self.image_size, self.image_size, 3))

            image_aligned = self._normalize(image_aligned)
            img = Image.fromarray(faceAligned.astype('uint8'), 'RGB')
            #img.show()
            element = {"image": image_aligned.tolist()}
            instances.append(element)

            left = face.left()
            top = face.top()
            width = face.right() - left
            height = face.bottom() - top
            rectangle = {"top": str(top), "left": str(left), "height": str(height), "width": str(width)}
            rectangles.append(rectangle)

        data_dict = {
            "instances" : instances
        }

        data = json.dumps(data_dict)

        json_response = requests.post("http://localhost:8501/v1/models/my_model/versions/3:predict", data=data)


        # Extract text from JSON
        response = json.loads(json_response.text)

        predictions = response['predictions']

        result_dict = []

        for i in range(len(faces)):
            element = {}
            gender = self.gender_categories[predictions[i]["gender"]]
            race = self.race_categories[predictions[i]["race"]]
            #if max(predictions[i]["race_score"]) < 0.39:
            #    race = "undefined"
            element["faceAttributes"] = {"gender":gender, "race":race, "race_score": predictions[i]["race_score"]}
            element["faceRectangle"] = rectangles[i]
            result_dict.append(element)

        #myjson = json.dumps(result_dict)

        return result_dict


## Test faces

if __name__=="__main__":
    import io
    import os
    import sys

    # FILE_IMAGE = "/home/milhouse/Imágenes/naomi.jpeg"
    FILE_IMAGE = "/home/milhouse/projects/diversityscore/resources/img/ironhack.png"
    # FILE_IMAGE = "/home/milhouse/projects/diversityscore/resources/img/startmeapp2.jpg"

    client = Local_API()
    faces = client.face_detect(file_url=FILE_IMAGE)