import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, cross_val_predict
import pickle




features_for_mood = ['energy', 'liveness', 'tempo', 'speechiness',
                                     'acousticness', 'instrumentalness', 'danceability', 'duration_ms',
                                     'loudness', 'valence']


data = pd.read_csv("training-data-music-mood.csv")
hyper_opt = False

trainx, testx, trainy, testy = train_test_split(data[features_for_mood], data['mood'], test_size = 0.33,
                                                random_state = 42, stratify=data['mood'])



scaler = StandardScaler()



train_scaled = scaler.fit_transform(trainx)
nn = MLPClassifier(max_iter = 15000, alpha=1.0, hidden_layer_sizes=8)


nn.fit(train_scaled, trainy)


test_preds = nn.predict(scaler.transform(testx))

print(accuracy_score(test_preds, testy))

# saving the model 
filename = 'trained-model-spotify.sav'
pickle.dump(nn, open(filename, 'wb'))


pickle.dump(scaler, open("scaler.sav", 'wb'))
