import sqlite3
import os 

db_folder="databases", db_name="books.db"
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, db_name)

# A database utility function that inserts a new user into the database using a username and a hashed password.
def insert_user(username, hashed_password):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (username, hashed_password) VALUES (?, ?)", 
                       (username, hashed_password))
        conn.commit()
        print(f"User '{username}' added successfully!")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")
    finally:
        conn.close()

# A database utility function that fetches a user using a username
def get_user(username):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user  # Returns a tuple (user_id, username, hashed_password) or None

# A database utility function that deletes the user from the database using the username.
def delete_user(username):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Execute the DELETE query
        cursor.execute("DELETE FROM Users WHERE username = ?", (username,))
        
        # Commit the transaction
        conn.commit()
        
        # Check if any rows were affected (i.e., user was deleted)
        if cursor.rowcount > 0:
            print(f"User '{username}' deleted successfully!")
        else:
            print(f"User '{username}' not found.")
    except sqlite3.Error as e:
        # Handle any database errors
        print(f"Error: {e}")
    finally:
        # Close the connection
        conn.close()


def add_book_to_library(user_id, book_id, status="To read"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO User_Library (user_id, book_id, status) VALUES (?, ?, ?)", 
                   (user_id, book_id, status))
    conn.commit()
    conn.close()
    print(f"Book ID {book_id} added to User ID {user_id}'s library with status '{status}'.")

# Util functions for user library tables

def update_book_status(user_id, book_id, new_status):
    """
    Update the status of a book in a user's library.

    :param user_id: The ID of the user
    :param book_id: The ID of the book
    :param new_status: The new status (e.g., "Have read", "Favorite")
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Update the status for the specified user and book
        cursor.execute("""
            UPDATE User_Library
            SET status = ?
            WHERE user_id = ? AND book_id = ?
        """, (new_status, user_id, book_id))
        
        # Check if any rows were updated
        if cursor.rowcount > 0:
            print(f"Status updated to '{new_status}' for User ID {user_id} and Book ID {book_id}.")
        else:
            print(f"No record found for User ID {user_id} and Book ID {book_id}.")
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def get_user_library(user_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.title, b.author, ul.status
        FROM Books b
        JOIN User_Library ul ON b.book_id = ul.book_id
        WHERE ul.user_id = ?
    """, (user_id,))
    library = cursor.fetchall()
    conn.close()
    return library  # Returns a list of tuples (title, author, status)

### Book Library util functions

# A database utility function that inserts a book into the book library table using: title of the book, author of the book, and the category of the book.
def add_book(title, author, category):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Books (title, author, category) VALUES (?, ?, ?)", 
                   (title, author, category))
    conn.commit()
    conn.close()
    print(f"Book '{title}' added successfully!")

# A database utility function that deletes a book from the database using: title of the book and author of the book
def delete_book(title, author):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Execute the DELETE query
        cursor.execute("DELETE FROM Books WHERE title = ? AND author = ?", (title, author))
        
        # Commit the transaction
        conn.commit()
        
        # Check if any rows were affected
        if cursor.rowcount > 0:
            print(f"Book '{title}' by '{author}' deleted successfully!")
        else:
            print(f"Book '{title}' by '{author}' not found.")
    except sqlite3.Error as e:
        # Handle any database errors
        print(f"Error: {e}")
    finally:
        # Close the connection
        conn.close()

# General util functions

# A database utility function that prints the content of a specific table using: Table's name, and the database path 
def print_table_contents(table_name, db_path):
    """
    Prints the contents of the specified table in the given database.

    :param table_name: The name of the table to print contents from
    :param db_path: The full path to the database file
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Fetch all rows from the specified table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Fetch column names for better readability
        column_names = [description[0] for description in cursor.description]

        # Print column names as headers
        print(f"\nContents of table '{table_name}':")
        print(" | ".join(column_names))
        print("-" * 50)

        # Print each row
        for row in rows:
            print(" | ".join(str(value) for value in row))

        if not rows:
            print(f"No data in table '{table_name}'.")
    except sqlite3.Error as e:
        print(f"Error: Unable to fetch data from table '{table_name}'. Details: {e}")
    finally:
        conn.close()