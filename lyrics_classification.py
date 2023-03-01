from transformers import pipeline
from collections import Counter
import string
import lyricsgenius
import re

stop_words_en = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


def fetch_song(title, artist):
    # add your genius api key here
    token = "3209302e-6fa8-4651-b1f9-28e8ac2c5854"
    genius = lyricsgenius.Genius(token)
    genius.remove_section_headers = True
    genius.verbose = False
    song = genius.search_song(title=title, artist=artist, get_full_info=True)

    if song:
        if "instrumental" in song.lyrics.lower():
            is_instrumental = True
        else:
            is_instrumental = False
    else:
        return

    # first line  removed due to parsing
    lyrics = ''.join(song.lyrics.splitlines(keepends=True)[1:])

    # lyrics are cropped because the ML model cannot process strings greater than 512 in length
    # full length lyrics is still kept for accurate word occurence analysis

    if len(lyrics) > 512:
        lyrics_cropped = (song.lyrics[:512] + '..') if len(song.lyrics) > 512 else song.lyrics
    else:
        lyrics_cropped = lyrics


    return {
  "artist": song.artist,
  "title":  song.full_title,
  "lyrics_cropped": lyrics_cropped,
   "lyrics": lyrics ,
   "is_instrumental": is_instrumental,
  "art_url": song.song_art_image_url
}


def consecutive_letters(str1):
    for el in str1:
        if el*2 in str1:
            return True
    return False

def sentiment_analysis_lyrics(lyrics, lyrics_cropped):
    split_it = [word.lower() for word in lyrics.split()]
    split_it_clean = list()
    for word in split_it:
        if word not in stop_words_en and "’" not in word and "'" not in word and not re.search('\d+', word) and not consecutive_letters(word):
            split_it_clean.append(word.replace(",", "").replace(".", "").replace("?", "").replace("!", "").replace("(", "").replace(")", ""))
    
    
    counter = Counter(split_it_clean)
    most_common_words = counter.most_common(6)
    sentence = ""  
    for word in most_common_words:
        for i in range(0, word[1]): 
            sentence += word[0] + " "   

    specific_model = pipeline(model="j-hartmann/emotion-english-roberta-large")
    data = [sentence, lyrics_cropped]
    result = specific_model(data)

    detected_emotion_highest_acc = result[0]["label"]
    if result[1]["score"] > result[0]["score"]:
        detected_emotion_highest_acc = result[1]["label"]

    return (detected_emotion_highest_acc, most_common_words[0][0])




def sentiment_analysis_song_lyrics(title, artist):
    song = fetch_song(title, artist)
    if song:
        if not song["is_instrumental"]:
            return sentiment_analysis_lyrics(song["lyrics"], song["lyrics_cropped"] )
    else:
        return


def fetch_info(title, artist):
    song = fetch_song(title, artist)
    if song:
        return {"title": song["title"], "artist": song["artist"], "is_instrumental": song["is_instrumental"], "art_url": song["art_url"],}
    else:
        return






