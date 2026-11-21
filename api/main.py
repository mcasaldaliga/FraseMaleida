from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import mysql.connector

# Configure the MySQL connection
db_config = {
    "host": "localhost",
    "user": "mysql",
    "port": 3306,
    "password": "1qaZ2wsX",
    "database": "frase_maleida"
}

HOST = "127.0.0.1"
PORT = 8000
API_VERSION = "v1"
baseApiUrl = f"http://{HOST}:{PORT}"

def get_db_connection():
    return mysql.connector.connect(**db_config)
 
app = FastAPI()


origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "This is the Frase Maleida API"}


class GameCreate(BaseModel):
    phrase: str


@app.post("/fraseMaleida/v1/generate-game")

# this endpoint generates a new game based on the provided phrase
# The table "games" should have a MEDIUMTEXT column "phrase" to store the provided phrase
# and a primary key column "idgame" to uniquely identify each game
async def generate_game(phrase: Optional[str] = None, game: Optional[GameCreate] = None):
    if phrase is None:
        if game is None:
            raise HTTPException(status_code=422, detail="A phrase is required")
        phrase = game.phrase

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO games (phrase) VALUES (%s)", (phrase,))
    id_game = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()

    game_url = f"{baseApiUrl}/fraseMaleida/{API_VERSION}/game/{id_game}"
    return {"url": game_url}

@app.get("/fraseMaleida/v1/game/{id_game}")
async def get_game(id_game: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT phrase FROM games WHERE idgame = %s", (id_game,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if row:
        return {"game_id": id_game, "phrase": row[0]}
    else:
        return {"error": "Game not found"}