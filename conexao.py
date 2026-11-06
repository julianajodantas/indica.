
import mysql.connector
from dotenv import load_dotenv
import os
from pathlib import Path

# Localiza o arquivo .env na mesma pasta deste arquivo
caminho_env = Path(__file__).resolve().parent / ".env"

# Carrega as configurações e substitui valores antigos
load_dotenv(dotenv_path=caminho_env, override=True)

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )