import numpy as np 
import pandas as pd 
import pickle

data = pd.read_csv('data.csv')
X = data.select_dtypes(np.number)

song_cluster_pipeline = pickle.load(open('song_cluster_pipeline.pkl','rb'))
song_cluster_labels = song_cluster_pipeline.predict(X) 
data['cluster_label'] = song_cluster_labels

data.to_csv('predicted.csv')
