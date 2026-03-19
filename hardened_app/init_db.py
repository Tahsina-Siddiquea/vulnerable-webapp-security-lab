import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS users")

cursor.execute("""
CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT,
email TEXT
)
""")

users = [
("alice","password123","alice@email.com"),
("bob","password123","bob@email.com"),
("admin","adminpass","admin@email.com")
]

cursor.executemany(
"INSERT INTO users(username,password,email) VALUES(?,?,?)",
users
)

conn.commit()
conn.close()

print("Database initialized")
print("Users created: alice, bob, admin")