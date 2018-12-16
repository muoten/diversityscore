import cognitive_face as CF

class GenderDetector():

    def __init__(self, key):
        print("Init GenderDetector")
        CF.Key.set(key)

        BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
        CF.BaseUrl.set(BASE_URL)
        self.CF = CF

    def detect_gender_from_binary(self, data):

        faces = self.CF.face.detect(data, attributes='gender')
        return faces

    def detect_gender(self, URI):
        faces = self.CF.face.detect(URI, attributes='gender')
        females = 0
        for face in faces:
            fa = face["faceAttributes"]
            if fa["gender"] == "Female":
                females = females+1

        result = {}
        result["female"] = females
        result["total"] = len(faces)
        return result