from is_on_youtube import CheckIfSongIsOnYoutube


class TestSearchingSongInYouTube(object):
    chrome_tab = CheckIfSongIsOnYoutube()

    def test_enter_youtube_url(self):
        assert "Successfully entered youtube" in self.chrome_tab._open_youtube()

    def test_search_song_in_youtube(self):
        assert self.chrome_tab._search_song("One") == "managed to search a song"

    def test_receive_song_duration_and_name(self):
        results = self.chrome_tab._look_for_results()
        assert "Duration" in results.
        assert "Song Name" in results

    def test_tear_down(self):
        self.chrome_tab.driver.close()
