from flask import Flask
from frontend.authroutes import auth_blueprint
from backend.pkg.api.handlers.listjob import getjob_blueprint

app = Flask(__name__)

app.register_blueprint(auth_blueprint)
app.register_blueprint(getjob_blueprint)

if __name__ == '__main__':
    app.run(debug=True)