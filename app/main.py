import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import SessionLocal
from app.db.crud import get_all_categories, get_all_books

def main():
    db = SessionLocal()

    categories = get_all_categories(db)
    print(f"Categories: {len(categories)}")

    for cat in categories:
        print(f"\nCategory: {cat.title}")
        for book in cat.books:
            print(f"  - {book.title} | {book.price} rub | {book.description}")

    print(f"\nTotal books: {len(get_all_books(db))}")
    db.close()

if __name__ == "__main__":
    main()