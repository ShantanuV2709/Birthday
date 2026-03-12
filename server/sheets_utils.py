import os
import gspread
from dotenv import load_dotenv

load_dotenv()

def get_sheets_client():
    # Priority 1: JSON string from environment variable (Best for Vercel/Render)
    service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if service_account_json:
        import json
        try:
            creds_dict = json.loads(service_account_json)
            return gspread.service_account_from_dict(creds_dict)
        except Exception as e:
            print(f"Error parsing GOOGLE_SERVICE_ACCOUNT_JSON: {e}")

    # Priority 2: Physical JSON file (Local development)
    service_account_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH")
    if service_account_path and os.path.exists(service_account_path):
        return gspread.service_account(filename=service_account_path)
        
    print(f"DEBUG: Service account path searched: {service_account_path}")
    raise Exception("No Google Service Account credentials found (set GOOGLE_SERVICE_ACCOUNT_JSON or GOOGLE_SERVICE_ACCOUNT_PATH)")

def get_guest_data():
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        raise Exception("GOOGLE_SHEET_ID not set in environment")
        
    client = get_sheets_client()
    sheet = client.open_by_key(sheet_id).sheet1
    
    # Get all records (including headers)
    records = sheet.get_all_records()
    return records
