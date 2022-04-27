from datetime import date, timedelta
from typing import List

from data_structure.lending import Lending
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from library.lending_data_loader import load_lending_from_list


def fill_select_checkbox(driver: webdriver.Chrome, lending: Lending):
    if driver.current_url != "https://opac.dl.itc.u-tokyo.ac.jp/opac/odr_stat/?lang=0":
        return

    target_checkout_date = lending.checkout_date
    target_book_ID = lending.book_ID

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
        candidate = load_lending_from_list(lending_data, is_extendable)
        if (
            candidate.book_ID == target_book_ID
            and candidate.checkout_date == target_checkout_date
        ):
            checkbox = tds[0].find_element(by=By.TAG_NAME, value="input")
            checkbox.click()
            close_dropdown = tds[0]
            close_dropdown.click()
            break


def extend_due_date(driver: webdriver.Chrome, lendings: List[Lending]):
    check_count = 0
    for lending in lendings:
        # 期限の前の日で，かつ延長可能ならば延長のチェックボックスを埋める
        print(f"remaining_days = {lending.due_date - date.today()}")
        if lending.is_extendable and lending.due_date - date.today() <= timedelta(
            days=1
        ):
            fill_select_checkbox(driver, lending)
            check_count += 1

    if check_count:  # チェックが空でない場合，延長を実行
        extend_button = driver.find_element(
            by=By.XPATH, value="//*[@id='srv_odr_stat_re']/p[1]/input[2]"
        )
        extend_button.click()
