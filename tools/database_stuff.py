import sqlite3
try:
    from .. import classifier_config
except:
    import classifier_config

db = sqlite3.connect(classifier_config.db_path)

def structureDB():
    db.execute("CREATE TABLE statements(statement, leaning, username)")
    db.commit()

def storeStatement(statement, leaning, username):
    db.execute(
        "INSERT INTO statements(statement, leaning, username) VALUES (?,?,?)",
        (statement, leaning, username)
    )
    db.commit()