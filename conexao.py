
import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

load_dotenv(
    Path(__file__).resolve().parent / ".env",
    override=False
)

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_disabled=False,
        connection_timeout=10
    )
