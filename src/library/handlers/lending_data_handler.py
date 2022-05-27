import re
from datetime import datetime
from typing import List

from constants.library import Library
from data_structure.lending import Lending
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


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

    def load_lending_data_from_opac(self, driver: webdriver.Chrome) -> None:
        assert (
            driver.current_url
            == "https://opac.dl.itc.u-tokyo.ac.jp/opac/odr_stat/?lang=0"
        ), "This page is not my lending status page."

        tableElem = driver.find_element(by=By.XPATH, value="//*[@id='datatables_re']")

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
                self.load_lending_from_list(lending_data, is_extendable)
            )

    def load_lending_from_list(
        self, data_list: List[str], is_extendable: bool
    ) -> Lending:
        book_ID = int(data_list[2])
        checkout_date = datetime.strptime(data_list[3], "%Y.%m.%d").date()
        extend_counter = int(re.sub(r"\D", "", data_list[4]))
        due_date = datetime.strptime(data_list[5], "%Y.%m.%d").date()
        is_reserved = 0 < int(re.sub(r"\D", "", data_list[6]))
        book_name = data_list[8]
        if "駒場" in data_list[9]:
            library = Library.Komaba
        elif "数理" in data_list[9]:
            library = Library.MS
        else:
            library = Library.MS

        lending = Lending(
            book_ID=book_ID,
            book_name=book_name,
            checkout_date=checkout_date,
            due_date=due_date,
            is_reserved=is_reserved,
            library=library,
            extend_counter=extend_counter,
            is_extendable=is_extendable,
        )
        return lending
