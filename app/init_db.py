import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal, engine
from app.db import models
from app.db.crud import create_category, create_book

def init_database():
    models.Base.metadata.create_all(bind=engine)
    print("Tables created")

    db = SessionLocal()

    categories = ["Fantasy", "Detective"]
    for cat in categories:
        create_category(db, cat)
        print(f"Category added: {cat}")

    books = [
        {"title": "Dune", "description": "Sci-fi novel", "price": 750, "category": "Fantasy"},
        {"title": "1984", "description": "Dystopia", "price": 450, "category": "Fantasy"},
        {"title": "Murder on the Orient Express", "description": "Classic detective", "price": 480, "category": "Detective"},
    ]

    all_cats = db.query(models.Category).all()
    cat_dict = {c.title: c.id for c in all_cats}

    for book in books:
        create_book(db, book["title"], book["description"], book["price"], cat_dict[book["category"]])
        print(f"Book added: {book['title']}")

    db.close()
    print("Database initialized")

if __name__ == "__main__":
    init_database()