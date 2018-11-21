#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_uploads import UploadSet, configure_uploads, IMAGES
import json
import pickle
from werkzeug.utils import secure_filename
from predict_disease import predict_disease
from models import models
import os
from flaskext.mysql import MySQL
import ast


def create_app():
    mysql = MySQL()
    app = Flask(__name__)
    app.secret_key = 'webtechproject'
    app_data = {
        "name":         "Disease Identification Using Images",
        "description":  "Flask application for WT-2 Project",
        "author":       "Harsh Garg, Gaurav Peswani, Hardik Mahipal Surana",
        "html_title":   "Home",
        "project_name": "Disease Identification Using Images",
        "keywords":     "flask, webapp, machine learning"
    }

    app.config["MYSQL_DATABASE_USER"] = 'root'
    app.config["MYSQL_DATABASE_PASSWORD"] = 'ubuntu'
    app.config["MYSQL_DATABASE_DB"] = "leafDiseaseIdentification"
    app.config["MYSQL_DATABASE_HOST"] = "localhost"
    mysql.init_app(app)

    photos = UploadSet('photos', IMAGES)
    app.config['UPLOADED_PHOTOS_DEST'] = './static/'
    configure_uploads(app, photos)

    @app.route('/')
    def index():
        return render_template('index.html', app_data=app_data)

    @app.route("/login",methods=["GET","POST"])
    def login():
        if (request.method == "GET"):
            
            return render_template("login.html")

        elif (request.method == "POST"):
            
            POST_USERNAME=str(request.form["username"])
            POST_PASSWORD=str(request.form["password"])
            
            print(POST_USERNAME)
            print(POST_PASSWORD)
           

            session["username"] = POST_USERNAME

            query = "SELECT name from register where username='" + session["username"] + "'"
            print("query is ",query)
            conn = mysql.connect()
            cursor = conn.cursor()
            res = cursor.execute(query)
            data = cursor.fetchall()
            print("data for details of user is ",data)
            nameOfUser = data[0][0]
            session["nameOfUser"] = nameOfUser


            print("session['username'] is ",session["username"])
            # Make DB query to see if User with 'email' and 'acc_type'
            # has the same password as in the DB.
            result = models.loginCheck(mysql,POST_USERNAME,POST_PASSWORD)
            # if (result=="Error"):
            #     flash("Error")
            print("result is ", result)


            if (result==True):
                return redirect(url_for("classify_tomato"))
            else:
                flash('wrong password!')
                return redirect(url_for("login"))
        else:
            flash("Error")

    @app.route('/b1')
    def b1():
        return render_template('b1.html', app_data=app_data)

    # # getting our trained model from a file we created earlier
    model = pickle.load(open("./model/model.pkl","rb"), encoding='utf-8')

    @app.route("/register",methods=["GET","POST"])
    def register_user():
        if (request.method=="GET"):
            # print("nameList is ",nameList)
            # print("emailList is ",emailList)
            # print("usernamesList is ",usernamesList)
            # print("passwordList is ",passwordList)
            return render_template("register.html",title="Patient")

        elif (request.method == "POST"):
            newUserDict = {
                "name" : str(request.form["name"]),
                "email" : str(request.form["email"]),
                "username" : str(request.form["username"]),
                "password" : str(request.form["password"]),
            }

            if not models.isExistingUser(mysql,newUserDict["username"]):
                # nameList.append(newUserDict["name"])
                # emailList.append(newUserDict["email"])
                # usernamesList.append(newUserDict["username"])
                # passwordList.append(newUserDict["password"])
                res = models.insertNewUser(mysql,newUserDict)
                if(res == True):

                    return redirect(url_for("login"))
                else:
                    return redirect(url_for("register"))
            else:

                return redirect(url_for("login"))


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



        return render_template('upload.html', app_data=app_data, name=session["nameOfUser"])


    @app.route('/logout',methods=["GET","POST"])
    def logout():
        print("Inside logout")
        if(request.method=="GET" and request.args.get("logout", "", type=int) == 1):
            try:
                session.pop("username")
            except KeyError:
                pass
            try:
                session.pop("nameOfUser")
            except:
                pass

            return redirect(url_for("login"))

        return render_template("login.html")


    # @app.route('/getDetailsOfUser', methods=['GET','POST'])
    # def getDetailsOfUser():
    #     if(request.method == 'GET'):
    #         # res = models.getDetailsOfUser(mysql,session["username"])
    #         query = "SELECT name from register where username='" + session["username"] + "'"
    #         print("query is ",query)
    #         conn = mysql.connect()
    #         cursor = conn.cursor()
    #         res = cursor.execute(query)
    #         data = cursor.fetchall()
    #         print("data for details of user is ",data)
    #         nameOfUser = data[0][0]

    #         return render_template("register.html",title="Patient")


    @app.route('/fetch_multistage', methods=['GET'])
    def fetch_multistage():
        print(request.files)
        FILES_LOC = "/home/harshgarg/Desktop/7thSem/WebTech-Project/WT-2/code/flaskr/static/text_for_msd/"
        if request.method == 'GET':
            if request.args.get("image", "", type=int) == 1:
                FILE_NAME = "images.json"
            elif request.args.get("link", "", type=int) == 1:
                FILE_NAME = "links.json"
            else:
                FILE_NAME = "content.json"
            file_ = open(FILES_LOC + FILE_NAME, 'r')
            res = file_.read()
            # print(res, type(res))
            return res
        return "Invalid fetch"


    return app



# ------- PRODUCTION CONFIG -------
#if __name__ == '__main__':
#    app.run()



# ------- DEVELOPMENT CONFIG -------
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
