-- in postgresql


-- Create table member
CREATE TABLE member (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    birth DATE NOT NULL,
    can_borrow BOOLEAN NOT NULL,
    ban BOOLEAN NOT NULL DEFAULT FALSE,
);

-- add ban columns in member table in postgresql
ALTER TABLE member ADD COLUMN ban BOOLEAN NOT NULL DEFAULT FALSE;

CREATE TABLE book (
    isbn SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    author VARCHAR(50) NOT NULL,
    publish_date DATE NOT NULL,
    quantity INT NOT NULL
);

CREATE TABLE ticket (
    id SERIAL PRIMARY KEY,
    member_id INT NOT NULL,
    book_isbn INT NOT NULL,
    quantity INT NOT NULL,
    borrow_date DATE NOT NULL,
    return_date DATE NOT NULL,
    FOREIGN KEY (member_id) REFERENCES member(id),
    FOREIGN KEY (book_isbn) REFERENCES book(isbn)
);

CREATE TABLE role (
    member_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    PRIMARY KEY (member_id, name),
    FOREIGN KEY (member_id) REFERENCES member(id)
);

CREATE TABLE category (
    name VARCHAR(50) NOT NULL,
    book_isbn INT NOT NULL,
    description VARCHAR(50) NOT NULL,
    PRIMARY KEY (name, book_isbn),
    FOREIGN KEY (book_isbn) REFERENCES book(isbn)
);

-- insert data 
INSERT INTO member (name, password, birth, can_borrow) VALUES ('John', '1234', '1990-01-01', true, false);
INSERT INTO member (name, password, birth, can_borrow) VALUES ('Mary', '1234', '1990-01-01', true, false);

-- delete member


INSERT INTO book (name, author, publish_date, quantity) VALUES ('Harry Potter', 'J.K. Rowling', '1997-06-26', 10);
INSERT INTO book (name, author, publish_date, quantity) VALUES ('The Lord of the Rings', 'J.R.R. Tolkien', '1954-07-29', 10);

INSERT INTO book(name, author, publish_date, quantity) VALUES ('The Hobbit', 'J.R.R. Tolkien', '1937-09-21', 30);
INSERT INTO book(name, author, publish_date, quantity) VALUES ('The Fellowship of the Ring', 'Arthur Isnard', '1954-07-29', 55);

INSERT INTO ticket (member_id, book_isbn, quantity, borrow_date, return_date) VALUES (1, 1, 1, '2019-01-01', '2019-01-08');
INSERT INTO ticket (member_id, book_isbn, quantity, borrow_date, return_date) VALUES (1, 2, 1, '2019-01-01', '2019-01-08');

INSERT INTO role (member_id, name) VALUES (1, 'admin');
INSERT INTO role (member_id, name) VALUES (2, 'member');

INSERT INTO category (name, book_isbn, description) VALUES ('fantasy', 1, 'fantasy book');
INSERT INTO category (name, book_isbn, description) VALUES ('fantasy', 2, 'fantasy book');

-- query
-- 1. List all books
SELECT * FROM book;

-- 2. List all books that are available to borrow
SELECT * FROM book WHERE quantity > 0;

-- 3. List all books that are not available to borrow
SELECT * FROM book WHERE quantity = 0;

-- create view from book
CREATE VIEW available_book AS
SELECT * FROM book WHERE quantity > 0;

CREATE VIEW unavailable_book AS
SELECT * FROM book WHERE quantity = 0;

-- 4. List all books that are available to borrow and have the category fantasy
SELECT * FROM available_book WHERE isbn IN (SELECT book_isbn FROM category WHERE name = 'fantasy');

-- 5. List all books that are available to borrow and have the category fantasy and the author is J.K. Rowling
SELECT * FROM available_book WHERE isbn IN (SELECT book_isbn FROM category WHERE name = 'fantasy') AND author = 'J.K. Rowling';CREATE VIEW view_name AS query;

-- 6. List all books that are available to borrow and have the category fantasy and the author is J.K. Rowling and the book name is Harry Potter
SELECT * FROM available_book WHERE isbn IN (SELECT book_isbn FROM category WHERE name = 'fantasy') AND author = 'J.K. Rowling' AND name = 'Harry Potter';

-- 7. List all books that are available to borrow and have the category fantasy and the author is J.K. Rowling and the book name is Harry Potter and the publish date is 1997-06-26
SELECT * FROM available_book WHERE isbn IN (SELECT book_isbn FROM category WHERE name = 'fantasy') AND author = 'J.K. Rowling' AND name = 'Harry Potter' AND publish_date = '1997-06-26';

-- 8. List all books that are available to borrow and have the category fantasy and the author is J.K. Rowling and the book name is Harry Potter and the publish date is 1997-06-26 and the quantity is 10
SELECT * FROM available_book WHERE isbn IN (SELECT book_isbn FROM category WHERE name = 'fantasy') AND author = 'J.K. Rowling' AND name = 'Harry Potter' AND publish_date = '1997-06-26' AND quantity = 10;

-- 9. List all books that are available to borrow and have the category fantasy and the author is J.K. Rowling and the book name is Harry Potter and the publish date is 1997-06-26 and the quantity is 10 and the book is not borrowed by any member
SELECT * FROM available_book WHERE isbn IN (SELECT book_isbn FROM category WHERE name = 'fantasy') AND author = 'J.K. Rowling' AND name = 'Harry Potter' AND publish_date = '1997-06-26' AND quantity = 10 AND isbn NOT IN (SELECT book_isbn FROM ticket);

-- 10. List all books that are available to borrow and have the category fantasy and the author is J.K. Rowling and the book name is Harry Potter and the publish date is 1997-06-26 and the quantity is 10 and the book is not borrowed by any member and the book is not borrowed by any member in the last 7 days
SELECT * FROM available_book WHERE isbn IN (SELECT book_isbn FROM category WHERE name = 'fantasy') AND author = 'J.K. Rowling' AND name = 'Harry Potter' AND publish_date = '1997-06-26' AND quantity = 10 AND isbn NOT IN (SELECT book_isbn FROM ticket) AND isbn NOT IN (SELECT book_isbn FROM ticket WHERE borrow_date > '2019-01-01');

-- transaction for book TABLE
-- 1. Borrow a book
UPDATE book SET quantity = quantity - 1 WHERE isbn = 1;

-- 2. Return a book
UPDATE book SET quantity = quantity + 1 WHERE isbn = 1;

-- 3. Add a new book
INSERT INTO book (name, author, publish_date, quantity) VALUES ('The Hobbit', 'J.R.R. Tolkien', '1937-09-21', 10);

-- 4. Delete a book
DELETE FROM book WHERE isbn = 1;

-- 5. Update a book
UPDATE book SET name = 'The Hobbit 2' WHERE isbn = 1;

-- 6. Add a new category
INSERT INTO category (name, book_isbn, description) VALUES ('fantasy', 1, 'fantasy book');

-- 7. Delete a category
DELETE FROM category WHERE name = 'fantasy' AND book_isbn = 1;CREATE VIEW view_name AS query;

-- 8. Update a category
UPDATE category SET description = 'fantasy book 2' WHERE name = 'fantasy' AND book_isbn = 1;

-- 9. Add a new member
INSERT INTO member (name, password, birth, can_borrow) VALUES ('John', '1234', '1990-01-01', true);

-- 10. Delete a member
DELETE FROM member WHERE id = 1;

-- 11. Update a member
UPDATE member SET name = 'John 2' WHERE id = 1;

-- 12. Add a new role
INSERT INTO role (member_id, name) VALUES (1, 'admin');

-- 13. Delete a role
DELETE FROM role WHERE member_id = 1 AND name = 'admin';

-- 14. Update a role
UPDATE role SET name = 'admin 2' WHERE member_id = 1 AND name = 'admin';

-- 15. Add a new ticket
INSERT INTO ticket (member_id, book_isbn, quantity, borrow_date, return_date) VALUES (1, 1, 1, '2019-01-01', '2019-01-08');

-- 16. Delete a ticket
DELETE FROM ticket WHERE member_id = 1 AND book_isbn = 1;

-- 17. Update a ticket
UPDATE ticket SET quantity = 2 WHERE member_id = 1 AND book_isbn = 1;

