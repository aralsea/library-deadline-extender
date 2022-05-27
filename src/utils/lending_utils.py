import re
from datetime import datetime
from typing import List

from constants.library import Library
from data_structure.lending import Lending


def load_lending_from_list(data_list: List[str], is_extendable: bool) -> Lending:
    book_ID = int(data_list[2])
    checkout_date = datetime.strptime(data_list[3], "%Y.%m.%d").date()
    extend_counter = int(re.sub(r"\D", "", data_list[4]))
    due_date = datetime.strptime(data_list[5], "%Y.%m.%d").date()
    is_reserved = 0 < int(re.sub(r"\D", "", data_list[6]))
    book_name = data_list[8]
    if "駒場" in data_list[9]:
        library = Library.Komaba
    elif "数理" in data_list[9]:
        library = Library.MS
    else:
        library = Library.MS

    lending = Lending(
        book_ID=book_ID,
        book_name=book_name,
        checkout_date=checkout_date,
        due_date=due_date,
        is_reserved=is_reserved,
        library=library,
        extend_counter=extend_counter,
        is_extendable=is_extendable,
    )
    return lending
