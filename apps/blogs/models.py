from sqlalchemy import Column, Integer, String
from database import Base  # Adjusted import

class Blog(Base):
    __tablename__ = "blogs"

    id        = Column(Integer, primary_key=True, index=True)
    title     = Column(String, index=True)
    content   = Column(String, index=True)
