from pydantic import BaseModel

class MovieBase(BaseModel):
    title: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    movies: list[Movie] = []

    class Config:
        orm_mode = True

