# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 10:50:41 2021

@author: EMMANUEL
"""
#Polynomial Regression

#Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Import dataset and create variables
dataset = pd.read_csv('Gaming_data.csv')
#X (independent variables must always be in matrix form)
#to do that we simply change 0 to 0:1.
#python doesnt take upper limit in an index so 0:1 is still 0
X = dataset.iloc[:,0:1].values 
Y = dataset.iloc[:,1].values

#This dataset is too small (10 rows) so we will not split it into test and train sets 

#Fit into Linear Regression
from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(X,Y)

#fit into Polynomial Regression
#a) Transform the normal matrices into polynomial matrices
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree=4)
#note that default degree = 2 but if our degree was 3 we will put degree=3 in the bracket
X_poly = poly_reg.fit_transform(X)

#b) Fit this new polynomial matrice into linear regression
lin2_reg = LinearRegression()
lin2_reg.fit(X_poly,Y)


#Visualizing Linear Regression
plt.scatter(X,Y)
plt.plot(X,lin_reg.predict(X),color='red') 
plt.title('Gaming data(Linear Regression)')
plt.xlabel('Game steps')
plt.ylabel('Game points')
plt.show()

#Visualizing Polynomial Regression
plt.scatter(X,Y)
plt.plot(X,lin2_reg.predict(poly_reg.fit_transform(X)),color='red') 
plt.title('Gaming data(Polynomial Regression)')
plt.xlabel('Game steps')
plt.ylabel('Game points')
plt.show()


#we will keep on changing the degree=? until all polynomial curve touches all the points
#degree=4 was the best suit 


#Predicting new results with Linear Regression
lin_reg.predict([[7.5]])

#Predicting new results with Polynomial Regression
lin2_reg.predict(poly_reg.fit_transform([[7.5]]))

#from the results linear reg = 411,257 which is way wrong
#polynomial reg = 225,126 which is very alright.

