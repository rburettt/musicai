from sentiment_analysis_acoustic_properties import sentiment_analysis_acoustic
from lyrics_classification import sentiment_analysis_song_lyrics, fetch_info
from flask import Flask, render_template, flash, request
from generate_image import image_generator

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        song_name = request.form['song_name']
        song_artist = request.form['song_artist']
        print(song_name)
        print(song_artist)

        if not song_name:
            flash('Title is required!')
        elif not song_artist:
            flash('Content is required!')

        if song_name and song_artist:
            acoustic = sentiment_analysis_acoustic(song_name, song_artist)
            lyrics = sentiment_analysis_song_lyrics(song_name, song_artist)
            infos = fetch_info(song_name, song_artist)
            if acoustic and lyrics:
                related_images = image_generator(acoustic[0], lyrics[0])
        return render_template('index.html', acoustic_analysis=acoustic[0], lyrics_analysis=lyrics[0], most_common_word=lyrics[1], infos=infos, related_image_1=related_images[0], related_image_2=related_images[1] )
    else:
        return render_template('index.html')


app.run()