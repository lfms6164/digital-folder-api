from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from digital_folder.db.db import get_db
from digital_folder.db.models import Auth


def create_admin():
    db: Session = next(get_db())

    try:
        username = "df_admin"
        password = "df_Admin123!"

        hashed_password = bcrypt.hash(password)

        new_admin = Auth(username=username, password=hashed_password)

        db.add(new_admin)
        db.commit()
        print("Admin created...")
    finally:
        db.close()
        print("create_admin complete!")


if __name__ == "__main__":
    create_admin()
