from sqlalchemy import Column, Integer, String, JSON, DateTime
from .database import Base


class PlayerRatingHistory(Base):
    __tablename__ = 'player_rating_history'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    rating_history = Column(JSON, nullable=False)  # Store rating history as JSON
    last_updated = Column(DateTime, nullable=False)