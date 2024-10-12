from gspread_formatting import DataValidationRule, BooleanCondition


def CheckboxValidation() -> DataValidationRule:
    return DataValidationRule(
        BooleanCondition("BOOLEAN", ["TRUE", "FALSE"]), showCustomUi=True
    )
