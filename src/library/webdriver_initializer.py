import chromedriver_binary  # noqa
from selenium import webdriver


def init_webdriver():
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("detach", True)

    # Selenium Server に接続する
    print("connectiong to remote browser...")
    driver = webdriver.Chrome(
        options=options,
    )
    return driver
