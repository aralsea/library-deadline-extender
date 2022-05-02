from enum import Enum


class Library(Enum):
    Komaba = ("Komaba", 2, "駒場図書館")
    MS = ("MS", 2, "数理図書館")

    def __init__(self, id, extend_limit, library_name):
        self.id = id
        self.extend_limit = extend_limit
        self.library_name = library_name
