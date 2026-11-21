from fastapi import FastAPI
import mysql.connector

# Configure the MySQL connection
db_config = {
    "host": "localhost",
    "user": "mysql",
    "password": "1qaZ2wsX",
    "database": "frase_maleida"
}

HOST = "localhost"
PORT = 3000
API_VERSION = "v1"
baseApiUrl = f"http://{HOST}:{PORT}"

def get_db_connection():
    return mysql.connector.connect(**db_config)
 
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "This is the Frase Maleida API"}

@app.post("/fraseMaleida/v1/generate-game")

# this endpoint generates a new game based on the provided phrase
# The table "games" should have a MEDIUMTEXT column "phrase" to store the provided phrase
# and a primary key column "idgame" to uniquely identify each game
async def generate_game(phrase: str):
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