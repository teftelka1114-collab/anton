from sqlalchemy.orm import Session
from app.db import models

def create_category(db: Session, title: str):
    category = models.Category(title=title)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_all_categories(db: Session):
    return db.query(models.Category).all()

def create_book(db: Session, title: str, description: str, price: int, category_id: int):
    book = models.Book(
        title=title,
        description=description,
        price=price,
        category_id=category_id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_all_books(db: Session):
    return db.query(models.Book).all()