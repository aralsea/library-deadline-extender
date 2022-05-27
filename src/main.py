import os

from slack_sdk.webhook import WebhookClient

from library.auto_extender import extend_due_date
from library.handlers.lending_data_handler import LendingDataHandler
from library.handlers.web_transition_handler import WebTransitionHandler
from library.lending_data_loader import load_lending_data
from library.my_opac_login import move_to_my_opac_stats
from library.my_opac_logout import logout_from_my_opac
from library.notification_sender import notifiy_lendings_list
from library.webdriver_initializer import init_webdriver


def run():
    driver = init_webdriver()
    webhook = WebhookClient(os.environ.get("SLACK_WEBHOOK_URL"))

    move_to_my_opac_stats(driver=driver)
    lendings = load_lending_data(driver=driver)
    for lending in lendings:
        print("--------------------------------")
        print(lending.book_ID)
        print(lending.book_name)
        print(lending.checkout_date)
        print(lending.due_date)
        print(lending.extend_counter)
        print(lending.is_reserved)
        print(lending.library)
        print(lending.lending_ID)
        print(lending.is_extendable)

    extend_due_date(driver=driver, lendings=lendings)

    notifiy_lendings_list(webhook=webhook, lendings=lendings)

    logout_from_my_opac(driver=driver)
    driver.close()
    driver.quit()


def test_environment_variable():
    print(os.environ.get("SLACK_WEBHOOK_URL"))


def test_handlers():
    is_heroku = os.environ.get("PYTHONHOME") == "/app/.heroku/python"
    web_transition_handler = WebTransitionHandler(
        is_heroku=is_heroku,
        is_detached=False,
        is_headless=True,
        wait_seconds=3,
    )

    web_transition_handler.move_to_opac_top_without_login()
    web_transition_handler.move_to_opac_top_with_login()
    web_transition_handler.move_to_my_lending_status()

    lending_data_handler = LendingDataHandler()
    lending_data_handler.load_lending_data_from_opac(web_transition_handler.driver)
    lending_data_handler.output_lending_data()


if __name__ == "__main__":
    test_handlers()
