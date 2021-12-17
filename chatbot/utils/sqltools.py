import sqlite3

connection = sqlite3.connect('feedback.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = "CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY,username text,email text , content text)"
cursor.execute(create_table)

connection.commit()

connection.close()