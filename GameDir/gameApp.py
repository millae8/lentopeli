import json
import mysql.connector
from flask import Flask, request
from flask_cors import CORS
import game

# ??????????????????????????

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def fly(id, destination, budget=9000, player=None):
    if id==0:
        game = game(0, destination, budget, player)


@app.route('/newgame')
def newgame():
    args = request.args
    player = args.get('player')
    destination = args.get('location')
    json_data = fly(0, destination, 9000, player)
    return json_data


if __name__ == '__main__':
    app.run(user_reloader=True, host='127.0.0.1', port=3000)
