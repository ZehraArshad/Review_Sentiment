import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

def save_to_sheet(df: pd.DataFrame, sheet_name: str, worksheet_name: str = "Sheet1"):
    sheet = client.open(sheet_name)
    worksheet = sheet.worksheet(worksheet_name)

    worksheet.clear()

    header = list(df.columns)
    values = df.values.tolist()

    worksheet.append_row(header)
    worksheet.append_rows(values)
