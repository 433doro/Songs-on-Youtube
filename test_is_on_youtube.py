from is_on_youtube import CheckIfSongIsOnYoutube, NoResultsException
import pytest


class TestSearchingSongInYouTube(object):
    chrome_tab = CheckIfSongIsOnYoutube()

    def test_integration_no_results(self):
        with pytest.raises(NoResultsException):
            really_bad_query = "23235235NO WAY I FUCKING EXISDT FOO BAR 123 DROR THE KING WHAT THE FUCK"
            self.chrome_tab.get_song_data_by_name(really_bad_query)

    def test_enter_youtube_url(self):
        assert "Successfully entered youtube" in self.chrome_tab._open_youtube()

    def test_search_song_in_youtube(self):
        assert self.chrome_tab._search_song_on_youtube("One") == "managed to search a song"

    def test_receive_song_duration_and_name(self):
        results_found = 0
        results = self.chrome_tab._parse_song_results()
        for element in results:  # type: tuple
            if "Song" in element:
                results_found = 1

        assert results_found == 1

    def test_tear_down(self):
        self.chrome_tab.driver.close()
