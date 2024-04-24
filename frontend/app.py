from flask import Flask, render_template, request

app = Flask(__name__)

SECRET_KEY = b'\xe1\x97=\x1a\xbe\xe8\xa4$\xc3~\xbf\xb9\xd6\xc3\xb3\xed5i\x87Q\x1f\x15\x02}NW \x08\xd5\xeeb\x82'

class User :
    def __init__(self,username,password,confpassword):
        self.username = username
        self.password = password
        self.confpassword = confpassword

    def display(self):
        print(self.username,self.password, self.confpassword)


@app.route("/")
def welcome():
    return "<p>Welcome</p>"

@app.route("/register", )
def authpage():
    return render_template('auth.html')

@app.route("/register/user",methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    confpass = request.form.get('confpass')
    
    if password == confpass:
        user = User(username=username, password=password,confpassword=confpass)
    else:
        return "<p>Wrong username or password</p>"
    payload = {
        'username': username,
        'password': password,
        'confirmed_password' : confpass,
    }
    user.display()
    return "<p>Thanks</p>"