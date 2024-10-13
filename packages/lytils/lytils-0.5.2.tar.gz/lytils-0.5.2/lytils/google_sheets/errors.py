class DataRangeColumnMismatchError(ValueError):
    """
    Used when there is a mismatch between the range's columns and data frame's columns.
    """

    def __init__(self, range, col_count, df_col_count):
        message = (
            f'Specified range "{range}" has fewer columns than provided data frame '
            f"({col_count} < {df_col_count})"
        )
        super().__init__(message)


class DataRangeRowMismatchError(ValueError):
    """
    Used when there is a mismatch between the range's rows and data frame's rows.
    """

    def __init__(self, range, row_count, df_row_count):
        message = (
            f'Specified range "{range}" has fewer rows than provided data frame '
            f"({row_count} < {df_row_count})"
        )
        super().__init__(message)
