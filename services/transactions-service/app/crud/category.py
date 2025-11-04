from sqlalchemy.orm import Session
from app.db import models
from app.schemas.transaction import CategoryCreate


# -------------------------------------------------
# CRUD: Create Category
# -------------------------------------------------
def create_category(db: Session, category: CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# -------------------------------------------------
# CRUD: Get all Categories
# -------------------------------------------------
def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


# -------------------------------------------------
# CRUD: Get Category by ID
# -------------------------------------------------
def get_category_by_id(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


# -------------------------------------------------
# CRUD: Delete Category
# -------------------------------------------------
def delete_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
    return category
