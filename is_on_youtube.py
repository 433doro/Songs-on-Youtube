from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException


def collect_user_input():
    song_name = input("Please enter Artist and song name:")  # type: str
    return song_name


class CheckIfSongIsOnYoutube(object):

    def __init__(self):
        self.driver = webdriver.Chrome()

    def look_for_song(self):
        song_and_artist = collect_user_input()
        self._open_youtube()
        self._search_song(song_and_artist)
        self._look_for_results()
        self.driver.close()

    def _open_youtube(self):
        self.driver.get("http://www.youtube.com")

    def _search_song(self, song):
        song_and_artist_name = song
        try:
            search_box = self.driver.find_element_by_id("search")
            search_box.send_keys(song_and_artist_name)
            search_button = self.driver.find_element_by_id("search-icon-legacy")
            search_button.click()
        except NoSuchElementException:
            no_network_error = self.driver.find_element_by_tag_name("h1").text
            if no_network_error == "There is no Internet connection":
                print("There is no Internet connection, please try again.\n")
                self.driver.close()
            raise

    def _look_for_results(self):
        try:
            video_duration = WebDriverWait(self.driver, 5, 0.1).until(
                e_c.presence_of_element_located(
                    (By.XPATH, "//span[@class='style-scope ytd-thumbnail-overlay-time-status-renderer']")
                )
            ).text

        except ElementNotVisibleException:
            no_results = WebDriverWait(self.driver, 5, 0.1).until(
                e_c.presence_of_element_located(
                    (By.CLASS_NAME, "promo-title style-scope ytd-background-promo-renderer")
                )
            ).text

            if no_results == "No results found":
                print("No results found")

        WebDriverWait(self.driver, 5, 0.1).until(
            e_c.presence_of_element_located(
                (By.XPATH, "//a[@id='video-title']")
            )
        ).click()

        sleep(3)

        video_name_in_youtube = WebDriverWait(self.driver, 10, 0.1).until(
            e_c.presence_of_element_located(
                (By.XPATH, "//yt-formatted-string[@class='style-scope ytd-video-primary-info-renderer']")
            )
        ).text
        print("Song name: {1}\nDuration: {2}".format(self, video_name_in_youtube, video_duration))


if __name__ == '__main__':
    song_and_artist = collect_user_input()
    obj = CheckIfSongIsOnYoutube()
    obj._open_youtube()
    obj._search_song(song_and_artist)
    obj._look_for_results()
    obj.driver.close()
