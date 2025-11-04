from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user # This dep is copied from Auth service
from app.db.models.user import User # This model is copied from Auth service
from app.db.models.transaction import Transaction, Category
from app.schemas.transaction import (
    TransactionCreate, TransactionPublic, CategoryCreate, CategoryPublic,
    PaginatedTransactions, CSVParsedRow
)
from app.crud import transaction as crud_transaction
from app.crud import category as crud_category
from app.core.ml import get_model, predict_category
from typing import List
import csv
import io
from datetime import datetime

router = APIRouter()
ml_model = get_model() # Load model on startup

@router.post("/", response_model=TransactionPublic, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # If category_id is not provided, try to predict it
    category_id = transaction.category_id
    if not category_id and transaction.category_name:
        # Find or create category
        category = crud_category.get_or_create_category(db, user_id=current_user.id, name=transaction.category_name)
        category_id = category.id
    elif not category_id:
        # Predict category
        prediction = predict_category(ml_model, transaction.description)
        if prediction['confidence'] > 0.5: # Confidence threshold
            category = crud_category.get_or_create_category(db, user_id=current_user.id, name=prediction['category'])
            category_id = category.id

    return crud_transaction.create_transaction(
        db=db, 
        transaction=transaction, 
        user_id=current_user.id, 
        category_id=category_id
    )

@router.get("/", response_model=PaginatedTransactions)
def read_transactions(
    skip: int = 0,
    limit: int = 25,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve paginated transactions for the current user.
    """
    total, transactions = crud_transaction.get_transactions(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return {"total": total, "items": transactions}

@router.post("/csv/parse", response_model=List[CSVParsedRow])
async def parse_csv_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """
    Parses a CSV file, predicts categories, and returns a JSON
    list for the user to confirm. Does NOT save to database.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a CSV.")

    contents = await file.read()
    file_data = io.StringIO(contents.decode('utf-8'))
    reader = csv.DictReader(file_data)
    
    parsed_rows: List[CSVParsedRow] = []
    
    try:
        for i, row in enumerate(reader):
            # Normalize common CSV headers
            description = row.get('Description') or row.get('description') or row.get('Memo')
            amount_str = row.get('Amount') or row.get('amount')
            date_str = row.get('Date') or row.get('date')

            if not all([description, amount_str, date_str]):
                 raise HTTPException(status_code=400, detail=f"Row {i+1}: Missing 'Date', 'Description', or 'Amount'.")
            
            # Simple parsing (can be made more robust)
            amount = float(amount_str)
            date = datetime.strptime(date_str, '%Y-%m-%d').date() # Assumes YYYY-MM-DD
            
            # Get ML prediction
            prediction = predict_category(ml_model, description)
            
            parsed_rows.append(
                CSVParsedRow(
                    row_id=i,
                    date=date,
                    description=description,
                    amount=amount,
                    suggested_category=prediction['category'],
                    confidence=prediction['confidence']
                )
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing CSV: {e}")
        
    return parsed_rows

# ... Other endpoints (CRUD for Categories, Goals, etc.) ...