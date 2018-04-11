from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.support.ui import WebDriverWait

import is_on_youtube_configuration


def collect_user_input():
    song = input("Please enter Artist and song name:")  # type: str
    return song


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
        self.driver.get(is_on_youtube_configuration.YOUTUBE_PATH)

    def _search_song(self, song):
        song_and_artist_name = song
        """
        this functions returns selenium's NoSuchElementException, the trigger is that the WebDriver couldn't find
        the HTML element to click on. 
        :return: NoSuchElementException
        """
        try:
            search_box = WebDriverWait(self.driver, 10).until(
                e_c.presence_of_element_located(
                    (By.ID, is_on_youtube_configuration.SEARCH_BOX_ID)
                )
            )
            search_box.send_keys(song_and_artist_name)
            sleep(3)
            search_button = WebDriverWait(self.driver, 5, 0.1).until(
                e_c.presence_of_element_located(
                    (By.ID, is_on_youtube_configuration.SEARCH_BUTTON_ID)
                )
            )
            search_button.click()

        except NoSuchElementException:
            no_network_error_textbox = self.driver.find_element_by_tag_name("h1").text
            if no_network_error_textbox == "There is no Internet connection":
                print("There is no Internet connection, please try again.\n")
                self.driver.close()
            raise

    def _look_for_results(self):

        try:
            self.driver.refresh()
            video_duration = WebDriverWait(self.driver, 5, 0.1).until(
                e_c.presence_of_element_located(
                    (By.XPATH, is_on_youtube_configuration.FIRST_VIDEO_RESULT_DURATION)
                )
            ).text

        except TimeoutException:
            no_results = WebDriverWait(self.driver, 5, 0.1).until(
                e_c.presence_of_element_located(
                    (By.XPATH, is_on_youtube_configuration.NO_RESULTS_XPATH)
                )
            ).text

            if no_results == "No results found":
                print("No results found")

        WebDriverWait(self.driver, 5, 0.1).until(
            e_c.element_to_be_clickable(
                (By.TAG_NAME, is_on_youtube_configuration.SONG_TITLE_TAG_NAME)
            )
        ).click()
        sleep(3)
        video_name_in_youtube = WebDriverWait(self.driver, 10, 0.1).until(
            e_c.presence_of_element_located(
                (By.XPATH, is_on_youtube_configuration.VIDEO_NAME_IN_YOUTUBE_XPATH)
            )
        ).text
        print("Song name: {1}\nDuration: {2}".format(self, video_name_in_youtube, video_duration))
