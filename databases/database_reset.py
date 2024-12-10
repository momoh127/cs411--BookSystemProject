### A function that can be used to reset the database for further testing. 

import os
from database_setup import create_database

def reset_database(db_folder="databases", db_name="books.db"):
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

