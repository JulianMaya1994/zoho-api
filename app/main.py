from fastapi import FastAPI
import psycopg2
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
    return {"status": "ok"}

@app.get("/tickets")
def get_tickets():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT id, subject, created_time FROM tickets_test LIMIT 50")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {"id": r[0], "subject": r[1], "created_time": r[2]}
        for r in rows
    ]
