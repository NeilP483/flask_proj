from flask import Flask
import sqlite3
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def create_conn():
    conn = sqlite3.connect(Config.DB_PATH)
    return conn, conn.cursor()

from app import models, routes
