import time

from selenium.webdriver.common.by import By

from library.ut_login import login_UT_account


def logout_from_my_opac(driver):
    time.sleep(3)
    # MY_OPACログアウト
    logout_btn = driver.find_element(
        by=By.XPATH, value="//*[@id='header']/div[2]/div[2]/div[2]/span/button"
    )
    logout_btn.click()
    print(driver.current_url)
