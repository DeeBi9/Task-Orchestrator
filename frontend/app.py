from flask import Flask, render_template, request, redirect, url_for
from utils import User, Database
from userutils import UserData

app = Flask(__name__)

@app.route("/")
def welcome():
    return "<p>Welcome</p>"

@app.route("/register")
def authpage():
    return render_template('./auth/authorize.html')

@app.route("/register/user", methods=['POST'])
def register():
    USERNAME = request.form.get('username')
    PASSWORD = request.form.get('password')
    CONFPASS = request.form.get('confpass')

    # Check if passwords match
    if PASSWORD != CONFPASS:
        return "<p>Password doesn't match with the confirmed password</p>"

    # Check if username already exists in the database
    db = Database()
    db.connect()
    cursor = db.conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{USERNAME}'")
    existing_user = cursor.fetchone()
    cursor.close()
    if existing_user:
        return f"<p>{USERNAME} already exists</p>"

    # Hash password
    user = User(username=USERNAME)
    hashedpass, hashed_confpass = user.hash_pass(PASSWORD, CONFPASS)
    
    # Generate token
    payload = user.genpayload()
    SECRET_KEY = user.gensecretkey()
    token = user.gentoken(payload, SECRET_KEY)

    try:
        # Insert new user into the database
        db.execute_query(f"INSERT INTO users (username, password) VALUES ('{USERNAME}', '{hashedpass.decode('utf-8')}')")
        print("User registered successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        db.close()

    print(token)
    # Redirect to login page if registration is successful
    return redirect(url_for('login'))


@app.route("/login")
def loginpage():
    return render_template("./auth/login.html")

@app.route("login/user")
def login():

    USERNAME = request.form.get('username')
    PASSWORD = request.form.get('password')

    # Create an instance userdata of the UserData class
    userdata = UserData()

    # Send the username to the connect to the postgres server
    userdata.senddata(username=USERNAME)

    #
    cursor = userdata.conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{USERNAME}'")
    cursor.close()

