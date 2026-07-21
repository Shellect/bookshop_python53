CREATE SCHEMA IF NOT EXISTS catalog;

CREATE TABLE IF NOT EXISTS catalog.books (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    poster VARCHAR(255) NULL,
    price DECIMAL(10, 2) NOT NULL CHECK(price >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

COMMENT ON TABLE catalog.books IS 'Книги в каталоге';

INSERT INTO catalog.books (title, author, poster, price)
VALUES 
( 'Трудно быть богом', 'Аркадий и Борис Стругацкие', '/img/1.jpg', 229 ),
( '1984', 'Джордж Оруэлл', '/img/2.jpg', 549 ),
( 'Понедельник начинается в субботу', 'Аркадий и Борис Стругацкие', '/img/3.jpg', 549 );