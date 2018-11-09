'''
trains a machine learning model for detecting diseases using images
'''

import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import linear_model

#loading my data and splitting it into training and testing pandas
df = pd.read_csv('./data/winequality-red.csv', delimiter=";")
X_train, X_test, y_train, y_test = train_test_split(df.drop('quality', axis=1), df['quality'], test_size=0.25, random_state=1)

#creating a model and training it
regr = linear_model.RidgeCV(alphas= np.arange(0.1,10.0,.5))
regr.fit(X_train, y_train)

#serializing our model to a file called model.pkl
pickle.dump(regr,open("model.pkl","wb"))

#checking for error
ans = regr.predict(X_test)
print(mean_squared_error(y_test, ans))


#using our trained model to predict a fake wine
#each number represents a feature like pH, acidity, etc.
print(regr.predict([[7.4,0.66,0,1.8,0.075,13,40,0.9978,3.51,0.56,9.4]]).tolist())

pickle.dump(regr, open("model.pkl","wb"))

#loading a model from a file called model.pkl
# model = pickle.load(open("model.pkl","r"))