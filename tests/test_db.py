import os
import sqlite3
from utils.db_utils import insert_user, get_user, delete_user, add_book, get_user_library
from config import DATABASE_PATH

def reset_test_database():
    """
    Reset the test database by dropping all tables and recreating them.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS Users;
        DROP TABLE IF EXISTS Books;
        DROP TABLE IF EXISTS User_Library;

        CREATE TABLE Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL
        );

        CREATE TABLE Books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            category TEXT
        );

        CREATE TABLE User_Library (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            status TEXT CHECK(status IN ('To read', 'Have read', 'Favorite')),
            FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
            FOREIGN KEY (book_id) REFERENCES Books(book_id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()

def test_insert_and_get_user():
    """Tests inserting a user into the database and retrieving the user's details."""
    reset_test_database()
    insert_user("testuser", "hashedpassword123")
    user = get_user("testuser")
    assert user is not None
    assert user[1] == "testuser"
    print("test_insert_and_get_user passed.")

def test_add_and_get_user_library():
    """ Tests adding a book to a user's library and retrieving the user's library."""
    reset_test_database()
    # Add a user and a book
    insert_user("testuser", "hashedpassword123")
    add_book("Python Programming", "John Doe", "Programming")

    # Simulate adding a book to the user's library
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT book_id FROM Books WHERE title = 'Python Programming'")
    book_id = cursor.fetchone()[0]
    cursor.execute("SELECT user_id FROM Users WHERE username = 'testuser'")
    user_id = cursor.fetchone()[0]

    cursor.execute("INSERT INTO User_Library (user_id, book_id, status) VALUES (?, ?, ?)", 
                   (user_id, book_id, "To read"))
    conn.commit()
    conn.close()

    library = get_user_library(user_id)
    assert len(library) == 1
    assert library[0][0] == "Python Programming"
    print("test_add_and_get_user_library passed.")

if __name__ == "__main__":
    test_insert_and_get_user()
    test_add_and_get_user_library()