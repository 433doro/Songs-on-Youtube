import is_on_youtube_as_WEB_API
from webtest import TestApp


def test_collect_song_data_using_WEB_API():

    youtube_songs_information_collection_app = TestApp(is_on_youtube_as_WEB_API.app)
    response_object = youtube_songs_information_collection_app.get('/song/river/')

    assert response_object.status_code == 200, "First test succeeded"




if __name__ == '__main__':

    test_collect_song_data_using_WEB_API()

