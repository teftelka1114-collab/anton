from fastapi import FastAPI
from app.api import books, categories

app = FastAPI(
    title="Book API",
    description="API for managing books and categories",
    version="1.0.0"
)

app.include_router(books.router)
app.include_router(categories.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "Welcome to Book API", "docs": "/docs"}