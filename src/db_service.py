import sqlite3

class DbService():

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
    
    def execute_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        self.conn.commit()
        return cur, result
    
    def close_conn(self):
        self.conn.close()