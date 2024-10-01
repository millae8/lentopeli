from geopy import distance

import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='demogame',
    user='name',
    password='word',
    autocommit=True,
    charset='utf8mb4',
    collation='utf8mb4_unicode_ci'
)

# FUNCTIONS

# random 3 airports 
def get_airports():
    sql = (f"SELECT iso_country, ident, name, type, latitude_deg, longitude_deg"
        "FROM airport"
        "WHERE continent = 'EU'" 
        "AND type='large_airport'"
        "ORDER by RAND()"
        "LIMIT 3;")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

# starting airport 
# ident ja type ei tarvita, otin ne pois for now(?)
def get_airports_start():
    sql = """SELECT iso_country, name, latitude_deg, longitude_deg
        FROM airport
        WHERE ident = 'EFHK'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

# create new game
def create_game(p_range, cur_airport, p_name, a_ports):
    sql = "INSERT INTO game (player_range, location, screen_name) VALUES (%s, %s, %s);"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (p_range, cur_airport, p_name))
    g_id = cursor.lastrowid

    return g_id

# get airport info
def get_airport_info(icao):
    sql = f'''SELECT iso_country, ident, name, latitude_deg, longitude_deg
                  FROM airport
                  WHERE ident = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return result

# calculate distance between two airports
def calculate_distance(current, target):
    start = get_airport_info(current)
    end = get_airport_info(target)
    return distance.distance((start['latitude_deg'], start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km

# update location
def update_location(icao, p_range, g_id):
    sql = f'''UPDATE game SET location = %s, player_range = %s WHERE id = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao, p_range, g_id))

# game starts

# GAME SETTINGS

print('When you are ready to start, ')
player = input('type player name: ')
# boolean for game over and win
game_over = False
win = False

player_range = 5000 # start range in km = 5000
score = 0
all_airports = get_airports_start()
start_airport = all_airports[0]['ident']
current_airport = start_airport
game_id = create_game(player_range, start_airport, player, all_airports)

# GAME LOOP

while not game_over:
    # get current airport info
    airport = get_airport_info(current_airport)
    # show game status
    print(f'''You are at {airport['name']}.''')
    print(f'''You have {player_range:.0f}km of range.''')
    # pause
    input('\033[32mPress Enter to continue...\033[0m')

    # if no range, game over
    # show airports in range. if none, game over
    airports = get_airports()
    print(f'''\033[34mThere are {len(airports)} airports in range: \033[0m''')
    if len(airports) == 0:
        print('You are out of range.')
        game_over = True
    else:
        print(f'''Airports: ''')
        for airport in airports:
            ap_distance = calculate_distance(current_airport, airport['ident'])
            print(f'''{airport['name']}, icao: {airport['ident']}, distance: {ap_distance:.0f}km''')
        # ask for destination
        dest = input('Enter destination icao: ')
        # makes sure the input is valid
        while dest != airports[0]['ident'] and dest != airports[1]['ident'] and dest != airports[2]['ident']:
            print('Input invalid, try again.')
            dest = input('Enter destination icao: ')

        selected_distance = calculate_distance(current_airport, dest)
        player_range -= selected_distance
        update_location(dest, player_range, game_id)
        current_airport = dest
        if player_range < 0:
            game_over = True
    # TODO
    if win and current_airport == start_airport:
        print(f'''You won! You have {player_range}km of range left.''')
        game_over = True

# if game is over loop stops
# show game result
print(f'''{'You won!' if win else 'You lost!'}''')
print(f'''Your range is {player_range:.0f}km''')
