import mysql.connector
import json
from flask import Flask
from flask_cors import CORS
import random
import geopy


# ??????????????????????????

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='owngame',
    user='project',
    password='all1234',
    autocommit=True,
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'
)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/airports/')
def get_airport():
    sql = f'''SELECT country.name AS countryName, airport.iso_country, airport.ident, airport.name AS airportName, airport.latitude_deg, airport.longitude_deg, airport.type
        FROM country
        LEFT JOIN airport
        ON airport.iso_country = country.iso_country
        WHERE airport.continent = 'EU' 
        AND airport.type = 'large_airport'
        ORDER by RAND()
        LIMIT 3;'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return json.dumps(result)

@app.route('/api/get_question')
def get_question():
    sql = """select question,correct_answer,display_answer from task order by rand() limit 1;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchone()
    return json.dumps(result)

'''
@app.route('/newgame')
def newgame():
    args = request.args
    player = args.get('player')
    destination = args.get('location')
    json_data = fly(0, destination, 9000, player)
    return json_data
'''

if __name__ == '__main__':
    app.run(user_reloader=True, host='127.0.0.1', port=3000)
