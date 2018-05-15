from time import sleep
from flask import Flask, jsonify, abort
from is_on_youtube import CheckIfSongIsOnYoutube
import logging
app = Flask(__name__)


@app.route('/song/<song_name>/', methods=['GET'])
def search_song_on_youtube(song_name):
    try:
        song_finder = CheckIfSongIsOnYoutube()
        results = song_finder.get_song_data_by_name(song_name)
        sleep(5)
        return jsonify(results)

    except:
        logging.exception("Something went wrong...")
        return abort(500)
