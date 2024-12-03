import json
import mysql.connector
from flask import Flask, request
from flask_cors import CORS
import game


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'






if __name__ == '__main__':
    app.run(user_reloader=True, host='127.0.0.1', port=3000)
