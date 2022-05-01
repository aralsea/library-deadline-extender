import time

from selenium.webdriver.common.by import By

from library.ut_login import login_UT_account


def move_to_my_opac_stats(driver):
    # Selenium 経由でブラウザを操作する
    time.sleep(3)

    driver.get("https://opac.dl.itc.u-tokyo.ac.jp/opac/opac_search/")
    print(driver.current_url)

    # MY_OPACログイン
    time.sleep(3)

    login_btn = driver.find_element(by=By.XPATH, value="//button[@id='btn-login']")
    login_btn.click()
    print(driver.current_url)

    # UTアカウントでログイン
    time.sleep(3)

    chose_ut_btn = driver.find_element(
        by=By.XPATH, value="//div[@class='col-md-2 login_btn']"
    )
    chose_ut_btn.click()
    print(driver.current_url)

    login_UT_account(driver)

    # My OPACサービスをクリック
    time.sleep(3)

    my_opac_buttun = driver.find_element(by=By.XPATH, value="//*[@id='us_service']")
    my_opac_buttun.click()
    time.sleep(3)
    my_opac_my_datum = driver.find_element(
        by=By.XPATH,
        value="//*[@id='us_service-menu']/li/div/div/ul[1]/li[1]/a",
    )
    my_opac_my_datum.click()
    print(driver.current_url)
