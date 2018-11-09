#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
import json
import pickle
from werkzeug.utils import secure_filename
from predict_disease import predict_disease

def create_app():
    app = Flask(__name__)

    app_data = {
        "name":         "Disease Identification Using Images",
        "description":  "Flask application for WT-2 Project",
        "author":       "Hardik Mahipal Surana",
        "html_title":   "Home",
        "project_name": "Disease Identification Using Images",
        "keywords":     "flask, webapp, machine learning"
    }

    photos = UploadSet('photos', IMAGES)
    app.config['UPLOADED_PHOTOS_DEST'] = './static/'
    configure_uploads(app, photos)

    @app.route('/')
    def index():
        return render_template('index.html', app_data=app_data)

    @app.route('/b1')
    def b1():
        return render_template('b1.html', app_data=app_data)

    # # getting our trained model from a file we created earlier
    # model = pickle.load(open("./model/model.pkl","rb"), encoding='utf-8')

    @app.route('/predict', methods=['POST'])
    def predict():
        #grabbing a set of wine features from the request's body
        feature_array = json.loads(request.data)['feature_array']
        # feature_array = request.get_json()['feature_array']
        
        #our model rates the wine based on the input array
        prediction = model.predict([feature_array]).tolist()
        
        #preparing a response object and storing the model's predictions
        response = {}
        response['predictions'] = prediction
        
        #sending our response object back as json
        return jsonify(response)

    # getting our trained model from a file we created earlier
    # model = pickle.load(open("./model/data/model_info/alexnet_trained_model.pkl","rb"), encoding='utf-8')
    
    @app.route('/classify_tomato', methods=['GET', 'POST'])
    def classify_tomato():
        if request.method == 'POST' and 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            result = predict_disease('./static/' + filename)
            return render_template('result.html', app_data={"result" : result})

        return render_template('upload.html', app_data=app_data)
    
    return app




# ------- PRODUCTION CONFIG -------
#if __name__ == '__main__':
#    app.run()



# ------- DEVELOPMENT CONFIG -------
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)