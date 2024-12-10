import sqlite3
import os
from config import DATABASE_PATH

os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

# connect to the database
def get_connection():
    """Get a connection to the database."""
    return sqlite3.connect(DATABASE_PATH)

# inserts a new user into the database using a username and a hashed password.
def insert_user(username, hashed_password):
    """
    Insert a new user into the Users table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (username, hashed_password) VALUES (?, ?)", 
                       (username, hashed_password))
        conn.commit()
        print(f"User '{username}' added successfully!")
    except sqlite3.IntegrityError:
        raise Exception("Username already exists.")
    finally:
        conn.close()

# fetches a user using a username.
def get_user(username):
    """
    Fetch a user from the Users table by username.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT user_id, username, hashed_password FROM Users WHERE username = ?", (username,))
        user = cursor.fetchone()
        return user
    finally:
        conn.close()

# deletes the user from the database using the username.
def delete_user(username):
    """
    Delete a user from the Users table by username.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"User '{username}' deleted successfully!")
        else:
            print(f"User '{username}' not found.")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

# adds a book to the user's library.
def add_book_to_library(user_id, book_id, status="To read"):
    """
    Add a book to the User_Library table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO User_Library (user_id, book_id, status) VALUES (?, ?, ?)", 
                       (user_id, book_id, status))
        conn.commit()
        print(f"Book ID {book_id} added to User ID {user_id}'s library with status '{status}'.")
    finally:
        conn.close()

# updates the status of a book in the user's library.
def update_book_status(user_id, book_id, new_status):
    """
    Update the status of a book in a user's library.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE User_Library
            SET status = ?
            WHERE user_id = ? AND book_id = ?
        """, (new_status, user_id, book_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Status updated to '{new_status}' for User ID {user_id} and Book ID {book_id}.")
        else:
            print(f"No record found for User ID {user_id} and Book ID {book_id}.")
    finally:
        conn.close()

# function that retrieves all books in a user's library.
def get_user_library(user_id):
    """
    Retrieve a user's library with book details and statuses.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT b.title, b.author, ul.status
            FROM Books b
            JOIN User_Library ul ON b.book_id = ul.book_id
            WHERE ul.user_id = ?
        """, (user_id,))
        library = cursor.fetchall()
        return library
    finally:
        conn.close()

# A database utility function that inserts a book into the Books table.
def add_book(title, author, category):
    """
    Add a new book to the Books table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Books (title, author, category) VALUES (?, ?, ?)", 
                       (title, author, category))
        conn.commit()
        print(f"Book '{title}' added successfully!")
    finally:
        conn.close()

# A database utility function to fetch all books from the Books table.
def get_all_books():
    """
    Fetch all books from the Books table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT book_id, title, author, category FROM Books")
        books = cursor.fetchall()
        return books
    finally:
        conn.close()

# Resets the database by clearing all tables.
def reset_test_database():
    """
    Reset the database by clearing all data in the tables.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Clear all data from the tables
        cursor.execute("DELETE FROM User_Library;")
        cursor.execute("DELETE FROM Books;")
        cursor.execute("DELETE FROM Users;")
        conn.commit()
        print("Test database reset successfully!")
    except sqlite3.Error as e:
        print(f"Error resetting database: {e}")
    finally:
        conn.close()