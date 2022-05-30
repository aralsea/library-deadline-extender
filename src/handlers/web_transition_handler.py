import os
import time
from datetime import date, timedelta
from typing import List

from data_structure.lending import Lending
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from utils.lending_utils import load_lending_from_list

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
        self.ut_id = os.environ.get("UT_USER_NAME")
        self.ut_password = os.environ.get("UT_PASSWORD")

        if not self.ut_id or not self.ut_password:
            raise Exception("Some Environment variables are missing.")

        self.wait_seconds = wait_seconds

        # webdriverを設定
        driver_path = "/app/.chromedriver/bin/chromedriver"

        options = webdriver.ChromeOptions()
        if is_headless or is_heroku:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920, 1080")
            options.add_argument("--no-sandbox")

        if is_detached and not is_heroku:
            options.add_experimental_option("detach", True)

        # Selenium Server に接続する
        print("connecting to remote browser...")
        if is_heroku:
            self.driver = webdriver.Chrome(
                executable_path=driver_path,
                options=options,
            )
        else:
            self.driver = webdriver.Chrome(options=options)

        self.driver.implicitly_wait(self.wait_seconds)

    def move_to_opac_top_without_login(self) -> None:
        # to do:もしログインしていたらログアウトする処理
        time.sleep(self.wait_seconds)
        self.driver.get("https://opac.dl.itc.u-tokyo.ac.jp/opac/opac_search/")

        time.sleep(self.wait_seconds)
        assert (
            self.driver.current_url
            == "https://opac.dl.itc.u-tokyo.ac.jp/opac/opac_search/"
        ), "Can't move to the top page of opac."

        try:
            logout_button = self.driver.find_element(
                by=By.XPATH,
                value="//*[@id='header']/div[2]/div[2]/div[2]/span/button",
            )
            logout_button.click()
            print("Logout succeeded!")
            print()
        except NoSuchElementException:
            pass
        print("Moved to the top page of opac without login.")
        print(f"current url = {self.driver.current_url}")
        print()

    def login_to_opac(self) -> None:

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
        try:
            self.driver.find_element(
                by=By.XPATH, value="//*[@id='header']/div[2]/div[2]/div[2]/span/button"
            )
        except NoSuchElementException:
            print("Faild to move to the top page of opac with login.")

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

        print("Moved to my lending status page.")
        print(f"cuurent url = {self.driver.current_url}")
        print()

    def quit(self) -> None:
        self.move_to_opac_top_without_login()
        self.driver.close()
        self.driver.quit()
        print("quit.")
        print()

    def extend_due_date_of_given_lendings(
        self, lendings: List[Lending]
    ) -> List[Lending]:
        assert (
            self.driver.current_url
            == "https://opac.dl.itc.u-tokyo.ac.jp/opac/odr_stat/?lang=0"
        ), "Current page is not my lending status page."

        updated_lendings: List[Lending] = []
        for lending in lendings:
            # 期限の前の日で，かつ延長可能ならば延長のチェックボックスを埋める
            print(lending.book_name)
            print(f"remaining_days = {lending.due_date - date.today()}")
            print()
            if lending.is_extendable and lending.due_date - date.today() <= timedelta(
                days=1
            ):
                if self.fill_checkbox_of_given_lending(lending):
                    # チェックボックスを埋めることに成功した場合
                    updated_lendings.append(lending)

        if updated_lendings:  # チェックが空でない場合，延長を実行
            extend_button = self.driver.find_element(
                by=By.XPATH, value="//*[@id='srv_odr_stat_re']/p[1]/input[2]"
            )
            extend_button.click()

        time.sleep(3)

        assert (
            self.driver.current_url
            == "https://opac.dl.itc.u-tokyo.ac.jp/opac/odr_stat/?lang=0"
        ), "Can't move to my lending status page."

        print("Moved to my lending status page.")
        print(f"cuurent url = {self.driver.current_url}")
        print()
        return updated_lendings

    def fill_checkbox_of_given_lending(self, lending: Lending) -> bool:
        assert (
            self.driver.current_url
            == "https://opac.dl.itc.u-tokyo.ac.jp/opac/odr_stat/?lang=0"
        ), "Current page is not my lending status page."

        target_checkout_date = lending.checkout_date
        target_book_ID = lending.book_ID

        tableElem = self.driver.find_element(
            by=By.XPATH, value="//*[@id='datatables_re']"
        )

        trs = tableElem.find_elements(by=By.TAG_NAME, value="tr")
        # ヘッダ行は除いて取得

        for i in range(1, len(trs)):
            tds = trs[i].find_elements(by=By.TAG_NAME, value="td")
            lending_data = []
            line = ""
            for j in range(0, len(tds)):
                lending_data.append(tds[j].text)
                if j < len(tds) - 1:
                    line += f"{tds[j].text} | "
                else:
                    line += f"{tds[j].text}"
            # print(line + "\r\n")
            is_extendable = True
            click_dropdown = tds[0]
            click_dropdown.click()

            try:
                tds[0].find_element(by=By.TAG_NAME, value="input")
            except NoSuchElementException:
                is_extendable = False

            click_dropdown.click()
            candidate = load_lending_from_list(lending_data, is_extendable)
            if (
                candidate.book_ID == target_book_ID
                and candidate.checkout_date == target_checkout_date
                and is_extendable
            ):
                checkbox = tds[0].find_element(by=By.TAG_NAME, value="input")
                checkbox.click()
                close_dropdown = tds[0]
                close_dropdown.click()
                return True

        return False

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
        ), "Current page is not opac top page."
        print("Passed UT account authentification.")
