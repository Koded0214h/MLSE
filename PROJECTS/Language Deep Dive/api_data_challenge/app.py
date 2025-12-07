import csv
from io import StringIO
from typing import List, Dict, Any

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field

# --- Pydantic Data Model for Validation ---
class FinancialRecord(BaseModel):
    # Field validation examples
    id: str = Field(..., description="Unique transaction ID")
    amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")
    # Enforcing specific values (debit or credit)
    type: str = Field(..., pattern="^(debit|credit)$", description="Transaction type") 
    date: str = Field(..., description="Transaction date (YYYY-MM-DD format assumed)")

class ConversionResponse(BaseModel):
    filename: str
    total_records: int
    valid_records: int
    invalid_records: int
    aggregated_data: Dict[str, Any]
    processed_records_sample: List[Dict[str, Any]] # A sample of the converted data

app = FastAPI(title="CSV Converter Service")

@app.post("/api/convert", response_model=ConversionResponse, tags=["CSV"])
async def convert_csv_to_json(csv_file: UploadFile = File(...)):
    """
    Accepts a CSV file, validates its contents, aggregates data, and returns a JSON report.
    """
    
    # 1. Read and Decode File Contents
    contents = await csv_file.read()
    
    try:
        decoded_contents = contents.decode('utf-8')
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding error: Must be UTF-8.")

    csv_stream = StringIO(decoded_contents)
    reader = csv.DictReader(csv_stream)
    
    valid_data: List[Dict[str, Any]] = []
    invalid_count = 0
    total_count = 0
    total_debit_amount = 0.0
    total_credit_amount = 0.0
    
    # 2. Process and Validate Data
    for row in reader:
        total_count += 1
        try:
            # Pydantic validation: attempts to convert and validate types/rules
            record = FinancialRecord(**row)
            
            # Aggregation logic
            if record.type == 'debit':
                total_debit_amount += record.amount
            elif record.type == 'credit':
                total_credit_amount += record.amount
                
            valid_data.append(record.model_dump())
            
        except Exception:
            invalid_count += 1
            # print(f"Invalid row skipped: {row}")
    
    # 3. Construct Response
    response = ConversionResponse(
        filename=csv_file.filename or "unknown.csv",
        total_records=total_count,
        valid_records=len(valid_data),
        invalid_records=invalid_count,
        aggregated_data={
            "total_debits": round(total_debit_amount, 2),
            "total_credits": round(total_credit_amount, 2),
            "net_balance": round(total_credit_amount - total_debit_amount, 2)
        },
        processed_records_sample=valid_data[:5] # Sample first 5 records
    )
    
    return response

# To run: uvicorn app:app --reload