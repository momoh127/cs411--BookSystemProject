import bcrypt

def hash_password(password):
    """
    Hash a plain-text password using bcrypt.

    Args:
        password (str): The plain-text password.

    Returns:
        str: The hashed password as a string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8") 

def verify_password(plain_password, hashed_password):
    """
    Verify a plain-text password against a hashed password.

    Args:
        plain_password (str): The plain-text password.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))