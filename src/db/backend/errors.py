class BookTableError(Exception):
    pass


class InvalidYearError(BookTableError):
    pass


class DuplicateIDError(BookTableError):
    pass