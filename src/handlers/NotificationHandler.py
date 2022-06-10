import os
from datetime import datetime, timedelta, timezone
from typing import List

from data_structure.lending import Lending
from slack_sdk.webhook import WebhookClient

JST = timezone(timedelta(hours=+9), "JST")


class NotificationHandler:
    def __init__(self) -> None:
        if os.environ.get("SLACK_WEBHOOK_URL"):
            self.webhook = WebhookClient(url=os.environ["SLACK_WEBHOOK_URL"])
        else:
            raise Exception("SLACK_WEBHOOK_URL is not set.")

    def post_current_lendings(self, lendings: List[Lending]) -> None:
        if not lendings:
            response = self.webhook.send(
                text=(
                    f"{datetime.now(JST).strftime('%Y年%m月%d日 %H:%M:%S')}更新"
                    "\n図書を借りていません"
                ),
            )
            print(f"status: {response.status_code} body: {response.body}")
            print("There is no updated lendings.")
            print()
            return
        attachments = []
        for lending in lendings:
            book_title = {"title": f"{lending.book_name}"}
            due_date = {"value": f"返却期限：{lending.due_date}"}
            checkout_date = {"value": f"貸出日：{lending.checkout_date}"}
            is_reserved = {"value": ("予約あり" if lending.is_reserved else "予約なし")}
            library = {"value": f"{lending.library.library_name}"}
            extend_counter = {"value": f"延長回数：{lending.extend_counter}回"}

            lending_dict = {
                "color": "#AAFFAA",
                "fields": [
                    book_title,
                    due_date,
                    library,
                    is_reserved,
                    extend_counter,
                    checkout_date,
                ],
            }

            attachments.append(lending_dict)

        response = self.webhook.send(
            text=f"{datetime.now(JST).strftime('%Y年%m月%d日 %H:%M:%S')}",
            attachments=attachments,
        )
        print(f"status: {response.status_code} body: {response.body}")
        print()

    def post_updated_lendings(self, updated_lendings: List[Lending]) -> None:
        if not updated_lendings:
            response = self.webhook.send(
                text=(
                    f"{datetime.now(JST).strftime('%Y年%m月%d日 %H:%M:%S')}更新"
                    "\n図書の延長はありませんでした．"
                ),
            )
            print(f"status: {response.status_code} body: {response.body}")
            print("There is no updated lendings.")
            print()
            return

        attachments = []
        for lending in updated_lendings:
            book_title = {"title": f"{lending.book_name}"}
            due_date = {"value": f"延長後の返却期限：{lending.due_date}"}
            library = {"value": f"{lending.library.library_name}"}

            lending_dict = {
                "color": "#36C5F0",
                "fields": [
                    book_title,
                    due_date,
                    library,
                ],
            }

            attachments.append(lending_dict)

        response = self.webhook.send(
            text=(
                f"{datetime.now(JST).strftime('%Y年%m月%d日 %H:%M:%S')}更新"
                "\n以下の図書の期限を延長しました"
            ),
            attachments=attachments,
        )
        print(f"status: {response.status_code} body: {response.body}")
        print()
