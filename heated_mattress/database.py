from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# TODO load sqlite path from properties
engine = create_engine('sqlite:///heated_mattress.sqlite3.db', convert_unicode=True)
session_factory = sessionmaker(autocommit=True, autoflush=True, bind=engine)
db_session = scoped_session(session_factory)

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import heated_mattress.models.dailyHeatedMattressJob
    Base.metadata.create_all(bind=engine)



