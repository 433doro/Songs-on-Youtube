import is_on_youtube_as_WEB_API
from webtest import TestApp
import logging


if __name__ == '__main__':

    logger = logging.getLogger()

    youtube_songs_information_colletion_app = TestApp(is_on_youtube_as_WEB_API.app)
    response_object = youtube_songs_information_colletion_app.get('/song/river/')

    assert response_object.status_code == 200


