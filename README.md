# Diversifynd

**Diversifynd** is a platform that supports diversity.
- Users can check which events or organizations have a better degree of representation in term of gender or race.
- For this purpose computer vision is applied to images of these events or organizations

## Install
Create virtualenv.
```
virtualenv -p python3 diversifynd
```
Install requirements
```
pip install -r requirements.txt
```

## Launch
```
python -m python.webserver
```
And browse localhost:8080

Examples:
- POST request
```curl -F "image=@myfile.jpg" http://localhost:8080/image```
- JSON response on `resources/result.json`
