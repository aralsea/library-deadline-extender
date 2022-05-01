#import chromedriver_binary  # noqa
from selenium import webdriver


def init_webdriver():
    driver_path = '/app/.chromedriver/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu');
    options.add_argument('--disable-extensions');
    options.add_argument('--proxy-server="direct://"');
    options.add_argument('--proxy-bypass-list=*');
    options.add_argument('--start-maximized');
    options.add_argument('--headless');
    # options.add_experimental_option("detach", True)

    # Selenium Server に接続する
    print("connectiong to remote browser...")
    driver = webdriver.Chrome(
        executable_path=driver_path,
        options=options,
    )
    return driver
