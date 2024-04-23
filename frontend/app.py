from flask import Flask, render_template

app = Flask(__name__)

class User :
    def __init__(self,username,password,confpass):
        self.username = username
        self.password = password
        self.confpass = confpass



@app.route("/")
def welcome():
    return "<p>Welcome</p>"

@app.route("/register")
def register():
    return render_template('auth.html')
