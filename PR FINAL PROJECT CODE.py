# -*- coding: utf-8 -*-
"""PR Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cSVHQTqexgFU0x0uGxzi1l-vHbnyYs_6
"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.svm import SVC 
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# This method will calculate time-domain feature of each dataset consist of 480 sequence of data and create a new dataset that we will used to recognized the activity.
def get_dataset():
  res=os.listdir("Dataset/AReM/")
  res.remove('bendingType.pdf')  
  res.remove('sensorsPlacement.pdf')
  final_dataset=[]
  for i in res:
    temp=os.listdir("Dataset/AReM/"+i)
    for j in temp:
      df=pd.read_csv(f"Dataset/AReM/{i}/{j}",skiprows=4,usecols=range(1,7),index_col=False)
      mean=df.mean()
      median=df.median()
      mode=df.mode()
      mode=mode.values
      std=df.std()
      var=df.var()
      cov=df.cov().values.tolist()
      min=df.min()
      max=df.max()
      dataframe=[]
      for k in range(0,6):
        dataframe.append(mean[k])
        dataframe.append(median[k])
        if (len(mode)>0):
          dataframe.append(mode[0][k])
        else:
          dataframe.append(np.nan)
        dataframe.append(std[k])
        dataframe.append(var[k])
        dataframe.append(cov[0][k])
        dataframe.append(max[k])
        dataframe.append(min[k])
      dataframe.append(i)
      final_dataset.append(dataframe)
  columns=["mean_avg_rss12","median_avg_rss12","mode_avg_rss12","std_avg_rss12","variance_avg_rss12","covariance_avg_rss12","max_avg_rss12","min_avg_rss12",
          "mean_var_rss12","median_var_rss12","mode_var_rss12","std_var_rss12","variance_var_rss12","covariance_var_rss12","max_var_rss12","min_var_rss12",
          "mean_avg_rss13","median_avg_rss13","mode_avg_rss13","std_avg_rss13","variance_avg_rss13","covariance_avg_rss13","max_avg_rss13","min_avg_rss13",
          "mean_var_rss13","median_var_rss13","mode_var_rss13","std_var_rss13","variance_var_rss13","covariance_var_rss13","max_var_rss13","min_var_rss13",
          "mean_avg_rss23","median_avg_rss23","mode_avg_rss23","std_avg_rss23","variance_avg_rss23","covariance_avg_rss23","max_avg_rss23","min_avg_rss23",
          "mean_var_rss23","median_var_rss23","mode_var_rss23","std_var_rss23","variance_var_rss23","covariance_var_rss23","max_var_rss23","min_var_rss23",
          "Position"]
  final_dataset=pd.DataFrame(final_dataset)
  final_dataset.columns=columns
  return final_dataset

# This method will be used to remove all the NAN values by replacing with mean.
def remove_nan(final_dataset):
  columns=final_dataset.columns
  for i in range(0,48):
    # print(final_dataset[columns[i]].isnull().values.any()) # This will return true if we have any null value in dataset
    final_dataset[columns[i]].fillna((final_dataset[columns[i]].mean()), inplace=True)
  return final_dataset

# This method will be used to split dataset in training and testing data and scale it.
def dataset_split(final_dataset):
  X_train, X_test, y_train, y_test = train_test_split(final_dataset.iloc[:,:-1], final_dataset.iloc[:,-1:],train_size = .55, random_state=1, stratify=final_dataset.iloc[:,-1:])
  sc = StandardScaler()
  sc.fit(X_train)
  X_train = sc.transform(X_train)
  X_test = sc.transform(X_test)
  return X_train,X_test,y_train.values.ravel(),y_test.values.ravel()

# This method will calculate the accuracy of the logistic regression model
def Accuracy_logistic_regression(model,X_test,y_test):
  y_pred=model.predict(X_test)
  accuracy=accuracy_score(y_test,y_pred)
  print(f"Accuracy of Logistic Regression on Testing Data is {accuracy}")
  cmatrix=confusion_matrix(y_test,y_pred)
  print(f"Confusion Matrix for Logistic Regression {cmatrix}")
  report=classification_report(y_test,y_pred)
  print(f"Classification report for Logistic Regression is ")
  print(f"{report}")
  return accuracy

# This method is to implement logistic regression
def Logistic_regression(X_train, X_test, y_train, y_test):
  cv =StratifiedKFold(n_splits=4, shuffle=True)
  model = LogisticRegression(solver="lbfgs",max_iter=6000)
  score = cross_val_score(model, X_train, y_train, cv=cv)
  print(f"Accuracy of Logistic Regression after applying K-fold Cross Validation {score.mean()}")
  model.fit(X_train,y_train)
  accuracy=Accuracy_logistic_regression(model,X_test,y_test)
  
  return score.mean(),accuracy

# We will do encoding of our target variable for naive bayes algorithm
def label_encoding(final_dataset):
  le=preprocessing.LabelEncoder()
  final_dataset=le.fit_transform(final_dataset)
  return final_dataset;

# This method will be used to implement naive bayes 
def Naive_bayes(X_train, X_test, y_train, y_test):
  model = GaussianNB()
  y_train=label_encoding(y_train)
  y_test=label_encoding(y_test)
  cv =StratifiedKFold(n_splits=4,  shuffle=True)
  score = cross_val_score(model,X_train,y_train, cv=cv)
  print(f"Accuracy of Naive Bayes after applying K-fold Cross Validation {score.mean()}")
  model.fit(X_train,y_train)
  y_pred = model.predict(X_test)
  accuracy=accuracy_score(y_test,y_pred)
  print(f"Accuracy of Naive Bayes on Testing Data is {accuracy}")
  cmatrix=confusion_matrix(y_test,y_pred)
  print(f"Confusion Matrix for Naive Bayes {cmatrix}")
  report=classification_report(y_test,y_pred)
  print(f"Classification report for Naive Bayes is ")
  print(f"{report}")
  return score.mean(),accuracy

# This method will be used to implement Support Vector Machine with Linear Kernel
def Support_vector_machine(X_train, X_test, y_train, y_test):
  svm = SVC(kernel="linear")  
  cv =StratifiedKFold(n_splits=4,  shuffle=True)
  score = cross_val_score(svm, X_train, y_train, cv=cv)
  print(f"Accuracy of Support Vector Machine after applying K-fold Cross Validation {score.mean()}")
  svm.fit(X_train,y_train)
  y_pred=svm.predict(X_test)
  accuracy=accuracy_score(y_test,y_pred)
  print(f"Accuracy of SVM on Testing Data is {accuracy}")
  cmatrix=confusion_matrix(y_test,y_pred)
  print(f"Confusion Matrix for svm {cmatrix}")
  report=classification_report(y_test,y_pred)
  print(f"Classification report for SVM is ")
  print(f"{report}")
  return score.mean(),accuracy

# Drive function
def main():
  final_dataset=get_dataset()
  final_dataset=remove_nan(final_dataset)
  print(final_dataset.head(30))
  print(final_dataset.tail(30))
  X_train, X_test, y_train, y_test=dataset_split(final_dataset)
  lg_score,lg_accuracy=Logistic_regression(X_train, X_test, y_train, y_test)
  nb_score,nb_accuracy=Naive_bayes(X_train, X_test, y_train, y_test)
  svm_score,svm_accuracy=Support_vector_machine(X_train, X_test, y_train, y_test)
  plt.title("Training Accuracy")
  plt.plot(["Logistics Regression","Naive Bayes","Support Vector Machine"],[lg_score,nb_score,svm_score])
  plt.show()
  plt.title("Testing Accuracy")
  plt.plot(["Logistics Regression","Naive Bayes","Support Vector Machine"],[lg_accuracy,nb_accuracy,svm_accuracy])
  plt.show()

main()





