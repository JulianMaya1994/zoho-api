from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = FastAPI()

def get_conn():
    return psycopg2.connect(
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT", 5432),
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD")
    )

@app.get("/")
def root():
    return {"status": "ok, API conectada a la nueva base de datos"}

# Le agregamos 'limit' y 'offset' para no saturar la memoria del contenedor
@app.get("/tickets")
def get_tickets():
    conn = get_conn()
    # Usamos RealDictCursor para que Postgres devuelva el JSON con las 187+ columnas y el raw_data
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Consultamos la tabla NUEVA con un límite de seguridad
    cur.execute("SELECT * FROM tickets LIMIT %s OFFSET %s", (limit, offset))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows
