# Third-party libraries
from gspread import Worksheet
from gspread_formatting import batch_updater
from gspread_formatting import format_cell_range, set_data_validation_for_cell_range
from pandas import DataFrame

# Local libraries
from lytils import cprint
from lytils.google_sheets import Columns
from lytils.google_sheets.errors import (
    DataRangeColumnMismatchError,
    DataRangeRowMismatchError,
)
from lytils.google_sheets.format import HeaderFormat
from lytils.google_sheets.Range import (
    get_column_letter,
    get_column_number,
    get_data_range,
    get_header_range,
    Range,
)
from lytils.regex import match


class SpreadsheetTab:
    def __init__(self, tab: Worksheet):
        self.__tab = tab
        self.__batch = batch_updater(self.__tab.spreadsheet)

    # Get path in terms of Spreadsheet > Worksheet
    def get_path(self):
        return f"{self.__tab.spreadsheet.title} > {self.__tab.title}"

    # Clear all data
    def clear(self) -> None:
        self.__tab.clear()

    # Clear specific ranges
    def clear_ranges(self, ranges: list[str]) -> None:
        self.__tab.batch_clear(ranges=ranges)

    # ? Format single column
    # def format_column(self, header, format, header_row=1):
    #     headers = self.__tab.row_values(header_row)

    #     # +1 because Google Sheets is 1-indexed
    #     header_index = headers.index(header) + 1

    #     column_letter = get_column_letter(header_index)
    #     format_range = f"{column_letter}{header_row + 1}:{column_letter}"
    #     format_cell_range(self.__tab, format_range, format)

    # Apply formatting to columns
    def format_columns(
        self,
        columns: Columns,
        column_start: str = "A",
        row_start: int = 1,  # Row starts at 2 to account for headers
        row_end: int | None = None,
        header: bool = True,
    ):
        col_start = get_column_number(column_start)
        row_start = row_start + 1 if header else row_start
        row_end = "" if row_end is None else row_end
        formats = []
        for i, col in enumerate(columns.as_list(), start=col_start):
            column_letter = get_column_letter(i)
            formats.append(
                [
                    f"{column_letter}{row_start}:{column_letter}{row_end}",
                    col.get_format(),
                ]
            )
        self.__batch.format_cell_ranges(self.__tab, formats)

    # ? Validate single column
    # def validate_column(self, header, validation, header_row=1):
    #     headers = self.__tab.row_values(header_row)

    #     # +1 because Google Sheets is 1-indexed
    #     header_index = headers.index(header) + 1

    #     column_letter = get_column_letter(header_index)
    #     validate_range = f"{column_letter}{header_row + 1}:{column_letter}"
    #     set_data_validation_for_cell_range(self.__tab, validate_range, validation)

    # Validate multiple columns
    def validate_columns(
        self,
        columns: Columns,
        column_start: str = "A",
        row_start: int = 2,  # Row starts at 2 to account for headers
        row_end: int | None = None,
        header: bool = True,
    ):
        col_start = get_column_number(column_start)
        row_start = row_start + 1 if header else row_start
        row_end = "" if row_end is None else row_end
        validations = []
        for i, col in enumerate(columns.as_list(), start=col_start):
            column_letter = get_column_letter(i)
            validations.append(
                [
                    f"{column_letter}{row_start}:{column_letter}{row_end}",
                    col.get_validation(),
                ]
            )
        self.__batch.set_data_validation_for_cell_ranges(self.__tab, validations)

    # Set desired column widths
    def set_column_widths(self, columns: Columns, column_start: str = "A"):
        col_start = get_column_number(column_start)
        widths = []
        for i, col in enumerate(columns.as_list(), start=col_start):
            column_letter = get_column_letter(i)
            widths.append(
                [
                    f"{column_letter}",
                    col.get_width(),
                ]
            )
        self.__batch.set_column_widths(self.__tab, widths)

    # Get range as a pandas DataFrame. Assume headers.
    def get_data(self, range: str = "", header: bool = True) -> DataFrame:

        data = self.__tab.get(range) if range else self.__tab.get_values()

        if data:
            if header:
                columns = data.pop(0)  # Use the first row as headers
                df = DataFrame(data, columns=columns)
            else:
                df = DataFrame(data)

        df = df.fillna("")  # Replace None values with an empty string

        return df

    # Clear range and populate with new data. Assume headers.
    def set_data(
        self,
        data_frame: DataFrame,
        columns: Columns,
        range: str = "",
        header: bool = True,
    ) -> None:
        o_range = Range(range, header) if range else Range("A1", header)
        col_count = o_range.column_count
        row_count = o_range.row_count

        if col_count != -1 and col_count < data_frame.shape[1]:
            raise DataRangeColumnMismatchError(range, col_count, data_frame.shape[1])

        if row_count != -1 and row_count < data_frame.shape[0]:
            raise DataRangeRowMismatchError(range, row_count, data_frame.shape[0])

        # Correct column order in Data Frame
        column_order = [col.get_header() for col in columns.as_list()]
        try:
            df = data_frame[column_order]
        except KeyError as e:
            cprint(f"<r>Data Frame missing column(s)")
            raise e

        # Replace NaN with empty string, resulting in empty cells
        df = df.fillna(value="")

        headers = df.columns.tolist()
        data = df.values.tolist()

        header_range = o_range.header_range
        data_range = o_range.data_range
        first_column = o_range.first_column
        first_row = o_range.first_row
        last_row = o_range.last_row

        if header:
            # Format header
            self.__batch.format_cell_range(self.__tab, header_range, HeaderFormat())

        # * Formatting has to come BEFORE updates to format correctly
        self.format_columns(
            columns,
            column_start=first_column,
            row_start=first_row,
            row_end=last_row,
            header=header,
        )
        self.validate_columns(
            columns,
            column_start=first_column,
            row_start=first_row,
            row_end=last_row,
            header=header,
        )
        self.set_column_widths(columns, column_start=first_column)

        # Clear range
        self.clear_ranges(ranges=[o_range.range]) if range else self.clear()

        # Execute bulk request
        self.__batch.execute()

        if header:
            # Set headers
            self.__tab.update(values=[headers], range_name=header_range)

            # Freeze the header row if it's the first row
            if o_range.first_row == 1:
                self.__tab.freeze(rows=1)

        # Set data
        self.__tab.update(
            values=data,
            range_name=data_range,
            value_input_option="USER_ENTERED",
        )
