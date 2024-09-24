from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, get_db
from fastapi.middleware.cors import CORSMiddleware

# Создаем таблицы в базе данных
models.Base.metadata.create_all(bind=engine)

# Создаем приложение FastAPI с префиксом /api
app = FastAPI(
    title="Favorite Movies API",
    description="API для управления пользователями и фильмами",
    version="1.0.0",
    openapi_prefix="/api"  # Префикс для всех маршрутов
)

# Настраиваем CORS (если фронтенд на другом домене)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Укажи конкретный домен для production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Маршрут для создания нового пользователя
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.create_user(db=db, user=user)

# Маршрут для получения всех фильмов
@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies

# Маршрут для добавления фильма для пользователя
@app.post("/users/{user_id}/movies/", response_model=schemas.Movie)
def create_movie_for_user(user_id: int, movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_movie_for_user(db=db, movie=movie, user_id=user_id)

