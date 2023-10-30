from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

from app.db.base_class import Base

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

### sqlalchemy 2.0 이상 버전에서 자동으로 model -> table 생성을 위해 명시
Base.metadata.create_all(engine)