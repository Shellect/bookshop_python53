import os
import psycopg2
import random
from faker import Faker
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": "database",
    "password": os.getenv("POSTGRES_PASSWORD"),
    "user": os.getenv("POSTGRES_USER"),
    "dbname": os.getenv("POSTGRES_DB")
}
fake = Faker('ru_RU')

if __name__ == "__main__":
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
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

