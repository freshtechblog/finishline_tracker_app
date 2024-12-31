import os
import gspread
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these SCOPES, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]

class GoogleSheetManager:
    """Class to interact with a google sheet
    """
    def __init__(self, credentials_path, token_path, sheet_name):
        """Initializer

        Args:
            credentials_path (str): Path to the credential file
            token_path (str): Path to the token file
            sheet_name (str): the name of the sheet
        """
        self.credentials_path = credentials_path
        self.token_path = token_path
        self.sheet_name = sheet_name
        self.client = None
        self.sheet = None
        self.connect()

    def connect(self):
        """Connect to the google sheet
        """
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, 'w') as token:
                token.write(creds.to_json())

        self.client = gspread.authorize(creds)
        self.sheet = self.client.open(self.sheet_name)

    def select_worksheet(self, worksheet_name):
        """Select the sheet to work with

        Args:
            worksheet_name (str): Name of the sheet

        Returns:
            Worksheet: The Worksheet class
        """
        return self.sheet.worksheet(worksheet_name)

    def get_cell(self, row, col, worksheet_name=None):
        """Get data from a cell

        Args:
            row (int): The row of the data
            col (int): The column of the data
            worksheet_name (str, optional): The name of the worksheet. Defaults to None.

        Returns:
            Any: The data in the cell
        """
        worksheet = self.select_worksheet(worksheet_name) if worksheet_name else self.sheet.get_worksheet(0)
        return worksheet.cell(row, col).value

    def update_cell(self, row, col, value, worksheet_name=None):
        """Update the data in a cell

        Args:
            row (int): The row of the cell
            col (int): The column of the cell
            value (Any): The value to insert
            worksheet_name (str, optional): The name of the worksheet. Defaults to None.
        """
        worksheet = self.select_worksheet(worksheet_name) if worksheet_name else self.sheet.get_worksheet(0)
        worksheet.update_cell(row, col, value)

    def get_all_values(self, worksheet_name=None):
        """Get all the values of a worksheet

        Args:
            worksheet_name (str, optional): The name of the worksheet. Defaults to None.

        Returns:
            GridRangeType: All of the values in the sheet
        """
        worksheet = self.select_worksheet(worksheet_name) if worksheet_name else self.sheet.get_worksheet(0)
        return worksheet.get_all_values()

    def add_row(self, row_data, worksheet_name=None):
        """Add a row to the data

        Args:
            row_data (Sequence): The data to add
            worksheet_name (str, optional): The name of the worksheet. Defaults to None.
        """
        worksheet = self.select_worksheet(worksheet_name) if worksheet_name else self.sheet.get_worksheet(0)
        worksheet.append_row(row_data)

    def get_range(self, cell_range, worksheet_name=None):
        """Get the data in a range

        Args:
            cell_range (str): The range to get in the format "M#:N#"
            worksheet_name (str, optional): The name of the worksheet. Defaults to None.

        Returns:
            GridRangeType: The data in the range
        """
        worksheet = self.select_worksheet(worksheet_name) if worksheet_name else self.sheet.get_worksheet(0)
        return worksheet.get(cell_range)

    def set_range(self, cell_range, values, worksheet_name=None):
        """Set the values in a range

        Args:
            cell_range (str): The range to get in the format "M#:N#"
            values (Iterable[Iterable[Any]]): The values to set
            worksheet_name (str, optional): The name of the worksheet. Defaults to None.
        """
        worksheet = self.select_worksheet(worksheet_name) if worksheet_name else self.sheet.get_worksheet(0)
        worksheet.update(cell_range, values)

# Usage example
if __name__ == "__main__":
    manager = GoogleSheetManager(
        'creds.json',
        'token.json',
        'Racer Brackets & Results Feb 2025')
    print(manager.set_range('D2:D5',[['1'],['3'],['4'],['2']],'Current Race'))
