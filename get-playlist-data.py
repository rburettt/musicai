import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import util
import pandas as pd
import math
import pickle

features_for_mood = ['energy', 'liveness', 'tempo', 'speechiness',
                                     'acousticness', 'instrumentalness', 'danceability', 'duration_ms',
                                     'loudness', 'valence']

def get_track_features(track_ids, spotify):
    chunk_size = 50
    num_chunks = int(math.ceil(len(track_ids) / float(chunk_size)))
    features_add = []
    for i in range(num_chunks):
        chunk_track_ids = track_ids[i * chunk_size:min((i + 1) * chunk_size, len(track_ids))]
        chunk_features = spotify.audio_features(tracks=chunk_track_ids)
        features_add.extend(chunk_features)

    features_df = pd.DataFrame(features_add).drop(['id', 'analysis_url', 'key', 'mode', 'time_signature',
                                                   'track_href', 'type', 'uri'], axis=1)
    features_df = features_df[features_for_mood]
    return features_df

# add your own Spotify API info here
token = util.prompt_for_user_token(username='username', scope='user-library-read',
                                                   client_id='3209302e-6fa8-4651-b1f9-28e8ac2c5854',
                                                   client_secret='3209302e-6fa8-4651-b1f9-28e8ac2c5854',
                                                   redirect_uri='http://localhost:5000')
spotify = spotipy.Spotify(auth=token, requests_timeout=20)

playlists = {
             'energetic' : ["https://open.spotify.com/playlist/4QDWboU5rwpDRXwYprwJf5",
                        "https://open.spotify.com/playlist/0V32mTwWBzo6rNIk21owsY",
                             ],
             'calm':    ["https://open.spotify.com/playlist/1r4hnyOWexSvylLokn2hUa",
                             "https://open.spotify.com/playlist/11IcIUefRdjIpy1K5GMdOH",],
}

tracks = pd.DataFrame()
moods = []

for mood, links in playlists.items():
    print (mood)
    for link in links:
        id = link[34:56]
        print(id)
        try:
            pl_tracks = spotify.playlist_tracks(id)['items']
            ids = [foo['track']['id'] for foo in pl_tracks]
        except:
            print (link)
            continue
        features = get_track_features(ids, spotify)
        features['id'] = ids
        features['mood'] = mood
        tracks = tracks.append(features)

tracks.to_csv('training-data-music-mood.csv')