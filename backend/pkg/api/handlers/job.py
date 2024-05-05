from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/jobs", methods=['POST'])
def create_job():
    
    # Data extracted from the request
    data = request.json

    # Using gRPC to transfer job from python code to the go code
    