import psycopg2

class UserData:
    def __init__(self):
        self.conn = None
        self.username = None

    def senddata(self,username):
        self.conn = psycopg2.connect(
            dbname={username},
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()
    
    def close(self):
        if self.conn:
            self.conn.close()