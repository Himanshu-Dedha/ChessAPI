from typing import Dict
from pydantic import BaseModel


class GetPlayers(BaseModel):
    usernames: list[str]

    class Config:
        orm_mode = True


class GetScore(BaseModel):
    ratings: Dict[str, int]

    class Config:
        orm_mode = True
