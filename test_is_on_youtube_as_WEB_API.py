import is_on_youtube_as_WEB_API
from webtest import TestApp


if __name__ == '__main__':

    youtube_songs_information_collection_app = TestApp(is_on_youtube_as_WEB_API.app)
    response_object = youtube_songs_information_collection_app.get('/song/river/')

    assert response_object.status_code == 200


