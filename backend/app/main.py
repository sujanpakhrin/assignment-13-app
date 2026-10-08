import os

import psycopg
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Assignment 13 API")


class Task(BaseModel):
    title: str


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "assignment13"),
        user=os.getenv("DB_USER", "assignment13"),
        password=os.getenv("DB_PASSWORD", "assignment13"),
    )


def ensure_table():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL
            )
            """
        )


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "backend",
    }


@app.get("/api/tasks")
def get_tasks():
    ensure_table()

    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title FROM tasks ORDER BY id"
        ).fetchall()

    return [
        {"id": row[0], "title": row[1]}
        for row in rows
    ]


@app.post("/api/tasks")
def create_task(task: Task):
    ensure_table()

    with get_connection() as conn:
        row = conn.execute(
            """
            INSERT INTO tasks (title)
            VALUES (%s)
            RETURNING id, title
            """,
            (task.title,),
        ).fetchone()

    return {
        "id": row[0],
        "title": row[1],
    }