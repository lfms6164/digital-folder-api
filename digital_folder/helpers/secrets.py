from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compare plain password provided by the user against the hashed password in the database.

    Args:
        plain_password (str): The plain password provided by the user during login.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if passwords match, False otherwise.
    """

    return pwd_context.verify(plain_password, hashed_password)
