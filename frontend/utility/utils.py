import jwt
import secrets
import bcrypt
import psycopg2

class User :
    def __init__(self, username):
        self.username = username
        self.hashed_password = None
        self.hashed_confpass = None
        self.SECRET_KEY = None

    def hash_pass(self, password, confpass):
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.hashed_confpass = bcrypt.hashpw(confpass.encode('utf-8'), salt)
        return self.hashed_password, self.hashed_confpass

    def genpayload(self):
        payload = {
            'username': self.username,
            'password': self.hashed_password.decode('utf-8'),  # Decoding bytes to string
            'confirmed_password': self.hashed_confpass.decode('utf-8'),  # Decoding bytes to string
            # TTL (time to live for the token will be passed) --> later
        }
        return payload
    
    @staticmethod
    def gensecretkey():
        secret_key = secrets.token_urlsafe(32)
        return secret_key
    
    @staticmethod
    def gentoken(payload, secret_key):
        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token
    
class Database:
    def __init__(self):
        self.conn = None
    
    def connect(self):
        self.conn = psycopg2.connect(
            dbname="userdts",
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

