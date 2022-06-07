import os

from handlers.lending_data_handler import LendingDataHandler
from handlers.NotificationHandler import NotificationHandler
from handlers.web_transition_handler import WebTransitionHandler


def test_environment_variable():
    print(os.environ.get("SLACK_WEBHOOK_URL"))


def extend_due_date():
    is_heroku = os.environ.get("PYTHONHOME") == "/app/.heroku/python"
    web_transition_handler = WebTransitionHandler(
        is_heroku=is_heroku,
        is_detached=False,
        is_headless=True,
        wait_seconds=3,
    )

    web_transition_handler.move_to_opac_top_without_login()
    web_transition_handler.login_to_opac()
    web_transition_handler.move_to_my_lending_status()
    lending_data_handler = LendingDataHandler()
    lending_data_handler.load_lending_data_from_opac(
        driver=web_transition_handler.driver
    )
    lending_data_handler.output_lending_data()

    updated_lendings = web_transition_handler.extend_due_date_of_given_lendings(
        lendings=lending_data_handler.lendings
    )

    notification_handler = NotificationHandler()
    notification_handler.post_updated_lendings(updated_lendings=updated_lendings)

    web_transition_handler.quit()


def check_current_lendings():
    is_heroku = os.environ.get("PYTHONHOME") == "/app/.heroku/python"
    web_transition_handler = WebTransitionHandler(
        is_heroku=is_heroku,
        is_detached=False,
        is_headless=True,
        wait_seconds=3,
    )

    web_transition_handler.move_to_opac_top_without_login()
    web_transition_handler.login_to_opac()
    web_transition_handler.move_to_my_lending_status()
    lending_data_handler = LendingDataHandler()
    lending_data_handler.load_lending_data_from_opac(
        driver=web_transition_handler.driver
    )
    lending_data_handler.output_lending_data()

    notification_handler = NotificationHandler()
    notification_handler.post_current_lendings(lendings=lending_data_handler.lendings)

    web_transition_handler.quit()


def run():
    extend_due_date()
    check_current_lendings()


def main(data, context):
    extend_due_date()
    check_current_lendings()


if __name__ == "__main__":
    run()
