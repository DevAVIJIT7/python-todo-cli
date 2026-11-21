import gspread

SPREADSHEET_NAME = "Month wise Income/Spent"
WORKSHEET_NAME = "BudgetPlan - 2027"


def get_worksheet() -> gspread.Worksheet:
    gc = gspread.oauth()
    spreadsheet = gc.open(SPREADSHEET_NAME)

    return spreadsheet.worksheet(WORKSHEET_NAME)