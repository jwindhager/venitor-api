from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

import settings

engine = create_engine(settings.DB_URL)

Base = automap_base()
Base.prepare(engine, reflect=True)

# TODO final table mapping
Device = Base.classes.Device_api2
Facilities = Base.classes.Facilities_api2
Status = Base.classes.Status_api2


def create_session():
    session = Session(bind=engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
