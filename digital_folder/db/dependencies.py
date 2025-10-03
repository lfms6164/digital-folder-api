from digital_folder.db.service import DbService


def get_db():
    with DbService() as db:
        yield db
