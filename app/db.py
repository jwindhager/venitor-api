from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

import settings

engine = create_engine(settings.DB_URL)

Base = automap_base()
Base.prepare(engine, reflect=True)
