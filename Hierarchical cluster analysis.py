# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 13:03:50 2021

@author: EMMANUEL
"""

#Import Libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Import dataset and create variable
dataset = pd.read_csv('Shopping_center.csv')
X = dataset.iloc[:,3:5].values

#Using Dendogram method to get optimal value of k
from scipy.cluster import hierarchy as sch
#import scipy.cluster.hierarchy as sch is a shorter way
d_gram = sch.dendrogram(sch.linkage(X, method='ward'))
plt.title('Dendogram method')
plt.xlabel('customers')
plt.ylabel('Euclidean distances')
plt.savefig('img_dendogram', dpi=500)
plt.show()

#using the dendogram image we look 4 the maximum distance i.e max height without intersection
#then we draw an horizontal line across this distance and count the number of intersections
#from our dendogram diagram optimum K = 5

#fit agglomerative clustering to data
from sklearn.cluster import AgglomerativeClustering
hc = AgglomerativeClustering(n_clusters=5, affinity='euclidean', linkage='ward')
y_hc = hc.fit_predict(X)

#Visualization of clusters
plt.scatter(X[y_hc==0,0], X[y_hc==0,1], s=100, color='red', label='cluster 1')
plt.scatter(X[y_hc==1,0], X[y_hc==1,1], s=100, color='green', label='cluster 2')
plt.scatter(X[y_hc==2,0], X[y_hc==2,1], s=100, color='blue', label='cluster 3')
plt.scatter(X[y_hc==3,0], X[y_hc==3,1], s=100, color='orange', label='cluster 4')
plt.scatter(X[y_hc==4,0], X[y_hc==4,1], s=100, color='brown', label='cluster 5')
plt.title('Cluster of Customers')
plt.xlabel('Annual Income')
plt.ylabel('spending points')
plt.legend()
plt.show()

