import pandas as pd
from pymongo import MongoClient
from datetime import datetime
from mongoengine import *
from datetime import datetime, date
from config import settings
import certifi

# ==========================
# MongoDB Connection
# ==========================
MONGO_URI = "mongodb+srv://admin:admin@hrms.kt85gff.mongodb.net/hrms?retryWrites=true&w=majority"  # change if using Atlas
DB_NAME = "hrms"

client = connect(
    host="mongodb+srv://admin:admin@hrms.kt85gff.mongodb.net/hrms?retryWrites=true&w=majority",
    tls=True,
    tlsCAFile=certifi.where()
)
db = client[DB_NAME]

# ==========================
# Excel File Path
# ==========================
EXCEL_FILE = "hrms.xlsx"   # <-- change if needed

# Target tables (collections)
TABLES = ["Location", "PT_Mast", "Bank", "Tax", "CTC"]

def clean_record(record):
    """Convert NaN to None & add timestamps"""
    cleaned = {}
    for k, v in record.items():
        key = k.strip().lower()
        if pd.isna(v):
            cleaned[key] = None
        else:
            cleaned[key] = str(v)

    cleaned["cr_at"] = datetime.utcnow()
    cleaned["mo_at"] = datetime.utcnow()

    return cleaned


def process_sheet(sheet_name):
    print(f"Processing sheet: {sheet_name}")

    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)

    if df.empty:
        print(f"⚠ Sheet {sheet_name} is empty, skipping.")
        return

    records = df.to_dict(orient="records")
    cleaned_records = [clean_record(r) for r in records]

    collection = db[sheet_name.lower()]
    collection.insert_many(cleaned_records)

    print(f"✅ Inserted {len(cleaned_records)} records into {sheet_name}")


def main():
    excel = pd.ExcelFile(EXCEL_FILE)

    for sheet in excel.sheet_names:
        if sheet in TABLES:
            process_sheet(sheet)

    print("🎉 All sheets processed successfully!")


if __name__ == "__main__":
    main()
