import os
import gspread
from dotenv import load_dotenv

load_dotenv()

def get_sheets_client():
    service_account_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH")
    if not service_account_path or not os.path.exists(service_account_path):
        raise Exception(f"Google Service Account file not found at {service_account_path}")
    
    gc = gspread.service_account(filename=service_account_path)
    return gc

def get_guest_data():
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        raise Exception("GOOGLE_SHEET_ID not set in environment")
        
    client = get_sheets_client()
    sheet = client.open_by_key(sheet_id).sheet1
    
    # Get all records (including headers)
    records = sheet.get_all_records()
    return records
