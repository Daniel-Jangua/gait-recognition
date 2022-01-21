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
    
    def insert_query(self, query, data):
        cur = self.conn.cursor()
        cur.execute(query, data)
        self.conn.commit()
    
    def close_conn(self):
        self.conn.close()