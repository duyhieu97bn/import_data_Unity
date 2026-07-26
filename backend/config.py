import os
from dotenv import load_dotenv

load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "")
SHEET1_NAME = os.getenv("SHEET1_NAME", "Sheet1")
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE", "service-account.json")
USE_LOCAL_FALLBACK = os.getenv("USE_LOCAL_FALLBACK", "true").lower() == "true"
LOCAL_EXCEL_FILE = os.getenv("LOCAL_EXCEL_FILE", "../data.xlsx")
TEMPLATE_FILE = os.getenv("TEMPLATE_FILE", "../template.xlsx")
