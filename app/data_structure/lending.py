from datetime import date

from constants.library import Library


class Lending:
    def __init__(
        self,
        book_ID: int,
        book_name: str,
        checkout_date: date,
        due_date: date,
        is_reserved: bool,
        library: Library,
        extend_counter: int,
        is_extendable: bool,
    ):
        self.lending_ID = f"{checkout_date}/{book_ID}"
        self.book_ID = book_ID
        self.book_name = book_name
        self.checkout_date = checkout_date
        self.due_date = due_date
        self.is_reserved = is_reserved
        self.library = library
        self.extend_counter = extend_counter
        self.is_extendable = is_extendable

    def can_be_extendable(self) -> bool:
        return (
            (date.today() <= self.due_date)
            and (not self.is_reserved)
            and (self.extend_counter < self.library.extend_limit)
        )
