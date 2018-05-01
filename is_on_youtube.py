from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import consts
import logging


class NoResultsException(Exception):
    pass


def check_if_driver_page_is_no_internet_connection(driver):
    """
    Check if the current chrome page contains the header "There is no Internet connection"
    :param driver:
    :return:
    """
    try:
        if driver.Chrome.find_element_by_class_name("error-code").text == "ERR_INTERNET_DISCONNECTED":
            first_header = True
        else:
            first_header = False

    except NoSuchElementException:
        first_header = False

    finally:

        return first_header


class CheckIfSongIsOnYoutube(object):

    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_song_data_by_name(self, song_name):

        try:

            self.driver.get(consts.YOUTUBE_PATH)
            # Make sure YouTube was loaded successfully, will raise ElementNotFound if not
            self.driver.find_element_by_id(consts.YOUTUBE_ICON_LOGO_ID)

            self._search_song_on_youtube(song_name)

            video_name_in_youtube, video_duration = self._parse_song_results()

            return {
                "name": video_name_in_youtube,
                "duration": video_duration
            }

        except NoResultsException:
            logging.error("Could not find results for %s", song_name)
            raise

        except NoSuchElementException:
            logging.exception("Failed get_song_data_by_name(%s)", song_name)
            raise
        except TimeoutException:
            logging.exception("Couldn't click on searched song name")
            raise

        finally:
            # TODO(Dror): Check if the driver has been opened
            self.driver.quit()

    def _search_song_on_youtube(self, song):
        """
        this functions returns selenium's NoSuchElementException, the trigger is that the WebDriver couldn't find
        the HTML element to click on. 
        :return: NoSuchElementException
        """
        search_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, consts.SEARCH_BOX_ID)
            )
        )
        search_box.send_keys(song)
        # TODO(Dror): Remove the sleeps
        sleep(3)
        WebDriverWait(self.driver, 5, 0.1).until(
            EC.presence_of_element_located(
                (By.ID, consts.SEARCH_BUTTON_ID)
            )
        ).click()

    def _parse_song_results(self):
        self.driver.refresh()
        sleep(3)
        # TODO(Dror): Remove this
        try:
            sleep(3)
            video_duration = WebDriverWait(self.driver, 5, 0.1).until(
                EC.presence_of_element_located(
                    (By.XPATH, consts.FIRST_VIDEO_RESULT_DURATION)
                )
            ).text

        except TimeoutException:
            no_results = WebDriverWait(self.driver, 5, 0.1).until(
                EC.presence_of_element_located(
                    (By.XPATH, consts.NO_RESULTS_XPATH)
                )
            ).text

            if no_results == "No results found":
                raise NoResultsException()

        try:
            self.driver.refresh()
            sleep(3)
            self.driver.find_element_by_tag_name(consts.SONG_TITLE_TAG_NAME).click()
            # WebDriverWait(self.driver, 10, 2).until(
            #     EC.element_to_be_clickable(
            #         (By.TAG_NAME, consts.SONG_TITLE_TAG_NAME)
            #     )
            # ).click()
        except TimeoutException:

            raise TimeoutException

        video_name_in_youtube = WebDriverWait(self.driver, 10, 0.1).until(
            EC.presence_of_element_located(
                (By.XPATH, consts.VIDEO_NAME_IN_YOUTUBE_XPATH)
            )
        ).text

        return video_name_in_youtube, video_duration
