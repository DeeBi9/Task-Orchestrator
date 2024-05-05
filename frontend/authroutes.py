from flask import Flask, render_template, request, redirect, url_for, Blueprint
from frontend.utility.utils import User, Database
from frontend.utility.userutils import UserData

# Creating a blueprint instance
auth_blueprint = Blueprint('auth_blueprint',__name__, template_folder='templates')

@auth_blueprint.route("/",methods=['GET'])
def welcome():
    return "<p>Welcome</p>"

@auth_blueprint.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('authorize.html')
    elif request.method == 'POST':
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

@auth_blueprint.route("/login",methods=['GET','POST'])
def login():    
    
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':

        USERNAME = request.form.get('username')
        PASSWORD = request.form.get('password')

        db = Database()
        db.connect()
        cursor = db.conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE username = '{USERNAME}'")
        existing_user = cursor.fetchone()
        cursor.close()
        db.close()

        if existing_user:
            # Create an instance userdata of the UserData class
            userdata = UserData()

            # Send the username to the connect to the postgres server
            userdata.senddata(username=USERNAME)

            #
            cursor = userdata.conn.cursor()
            cursor.execute(f"SELECT * FROM WHERE username = '{USERNAME}'")
            cursor.close()
            userdata.close()

        else:
            return 