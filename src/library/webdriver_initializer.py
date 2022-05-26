import os

from selenium import webdriver

is_heroku = os.environ.get("PYTHONHOME") == "/app/.heroku/python"
if not is_heroku:
    import chromedriver_binary  # noqa


def init_webdriver():
    driver_path = "/app/.chromedriver/bin/chromedriver"
    options = webdriver.ChromeOptions()
    # options.add_argument("--disable-gpu")
    # options.add_argument("--disable-extensions")
    # options.add_argument('--proxy-server="direct://"')
    # options.add_argument("--proxy-bypass-list=*")
    # options.add_argument("--start-maximized")
    options.add_argument("--headless")
    # options.add_argument("--window-size=1920,1080")

    # options.add_experimental_option("detach", True)

    # Selenium Server に接続する
    print("connectiong to remote browser...")
    if is_heroku:
        driver = webdriver.Chrome(
            executable_path=driver_path,
            options=options,
        )
    else:
        driver = webdriver.Chrome(options=options)
    return driver
