from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.db import crud
from app.schemas import BookCreate, BookUpdate, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=list[BookResponse])
def get_books(
    category_id: int | None = Query(None, description="Filter by category ID"),
    db: Session = Depends(get_db)
):
    if category_id:
        return crud.get_books_by_category(db, category_id)
    return crud.get_all_books(db)

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    category = crud.get_category_by_id(db, book.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.create_book(
        db,
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url
    )

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    existing = crud.get_book_by_id(db, book_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.category_id is not None:
        category = crud.get_category_by_id(db, book.category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        existing.category_id = book.category_id

    if book.title is not None:
        existing.title = book.title
    if book.description is not None:
        existing.description = book.description
    if book.price is not None:
        existing.price = book.price
    if book.url is not None:
        existing.url = book.url

    db.commit()
    db.refresh(existing)
    return existing

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return None