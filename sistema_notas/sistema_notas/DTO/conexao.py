from dotenv import dotenv_values, load_dotenv
from sqlalchemy.engine import URL, create_engine


def get_db_connection():
    load_dotenv()
    values = dotenv_values()

    url_object = URL.create(
        username=values["USERNAME"],
        password=values["PASSWORD"],
        database=values["DATABASE"],
        host=values["HOST"],
        drivername=values["DRIVERNAME"],
    )

    engine = create_engine(url_object)
    return engine
