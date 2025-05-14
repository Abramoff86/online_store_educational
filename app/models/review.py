from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, Date
from sqlalchemy.orm import relationship
from datetime import date

from app.backend.db import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    comment = Column(String)
    comment_date = Column(Date, default=date.today())
    grade = Column(Integer)
    is_active = Column(Boolean, default=True)

    user = relationship('User', back_populates='reviews')