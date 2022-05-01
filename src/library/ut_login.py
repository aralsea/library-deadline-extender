import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def login_UT_account(driver: webdriver.Chrome) -> None:
    time.sleep(3)
    ut_id = os.environ.get("UT_USER_NAME")
    ut_password = os.environ.get("UT_PASSWORD")

    ut_id_form = driver.find_element(by=By.XPATH, value="//*[@id='userNameInput']")
    ut_password_form = driver.find_element(
        by=By.XPATH, value="//*[@id='passwordInput']"
    )
    ut_submit_button = driver.find_element(by=By.XPATH, value="//*[@id='submitButton']")

    ut_id_form.send_keys(ut_id)
    ut_password_form.send_keys(ut_password)
    ut_submit_button.click()

    print(driver.current_url)
    return
