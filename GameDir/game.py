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
    sql = """SELECT iso_country, ident, name, type, latitude_deg, longitude_deg
        FROM airport
        WHERE continent = 'EU' 
        AND type='large_airport'
        ORDER by RAND()
        LIMIT 3;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

# starting airport 
# ident ja type ei tarvita, otin ne pois for now(?)
# ident tarvitaan koska se käyttää sitä löytääkseen oikeen lentokentän: where ident = efhk
def get_airports_start():
    sql = """SELECT iso_country, ident, name, latitude_deg, longitude_deg
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

# get a question
"""
def get_question():
    sql = en muista mitä ope sano :c
"""

# game starts

# GAME SETTINGS

print('Kun olet valmis aloittamaan, ')
player = input('kirjoita pelaajan nimi: ')
# boolean for game over and win
game_over = False
win = False

player_range = 5000 # start range in km = 5000
#max_stamp = 3
#stamp = 0
all_airports = get_airports_start()
start_airport = all_airports[0]['ident']
current_airport = start_airport
game_id = create_game(player_range, start_airport, player, all_airports)

# GAME LOOP

while not game_over:
    # get current airport info
    airport = get_airport_info(current_airport)
    # show game status
    print(f'''Olet kohteessa {airport['name']}.''')
    print(f'''Sinulla on {player_range:.0f}km of range.''')
    # pause
    input('\033[32mPaina Enter jatkaaksesi...\033[0m')

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
        dest = input('Kirjoita määränpään icao: ')
        # makes sure the input is valid
        while dest != airports[0]['ident'] and dest != airports[1]['ident'] and dest != airports[2]['ident']:
            print('Virheellinen syöte, kokeile uudestaan.')
            dest = input('Kirjoita määränpään icao: ')

        selected_distance = calculate_distance(current_airport, dest)
        player_range -= selected_distance
        update_location(dest, player_range, game_id)
        current_airport = dest
        if player_range < 0:
            game_over = True

        '''
        kysymys tähän?
        
        question = get_question()
        print(question)
        vastaus = input()    
        if vastaus == answer:
            stamp += 1
            print("Oikein. Saat leiman.")
        else:
            print(f"Väärin. Oikea vastaus on {oikeavastaus}.")
        if stamp == max_stamp
            print("Olet kerännyt tarvittavan määrän leimoja.")
            break (???)
        '''

    #koska eurooppa osiossa ei voi voittaa, pitäskö tää siirtää pois loopista?
    if win:
        print(f'''You won! You have {player_range}km of range left.''')
        game_over = True

# turkki-ankara (LTAC), afganistan-kabul (OAKB), japani-tokyo (RJAA)
# yhdysvallat-seattle (KBFI), kanada-vancouver (CYVR), grönlanti-ilulissat (BGJN)

# if game is over loop stops
# show game result
print(f'''{'You won!' if win else 'You lost!'}''')
print(f'''Your range is {player_range:.0f}km''')