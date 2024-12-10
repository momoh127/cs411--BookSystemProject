### A function that can be used to reset the database for further testing. 

import os
from database_setup import create_database

def reset_database(db_folder="databases", db_name="books.db"):
    """
    Ensures the specified database folder exists and sets the database file path.

    If the folder does not exist, it will be created. The function combines the folder 
    and database name to create the full database path.

    Args:
        db_folder (str): The folder where the database will be stored. Default is "databases".
        db_name (str): The name of the database file. Default is "books.db".
"""
    #ensure folder exists 
    os.makedirs(db_folder, exist_ok=True)
    db_path = os.path.join(db_folder, db_name)

    

    # Check if the database file exists
    if os.path.exists(db_path):
        # Delete the database file
        os.remove(db_path)
        print(f"Database file '{db_name}' deleted.")
    else:
        print(f"Database file '{db_name}' does not exist.")

    # Recreate the database
    create_database()

if __name__ == "__main__":
    reset_database()

