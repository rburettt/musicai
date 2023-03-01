# musicai

This application takes a song and uses ML to analyse its lyrics and acoustic properties.
With the predicted information, it then generates two relevant images and a color palette based on the album cover.

## Demo 

![](demo.gif)

## Usage

### API requirements
In generate_image.py, add your Unsplash API key

In lyrics_classification.py, add your Genius API key

In sentiment_analysis_acoustic_properties.py, add your Spotify API informations

### Running the app

Create a virtual environement 

python3 -m venv venv

Activate it

.  venv/bin/activate

Install the requirements

python -r requirements.txt

Run the app

python app.py

Note: the first time you run the application, your web-browser will launch in order for you to login to Spotify (does not work with Safari as a default browser)

### Tweaking the ML model

You can generate your own neural network that will classify songs based on acoustic properties

To do so, use the files get-playlist-data.py (training set) and generate-ml-spotify-data-sentiment-analysis.py

The model used to analyse the lyrics is not modifiable and was taken from https://huggingface.co/j-hartmann/emotion-english-roberta-large.

### Stack

Front-end: Tailwind, color-thief

Backend: Flask

ML: Numpy, Panda, Scikit-learn, Transformers

API: Spotify (with Spotipy), Unsplash (with PyUnsplash) and Genius (with lyricsgenius)

### Inspiration
The idea for this app was inspired by[this article](https://medium.com/codex/music-mood-classification-using-neural-networks-and-spotifys-web-api-d73b391044a4)

The code for getting the initial dataset that classified Spotify songs into categories was forked [this repo](https://github.com/kvsingh/music-mood-classification)



