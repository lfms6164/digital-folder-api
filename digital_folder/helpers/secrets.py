import pandas as pd
from pydantic import SecretStr


def get_scrt_key(db_path: str) -> SecretStr:
    """
    Retrieve the secret key (password) from the Excel DB.

    Args:
        db_path (str): The path to the Excel db.

    Returns:
        SecretStr: The secret key.
    """
    try:
        admin_df = pd.read_excel(db_path, sheet_name="Admin")

        secret_key = admin_df.iloc[0]["password"]

        return SecretStr(secret_key)
    except IndexError:
        raise ValueError(f"Unable to get secret key from database.")
    except Exception as e:
        raise RuntimeError(f"Error reading secret key: {e}")
