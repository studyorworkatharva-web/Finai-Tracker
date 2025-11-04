from sqlalchemy.orm import Session
from app.db import models
from app.schemas.transaction import TransactionCreate


# -------------------------------------------------
# CRUD: Create Transaction
# -------------------------------------------------
def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = models.Transaction(
        description=transaction.description,
        amount=transaction.amount,
        category=transaction.category,
        date=transaction.date,
        user_id=user_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


# -------------------------------------------------
# CRUD: Get Transactions (all for a user)
# -------------------------------------------------
def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Transaction)
        .filter(models.Transaction.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# -------------------------------------------------
# CRUD: Get single Transaction
# -------------------------------------------------
def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()


# -------------------------------------------------
# CRUD: Delete Transaction
# -------------------------------------------------
def delete_transaction(db: Session, transaction_id: int):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if transaction:
        db.delete(transaction)
        db.commit()
    return transaction
