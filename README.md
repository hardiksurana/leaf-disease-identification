Setup Instructions
```
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
cd code
python3 model/preprocess.py
python3 model/alexnet.py
python3 flaskr/app.py
```
Dataset can be found [here](https://drive.google.com/file/d/1DVy0LyUUfJciyo7BUFm1sHKSRdTVJgjF/view)