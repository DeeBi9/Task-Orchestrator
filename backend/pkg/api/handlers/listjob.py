from flask import Flask, Blueprint

app = Flask(__name__)

getjob_blueprint = Blueprint('getjob_blueprint',__name__)

@getjob_blueprint.route("/login/jobs",methods=['GET'])
def getjobs():
    return "<p>Hi</p>"