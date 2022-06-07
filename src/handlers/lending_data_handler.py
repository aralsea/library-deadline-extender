import time
from typing import List

from data_structure.lending import Lending
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from utils.lending_utils import load_lending_from_list


class LendingDataHandler:
    def __init__(self) -> None:
        self.lendings: List[Lending] = []

    def output_lending_data(self) -> None:
        for lending in self.lendings:
            print("--------------------------------")
            print(f"book id : {lending.book_ID}")
            print(f"book name : {lending.book_name}")
            print(f"貸出日 : {lending.checkout_date}")
            print(f"返却期限 : {lending.due_date}")
            print(f"延長回数 : {lending.extend_counter}")
            print(f"予約の有無 : {lending.is_reserved}")
            print(f"図書館 : {lending.library}")
            print(f"延長可能か : {lending.is_extendable}")
            print()

    def load_lending_data_from_opac(self, driver: webdriver.Chrome) -> None:
        assert (
            driver.current_url
            == "https://opac.dl.itc.u-tokyo.ac.jp/opac/odr_stat/?lang=0"
        ), "Current page is not my lending status page."

        time.sleep(3)
        get_screenshot = driver.get_screenshot_as_file(
            "./src/outputs/my_lending_status.png"
        )

        print(f"get screenshot : {get_screenshot}")

        self.lendings.clear()

        try:
            tableElem = driver.find_element(
                by=By.XPATH, value="//*[@id='datatables_re']"
            )
        except NoSuchElementException:
            print("You are NOT lending books.")
            return

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
            print(line + "\r\n")

            is_extendable = True
            click_dropdown = tds[0]
            click_dropdown.click()

            try:
                tds[0].find_element(by=By.TAG_NAME, value="input")
            except NoSuchElementException:
                is_extendable = False

            click_dropdown.click()

            self.lendings.append(
                load_lending_from_list(
                    data_list=lending_data, is_extendable=is_extendable
                )
            )
