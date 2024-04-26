from flask import Flask, render_template, request
import jwt
import secrets
import bcrypt
import psycopg2

app = Flask(__name__)

class User :
    def __init__(self,username):
        self.username = username
        self.hashed_password
        self.hashed_confpass
        self.SECRET_KEY

    def hash_pass(self,password,confpass):
        salt = bcrypt.gensalt()
        self.hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.hashed_confpass = bcrypt.hashpw(confpass.encode('utf-8'),salt)
        return self.hashed_password, self.hashed_confpass

    def genpayload(self):
        payload = {
            'username': self.username,
            'password': self.hashed_password,
            'confirmed_password' : self.hashed_confpass,
            # TTL (time to live for the token will be passed) --> later
        }
        return payload
    
    def gensecretkey():
        secret_key = secrets.token_urlsafe(32)
        return secret_key
    
    def gentoken(payload,secret_key):
        token = jwt.encode(payload,secret_key,algorithm="HS256")
        return token
    
class Database:
    def __init__(self) -> None:
        pass
    
    def connect():
        conn = psycopg2.connect(
            dbname="userdts",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

        # Create a cursor object to execute SQL queries
        cur = conn.cursor()

        # Define your SQL query with WHERE clause to insert data
        sql = "INSERT INTO your_table (column1, column2, column3) VALUES (%s, %s, %s) WHERE some_column = %s"

        # Define the data to be inserted
        data = ('value1', 'value2', 'value3', 'filter_value')

        # Execute the SQL query
        cur.execute(sql, data)

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

@app.route("/")
def welcome():
    return "<p>Welcome</p>"

@app.route("/register", )
def authpage():
    return render_template('auth.html')

@app.route("/register/user",methods=['POST'])
def register():
    USERNAME = request.form.get('username')
    PASSWORD = request.form.get('password')
    CONFPASS = request.form.get('confpass')
    
    if PASSWORD == CONFPASS:
        user = User(username=USERNAME)
        hashedpass , hashed_confpass = user.hash_pass(PASSWORD,CONFPASS)
        payload = user.genpayload()
        SECRET_KEY = user.gensecretkey()
        token = user.gentoken(payload,SECRET_KEY)
    else:
        return "<p>Password doesn't match with the confirmed password</p>"
    


    SECRET_KEY = secrets.token_urlsafe(32)
    
    
    print(token)
    return "<p>Thanks</p>"