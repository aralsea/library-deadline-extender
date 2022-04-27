import datetime
from typing import List

from data_structure.lending import Lending
from slack_sdk.webhook import WebhookClient


def notifiy_lendings_list(webhook: WebhookClient, lendings: List[Lending]) -> None:

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

    response = webhook.send(
        text=f"{datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}更新",
        attachments=attachments,
    )
    print(f"status: {response.status_code} body: {response.body}")
