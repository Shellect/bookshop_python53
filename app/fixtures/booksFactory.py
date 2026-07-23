import os
import psycopg2
import random
from faker import Faker
from dotenv import load_dotenv

load_dotenv()
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_DB = os.getenv("POSTGRES_DB")

fake = Faker('ru_RU')

with psycopg2.connect(
        host="database",
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
      ) as conn, conn.cursor() as cur:

    books = [(
        ' '.join(fake.words(nb=random.randint(2, 5))).title(),
        fake.name(),
        "/img/no_img.jpeg",
        random.randint(10000, 1000000)
        ) for _ in range(500)]

    # Выполняем запрос
    for i in range(0, 500, 50):
        cur.executemany("INSERT INTO catalog.books" \
        " (title, author, poster, price)" \
        "VALUES (%s, %s, %s, %s)", books[i:i+50])
    conn.commit()
    
