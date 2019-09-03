from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time


PAUSE_TIME = 2  # changing the pause_time to small values might result in signing out from your account so be "generous"


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def login(self):

        driver = self.driver
        driver.get("https://www.instagram.com/accounts/login/")
        driver.implicitly_wait(PAUSE_TIME)
        driver.maximize_window()

        driver.find_element_by_name("username").send_keys(self.username)  # insert username data
        driver.find_element_by_name("password").send_keys(self.password)  # insert password data
        driver.find_element_by_css_selector("#react-root > section > main > div > article > div > div:nth-child(1) > div > form > div:nth-child(4) > button > div").click()  # submiting the data above

        time.sleep(PAUSE_TIME)  # using implicity.wait here would restore default settings leading to logging out from the user's acoount

    def like_all_posts(self, profile_name):

        driver = self.driver
        driver.get("https://www.instagram.com/" + profile_name + "/")
        driver.implicitly_wait(PAUSE_TIME)

        # click the first image
        driver.find_element_by_css_selector("#react-root > section > main > div > div._2z6nI > article > div > div > div:nth-child(1) > div:nth-child(1) > a > div > div._9AhH0").click()

        next_post_button = driver.find_element_by_class_name("coreSpriteRightPaginationArrow")

        try:
            # while there are remaining posts
            while next_post_button:
                try:

                    time.sleep(PAUSE_TIME)
                    '''
                    Liking the posts. Leaving alone the @aria-label="Like" would result liking and 
                    the comments which we dont want. In addition, if a post is already liked we move 
                    on to next one rather than unliking it (liking it again).
                    '''
                    driver.find_element_by_xpath("//button/span[@class='glyphsSpriteHeart__outline__24__grey_9 u-__7' and @aria-label='Like']").click()

                except NoSuchElementException as exception:
                    next_post_button.click()


        except NoSuchElementException as exception:  # the reason for this try catch is that the last post will not have the next_post button so the loop would have terminated
            driver.find_element_by_xpath("//button/span[@class='glyphsSpriteHeart__outline__24__grey_9 u-__7' and @aria-label='Like']").click()
            print("All post have been liked!")

    def follow_user(self, profile_name):
        driver = self.driver
        driver.get("https://www.instagram.com/" + profile_name + "/")
        driver.implicitly_wait(PAUSE_TIME)

        try:
            not_Following = driver.find_element_by_class_name("jIbKX")  # if you haven't followed the user yet
            if not_Following:
                not_Following.click()
            else:
                pass

        except NoSuchElementException:
            print("User is already followed")


test = InstagramBot(username,password)
test.login()

