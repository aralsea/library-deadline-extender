import platform
import sys
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


def download_lengding_datum(driver):
    if (
        driver.current_url
        != "https://opac.dl.itc.u-tokyo.ac.jp/opac/odr_stat/?lang=0"
    ):
        return
    # 貸し出しデータを出力
    file_output_entry = driver.find_element(
        by=By.XPATH, value="//*[@id='srv_odr_stat_re']/div[2]/div[1]/span/a[2]"
    )
    # クリック前のハンドルリスト
    handles_befor = driver.window_handles

    # (リンク)要素を新しいタブで開く
    actions = ActionChains(driver)

    if platform.system() == "Darwin":
        # Macなのでコマンドキー
        actions.key_down(Keys.COMMAND)
    else:
        # Mac以外なのでコントロールキー
        actions.key_down(Keys.CONTROL)

    actions.click(file_output_entry)
    actions.perform()

    # 新しいタブが開ききるまで最大30秒待機
    try:
        WebDriverWait(driver, 30).until(
            lambda a: len(a.window_handles) > len(handles_befor)
        )
    except TimeoutException:
        print("TimeoutException: 新規ウィンドウが開かずタイムアウトしました")
        sys.exit(1)

    # クリック後のハンドルリスト
    handles_after = driver.window_handles

    # ハンドルリストの差分
    handle_new = list(set(handles_after) - set(handles_befor))

    # 新しいタブに移動
    driver.switch_to.window(handle_new[0])

    select_element = driver.find_element(By.ID, "charset")
    select_object = Select(select_element)
    select_object.select_by_visible_text("UTF-8")

    file_output_button = driver.find_element(
        by=By.XPATH, value="//*[@id='opac_fileout']/form/p/input[1]"
    )
    file_output_button.click()

    time.sleep(3)
    file_download_button = driver.find_element(
        by=By.XPATH, value="//*[@id='opac_fileout']/form/p[2]/a"
    )
    file_download_button.click()
