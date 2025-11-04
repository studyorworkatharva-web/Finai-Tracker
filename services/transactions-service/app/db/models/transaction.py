from sqlalchemy import Column, Integer, String, DateTime, func, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Assumes users table exists
    
    # We add this relationship, but the User model is in another service.
    # This foreign key is just a number; we don't 'join' across services.
    # user = relationship("User") 

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True, nullable=False)
    amount = Column(Float(precision=2), nullable=False)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    category = relationship("Category")