'''
Handles the creation of the model. Since it exported as a pkl file,
I might just delete this file. Either way it'll exist as record
'''
# lol
import warnings 
warnings.filterwarnings('ignore')

# Basic 
import numpy as np  
import pandas as pd

# Clustering and Metrics 
from sklearn.cluster import KMeans 
from sklearn.preprocessing import StandardScaler 
from sklearn.pipeline import Pipeline 

## Managing the model
import pickle

## Read in data
data = pd.read_csv('data.csv')

## Get numeric cols
X = data.select_dtypes(np.number)

## Create Model
song_cluster_pipeline = Pipeline([('scaler',StandardScaler()), 
                                  ('kmeans', KMeans(n_clusters=20, verbose=False, n_init=4))], verbose=False) 

## Fit to numerical columns
song_cluster_pipeline.fit(X) 

## Create pkl
pickle.dump(song_cluster_pipeline, open('song_cluster_pipeline.pkl','wb'))

