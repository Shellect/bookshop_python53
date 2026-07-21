from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/books")
async def get_books():
    conn = psycopg2.connect("host=database dbname=bookshop user=user password=12345678")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM catalog.books;")
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books