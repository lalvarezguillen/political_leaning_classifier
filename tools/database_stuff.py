import sqlite3

db = sqlite3.connect("dataset.db")

def structureDB():
    db.execute("CREATE TABLE statements(statement, leaning, username)")
    db.commit()

def storeStatement(statement, leaning, username):
    db.execute(
        "INSERT INTO statements(statement, leaning, username) VALUES (?,?,?)",
        (statement, leaning, username)
    )
    db.commit()