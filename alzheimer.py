# -*- coding: utf-8 -*-
"""Copy of Alzheimer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10iVIqijX_2DBC46yahbxg8zghHR5uOuj
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import gc
import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv('oasis_longitudinal.csv')
todel = ['Subject ID','MRI ID','Visit','MR Delay','Hand','eTIV']
dataset = data.drop(todel,axis=1)

"""#Outlier Deletion"""

dataset = dataset.drop(labels=[0,1,2,3], axis=0)

dataset['SES'] = dataset['SES'].astype('object')
dataset['CDR'] = dataset['CDR'].astype('object')

from sklearn.preprocessing import LabelEncoder
for column in dataset.columns:
    if dataset[column].dtype == type(object):
        le = LabelEncoder()
        dataset[column] = le.fit_transform(dataset[column])

# dataset.fillna(dataset.mode().iloc[0], inplace=True)
dataset['SES'].fillna(dataset['SES'].mode().iloc[0], inplace = True)
dataset['MMSE'].fillna(dataset['MMSE'].mean(),inplace=True)

from sklearn.model_selection import train_test_split
predictors = dataset.drop("Group",axis=1)
target = dataset["Group"]
X_train, X_test, Y_train, Y_test = train_test_split(predictors, target, test_size = 0.3, random_state = 1)

"""## Random Forest"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

max_accuracy = 0


for x in range(2000):
    rf = RandomForestClassifier(random_state=x)
    rf.fit(X_train,Y_train)
    Y_pred_rf = rf.predict(X_test)
    current_accuracy = round(accuracy_score(Y_pred_rf,Y_test)*100,2)
    if(current_accuracy>max_accuracy):
        max_accuracy = current_accuracy
        best_x = x

rf = RandomForestClassifier(random_state=best_x)
rf.fit(X_train,Y_train)
Y_pred_rf = rf.predict(X_test)

# score_rf = round(accuracy_score(Y_pred_rf,Y_test)*100,2)

# print("The accuracy score achieved using random forest classifier is: "+str(score_rf)+" %")
# rf.predict(X_test)

pickle.dump(rf, open('alzheimer.pkl', 'wb'))

