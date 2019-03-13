import sqlite3

class Create:

    def __init__(self):
        pass

    def init_db(self):

        connection = sqlite3.connect("inventuur.db")
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS andmed (
            tootja text,
            toode text,
            jalanumber integer,
            kogus integer,
            hind integer
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS kohalikud_andmed (
            tootja text,
            toode text,
            jalanumber integer,
            kogus integer,
            hind integer
        )
        """)

        connection.commit()  # Committing the changes
        connection.close()


