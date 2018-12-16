import cognitive_face as CF
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib import patches

class GenderDetector():

    def __init__(self, key):
        print("Init GenderDetector")
        CF.Key.set(key)

        BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
        CF.BaseUrl.set(BASE_URL)
        self.CF = CF


    def detect_faces_from_binary(self, data):
        faces = self.CF.face.detect(data, attributes='gender')
        return faces

    def detect_gender_from_binary(self, data):

        faces = self.CF.face.detect(data, attributes='gender')
        print(faces)

        females = 0
        for face in faces:
            fa = face["faceAttributes"]
            if fa["gender"] == "female":
                females = females + 1

        result = {}
        result["female"] = females
        result["total"] = len(faces)
        return result

    def detect_gender(self, URI):
        faces = self.CF.face.detect(URI, attributes='gender')
        females = 0
        for face in faces:
            fa = face["faceAttributes"]
            if fa["gender"] == "female":
                females = females+1

        result = {}
        result["female"] = females
        result["total"] = len(faces)
        return result

    def plot_gender(self, data):
        faces = self.CF.face.detect(data, attributes='gender')
        plt.figure(figsize=(8, 8))
        ax = plt.imshow(data, alpha=0.6)
        for face in faces:
            fr = face["faceRectangle"]
            fa = face["faceAttributes"]
            origin = (fr["left"], fr["top"])
            p = patches.Rectangle(
                origin, fr["width"], fr["height"], fill=False, linewidth=2, color='b')
            ax.axes.add_patch(p)
            plt.text(origin[0], origin[1], "%s, %d" % (fa["gender"].capitalize(), fa["age"]),
                     fontsize=20, weight="bold", va="bottom")