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
async def get_books(page: int = 0):
    conn = psycopg2.connect("host=database dbname=bookshop user=user password=12345678")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM catalog.books LIMIT 10 OFFSET " + str(page * 10))
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books