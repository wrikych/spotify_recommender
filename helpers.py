'''
Handles the recommend_songs() functionalities. Meant to 
be called on, and has all the necessary auxiliaries which include:

------------------
------------------
 
-> Importing the pickle file (currently the entire pipeline)
-> The Spotify Client
-> find_song(), get_song_data(), get_mean_vector(), flatten_dict_list(), recommend_songs()

Imports - to be safe, right now, I'm importing what I need as I go. 
'''
## All imports - 
import numpy as np  
import pandas as pd 
from sklearn.metrics import euclidean_distances 
from scipy.spatial.distance import cdist
import pickle 
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials 
from collections import defaultdict 

## focused on features - 
number_cols = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit', 
 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

## Creating the client
CID, CSECRET = '4e716bc3aa7d41008190fddb1a6a47f6', 'd579bfd23dee46c8926413a166443e75' 
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = CID, 
                                                           client_secret = CSECRET))

## Importing the pickle file
song_cluster_pipeline = pickle.load(open('song_cluster_pipeline.pkl','rb'))

## find_song() --> gets the details of inputed track
def find_song(name, year): 
    song_data = defaultdict() 
    results = sp.search(q= 'track: {} year: {}'.format(name,year), limit=1) 
    if results['tracks']['items'] == []: 
        return None 
    results = results['tracks']['items'][0] 
    track_id = results['id'] 
    audio_features = sp.audio_features(track_id)[0] 
    song_data['name'] = [name] 
    song_data['year'] = [year] 
    song_data['explicit'] = [int(results['explicit'])] 
    song_data['duration_ms'] = [results['duration_ms']] 
    song_data['popularity'] = [results['popularity']] 
    for key, value in audio_features.items(): 
        song_data[key] = value 
    return pd.DataFrame(song_data)

## get_song_data() --> get dataframe specific feature info from spotify
def get_song_data(song, spotify_data): 
     
    try: 
        song_data = spotify_data[(spotify_data['name'] == song['name'])  
                                & (spotify_data['year'] == song['year'])].iloc[0] 
        return song_data 
     
    except IndexError: 
        return find_song(song['name'], song['year'])
    
## get_mean_vector() --> intermediary
def get_mean_vector(song_list, spotify_data): 
     
    song_vectors = [] 
     
    for song in song_list: 
        song_data = get_song_data(song, spotify_data) 
        if song_data is None: 
            print('Warning: {} does not exist in Spotify or in database'.format(song['name'])) 
            continue 
        song_vector = song_data[number_cols].values 
        song_vectors.append(song_vector)   
     
    song_matrix = np.array(list(song_vectors)) 
    return np.mean(song_matrix, axis=0)

## flatten_dict_list() --> intermediary
def flatten_dict_list(dict_list): 
     
    flattened_dict = defaultdict() 
    for key in dict_list[0].keys(): 
        flattened_dict[key] = [] 
     
    for dictionary in dict_list: 
        for key, value in dictionary.items(): 
            flattened_dict[key].append(value) 
             
    return flattened_dict

## recommend_songs() --> executable function
def recommend_songs(song_list, spotify_data, n_songs=10): 
     
    metadata_cols = ['name', 'year', 'artists'] 
    song_dict = flatten_dict_list(song_list) 
     
    song_center = get_mean_vector(song_list, spotify_data) 
    scaler = song_cluster_pipeline.steps[0][1] 
    scaled_data = scaler.transform(spotify_data[number_cols]) 
    scaled_song_center = scaler.transform(song_center.reshape(1, -1)) 
    distances = cdist(scaled_song_center, scaled_data, 'cosine') 
    index = list(np.argsort(distances)[:, :n_songs][0]) 
     
    rec_songs = spotify_data.iloc[index] 
    rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])] 
    return rec_songs[metadata_cols].to_dict(orient='records')