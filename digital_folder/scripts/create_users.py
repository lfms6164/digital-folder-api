from passlib.hash import bcrypt

from digital_folder.db.db import SessionLocal
from digital_folder.db.models import User, UserRole


def create_users():
    db = SessionLocal()

    try:
        user = User(
            username="df_user",
            password=bcrypt.hash("df_user"),
            role=UserRole.USER,
        )
        viewer = User(
            username="df_viewer",
            password=bcrypt.hash("df_viewer"),
            role=UserRole.VIEWER,
        )

        db.add_all([user, viewer])
        db.commit()
        print(f"User created... id: {user.id}")
    finally:
        db.close()
        print("create_users complete!")


if __name__ == "__main__":
    create_users()
