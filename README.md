# Diversifynd

**Diversifynd** is a platform that supports diversity.
- Users can check which events or organizations have a better degree of representation in term of gender or race.
- For this purpose computer vision is applied to images of these events or organizations

## Deploy
Build image for demo web and REST service.
```
docker build . -t diversifynd/web
```
Build image for our custom race and gender recognition model. Based on Tensorflow/serving and project https://github.com/zZyan/race_gender_recognition
```
docker build . -t diversifynd/model -f Dockerfile.model
```
Launch race and gender recognition model
```
docker run -e "PORT=8501" -p 8501:8501 diversifynd/model
```
Launch demo web and REST service
```
docker run -e "PORT=8080" -p 8080:8080 diversifynd/web
```

And browse localhost:8080

REST API:

- `/stats` [POST]
    - arguments [multipart/form-data]:
        - image
        - female
        - non_white
        - total
    - return [application/json]:
        - image
        - pic_stats
        - stats
    - Example: 
        - `curl -F "image=@resources/img/ironhack.png" -F "female=0" -F "total=4" -F "non_white=1" https://localhost:8080/stats` 
