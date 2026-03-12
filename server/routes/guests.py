from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from sheets_utils import get_guest_data
import os

router = APIRouter()

ADULT_PRICE = 500
CHILD_PRICE = 299

@router.get("/")
async def get_guest_stats():
    """
    Fetches data from Google Sheets and returns aggregated statistics.
    Expects columns: "Guest Name", "Number of Adults attending", "Number of Children attending"
    """
    try:
        records = get_guest_data()
        
        total_adults = 0
        total_children = 0
        guest_list = []
        
        for record in records:
            # Match actual Google Sheet column names from screenshot
            name = record.get("Name") or "Guest"
            adults_raw = record.get("Number of Adults") or record.get("Number of Adults attending") or record.get("adultCount") or 0
            children_raw = record.get("Number of Children") or record.get("Number of Children attending") or record.get("childCount") or 0
            
            curr_adults = 0
            curr_children = 0
            
            try:
                curr_adults = int(adults_raw) if str(adults_raw).strip() else 0
                total_adults += curr_adults
            except (ValueError, TypeError):
                pass
                
            try:
                curr_children = int(children_raw) if str(children_raw).strip() else 0
                total_children += curr_children
            except (ValueError, TypeError):
                pass
            
            guest_list.append({
                "name": name,
                "adults": curr_adults,
                "children": curr_children
            })
            
        adult_expenditure = total_adults * ADULT_PRICE
        child_expenditure = total_children * CHILD_PRICE
        total_expenditure = adult_expenditure + child_expenditure
        
        return {
            "totalAdults": total_adults,
            "totalChildren": total_children,
            "totalGuests": total_adults + total_children,
            "totalExpenditure": total_expenditure,
            "adultExpenditure": adult_expenditure,
            "childExpenditure": child_expenditure,
            "guests": guest_list
        }
    except Exception as e:
        print(f"Error fetching sheets data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
