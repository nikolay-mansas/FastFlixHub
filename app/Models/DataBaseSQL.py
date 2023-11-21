create_table_sql = """CREATE TABLE IF NOT EXISTS Users
(
    ID INTEGER NOT NULL,
    Email TEXT NOT NULL,
    Name TEXT NOT NULL,
    Age TEXT NOT NULL,
    Hiden TEXT NOT NULL,
    Amount TEXT NOT NULL
);
"""

search_user_by_ID = """SELECT * FROM Users WHERE ID=?"""
search_user_by_email = """SELECT * FROM Users WHERE Email=?"""
