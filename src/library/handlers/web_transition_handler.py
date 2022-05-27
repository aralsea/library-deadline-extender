import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

is_heroku = os.environ.get("PYTHONHOME") == "/app/.heroku/python"
if not is_heroku:
    import chromedriver_binary  # noqa


class WebTransitionHandler:
    def __init__(
        self,
        is_heroku: bool,
        is_detached: bool,
        is_headless: bool,
        wait_seconds: int,
    ) -> None:
        self.wait_seconds = wait_seconds

        # webdriverを設定
        driver_path = "/app/.chromedriver/bin/chromedriver"

        options = webdriver.ChromeOptions()
        if is_headless or is_heroku:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920, 1080")

        if is_detached and not is_heroku:
            options.add_experimental_option("detach", True)

        # Selenium Server に接続する
        print("connectiong to remote browser...")
        if is_heroku:
            self.driver = webdriver.Chrome(
                executable_path=driver_path,
                options=options,
            )
        else:
            self.driver = webdriver.Chrome(options=options)

        self.driver.implicitly_wait(self.wait_seconds)
        self.ut_id = os.environ.get("UT_USER_NAME")
        self.ut_password = os.environ.get("UT_PASSWORD")

    def move_to_opac_top_without_login(self) -> None:
        # to do:もしログインしていたらログアウトする処理

        time.sleep(self.wait_seconds)

        self.driver.get("https://opac.dl.itc.u-tokyo.ac.jp/opac/opac_search/")

        time.sleep(self.wait_seconds)
        assert (
            self.driver.current_url
            == "https://opac.dl.itc.u-tokyo.ac.jp/opac/opac_search/"
        ), "Can't move to the top page of opac."
        print("Moved to the top page of opac without login.")
        print(f"current url = {self.driver.current_url}")
        print()

    def move_to_opac_top_with_login(self) -> None:
        time.sleep(self.wait_seconds)
        assert (
            self.driver.current_url
            == "https://opac.dl.itc.u-tokyo.ac.jp/opac/opac_search/"
        ), "Current page is not the top page of opac."

        login_button = self.driver.find_element(
            by=By.XPATH, value="//button[@id='btn-login']"
        )

        login_button.click()
        chose_ut_button = self.driver.find_element(
            by=By.XPATH, value="//*[@id='login1']/dl/div[1]/dt/a"
        )
        chose_ut_button.click()
        time.sleep(3)
        print(f"current url = {self.driver.current_url}")
        print()
        self.login_by_UT_account()
        assert (
            self.driver.current_url
            == "https://opac.dl.itc.u-tokyo.ac.jp/opac/opac_search/"
        ), "Current page is not opac top page."

        # ログアウトボタンがないならログインできていない．
        assert bool(
            self.driver.find_element(
                by=By.XPATH, value="//*[@id='header']/div[2]/div[2]/div[2]/span/button"
            )
        ), "Faild to move to the top page of opac with login."

        print("Login succeeded!")
        print(f"current url = {self.driver.current_url}")
        print()

    def move_to_my_lending_status(self) -> None:
        assert (
            self.driver.current_url
            == "https://opac.dl.itc.u-tokyo.ac.jp/opac/opac_search/"
        ), "Current page is not opac top page."

        # ログアウトボタンがないならログインできていない．
        assert bool(
            self.driver.find_element(
                by=By.XPATH, value="//*[@id='header']/div[2]/div[2]/div[2]/span/button"
            )
        ), "You have not logged in yet."

        my_opac_button = self.driver.find_element(
            by=By.XPATH, value="//*[@id='us_service']"
        )
        my_opac_button.click()
        time.sleep(3)
        my_lending_status_button = self.driver.find_element(
            by=By.XPATH,
            value="//*[@id='us_service-menu']/li/div/div/ul[1]/li[1]/a",
        )
        my_lending_status_button.click()
        time.sleep(3)

        assert (
            self.driver.current_url
            == "https://opac.dl.itc.u-tokyo.ac.jp/opac/odr_stat/?lang=0"
        ), "Can't move to my lending status page."

        print("Moved to my lending page.")
        print(f"cuurent url = {self.driver.current_url}")
        print()

    def login_by_UT_account(self) -> None:
        ut_id_form = self.driver.find_element(
            by=By.XPATH, value="//*[@id='userNameInput']"
        )

        ut_password_form = self.driver.find_element(
            by=By.XPATH, value="//*[@id='passwordInput']"
        )
        ut_submit_button = self.driver.find_element(
            by=By.XPATH, value="//*[@id='submitButton']"
        )

        ut_id_form.send_keys(self.ut_id)
        ut_password_form.send_keys(self.ut_password)
        time.sleep(3)
        ut_submit_button.click()
        time.sleep(3)
        assert (
            self.driver.current_url
            == "https://opac.dl.itc.u-tokyo.ac.jp/opac/opac_search/"
        ), "current page is not opac top page."
        print("Passed UT account authentification.")
