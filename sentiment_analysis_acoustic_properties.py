import pandas as pd
import spotipy
from sklearn.preprocessing import StandardScaler
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util
import math
import pickle

# load the model from disk
pretrained_model = pickle.load(open("trained-model-spotify.sav", 'rb'))
scaler = pickle.load(open("scaler.sav", 'rb'))

# add your own Spotify API info here
token = util.prompt_for_user_token(username='username', scope='user-library-read',
                                                   client_id='3209302e-6fa8-4651-b1f9-28e8ac2c5854',
                                                   client_secret='3209302e-6fa8-4651-b1f9-28e8ac2c5854',
                                                   redirect_uri='http://localhost:5000')

spotify = spotipy.Spotify(auth=token, requests_timeout=20)

def get_track_features(track_id, spotify):

    features_for_mood = ['energy', 'liveness', 'tempo', 'speechiness', 'acousticness', 'instrumentalness', 'danceability', 'duration_ms', 'loudness', 'valence']
    features_add = []
    track_features = spotify.audio_features(tracks=track_id)
    features_add.extend(track_features)

    features_df = pd.DataFrame(features_add).drop(['id', 'analysis_url', 'key', 'mode', 'time_signature',
                                                   'track_href', 'type', 'uri'], axis=1)
    features_df = features_df[features_for_mood]


    return scaler.transform(features_df)

def sentiment_analysis_acoustic(track, artist):
    try:
        track_id = spotify.search(q='artist:' + artist + ' track:' + track, type='track')['tracks']['items'][0]['id']
    except:
        return
    song_data = get_track_features([track_id], spotify)
    return pretrained_model.predict(song_data)


