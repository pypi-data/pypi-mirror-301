from lytils.regex import match


def get_column_letter(column_number) -> str:
    """
    Get column letter given column number.
    1 = A, 2 = B, ...,  27 = AA, 28 = AB, etc
    """
    dividend = column_number
    letter = ""
    while dividend > 0:
        remainder = (dividend - 1) % 26
        letter = chr(65 + remainder) + letter
        dividend = (dividend - remainder) // 26
    return letter


def get_column_number(column_letter) -> int:
    """
    Get column number given column letter.
    A = 1, B = 2, ...,  AA = 27, AB = 28, etc
    """
    number = 0
    for char in column_letter:
        number = number * 26 + (ord(char) - ord("A") + 1)
    return number


def get_first_column(range: str, as_number: bool = False) -> str | int:
    column = match(r"^[A-Za-z]+", range, group=0)
    column = column if column else "A"
    return get_column_number(column) if as_number else column.upper()


def get_last_column(range: str, as_number: bool = False) -> str | int:
    column = match(r":([A-Za-z]+)", range, group=1)
    return get_column_number(column) if as_number else column.upper()


def get_first_row(range: str) -> int:
    row = match(r"^[A-Za-z]*([0-9]+)", range, group=1)
    return int(row) if row else 1


def get_last_row(range: str) -> int | str:
    row = match(r":[A-Za-z]*([0-9]+)", range, group=1)
    return int(row) if row else ""


def get_column_count(range: str) -> int:
    first_column = get_first_column(range, as_number=True)
    last_column = get_last_column(range, as_number=True)
    return last_column - first_column + 1 if last_column else -1


def get_row_count(range: str) -> int:
    first_row = get_first_row(range)
    last_row = get_last_row(range)
    return last_row - first_row + 1 if last_row else -1


def correct_range(
    range, first_column: str, first_row: int, last_column: str, last_row: int | str
) -> str:
    correct = f"{first_column}{first_row}"
    correct += f":{last_column}{last_row}" if ":" in range else ""
    return correct


def get_header_range(range: str):
    """
    Get header range (first row) given a range in a1 notation
    """
    first_column = get_first_column(range)
    last_column = get_last_column(range)
    first_row = get_first_row(range)

    return correct_range(range, first_column, first_row, last_column, first_row)


def get_data_range(range: str, header: bool = True):
    """
    Get data range (everything except first row) given a range in a1 notation
    """
    first_column = get_first_column(range)
    last_column = get_last_column(range)
    first_row = get_first_row(range)
    last_row = get_last_row(range)

    # Increment first row by 1 if range includes a header
    first_row = int(first_row) + 1 if header else first_row

    # Increment first row by 1
    return correct_range(range, first_column, first_row, last_column, last_row)


class Range:
    def __init__(self, range: str, header: bool = False):
        self.__first_column = get_first_column(range)
        self.__last_column = get_last_column(range)
        self.__first_column_as_number = get_first_column(range, as_number=True)
        self.__last_column_as_number = get_last_column(range, as_number=True)
        self.__first_row = get_first_row(range)
        self.__last_row = get_last_row(range)
        self.__range = correct_range(
            range,
            self.__first_column,
            self.__first_row,
            self.__last_column,
            self.__last_row,
        )
        self.__column_count = get_column_count(self.__range)
        self.__row_count = get_row_count(self.__range)
        self.__header_range = get_header_range(self.__range) if header else None
        self.__data_range = get_data_range(self.__range, header)
        self.__first_data_row = get_first_row(self.__data_range)
        self.__last_data_row = get_last_row(self.__data_range)

    @property
    def range(self):
        return self.__range

    @property
    def first_column(self):
        return self.__first_column

    @property
    def last_column(self):
        return self.__last_column

    @property
    def first_column_as_number(self):
        return self.__first_column_as_number

    @property
    def last_column_as_number(self):
        return self.__last_column_as_number

    @property
    def first_row(self):
        return self.__first_row

    @property
    def last_row(self):
        return self.__last_row

    @property
    def column_count(self):
        return self.__column_count

    @property
    def row_count(self):
        return self.__row_count

    @property
    def header_range(self):
        return self.__header_range

    @property
    def data_range(self):
        return self.__data_range

    @property
    def first_data_row(self):
        return self.__first_data_row

    @property
    def last_data_row(self):
        return self.__last_data_row
