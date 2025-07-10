import sqlite3

def get_db():
    return sqlite3.connect("persona.db")
# Database connection and initialization
