from geopy import distance
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='base',
    user='name',
    password='secret',
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
def get_airports_start():
    sql = """SELECT iso_country, ident, name, latitude_deg, longitude_deg
        FROM airport
        WHERE ident = 'EFHK'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall() # pitääkö tässä olla fetchone fetchall:n tilalle?
    return result

# create new game
# #vaihdoin info:t game:n ku en saanut muuten toimimaan mut jos muilla toimii saa vaihtaa takasin
def create_game(cur_airport, p_name, a_ports):
    sql = "INSERT INTO game (location, screen_name) VALUES (%s, %s);"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (cur_airport, p_name))
    g_id = cursor.lastrowid

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
def update_location(icao, g_id):
    sql = f'''UPDATE game SET location = %s WHERE id = %s'''
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, (icao, g_id))

# hakee kysymyksiä randomisti 1 kpl
def get_question():
    sql = (f"select question,correct_answer,display_answer from task order by rand() limit 1")
    cursor = conn.cursor()
    cursor.execute(sql)
    result_row = cursor.fetchone()
    # palauttaa monikon, paitsi jos tyhjä tulosjoukko -> tulostaa None
    return result_row

# game starts

# GAME SETTINGS

print('Kun olet valmis aloittamaan, ')
player = input('kirjoita pelaajan nimi: ')
# boolean for game over and win
game_over = False
win = False

max_stamp = 3
stamp = 0
budget = 6000
all_airports = get_airports_start()
start_airport = all_airports[0]['ident']
current_airport = start_airport
game_id = create_game(start_airport, player, all_airports)

# GAME LOOP

while not game_over:
    # get current airport info
    airport = get_airport_info(current_airport)
    # show game status
    print(f'''Olet kohteessa {airport['name']}.''')
    # pause
    input('\033[32mPaina Enter jatkaaksesi...\033[0m')

    airports = get_airports()
    print(f'''Lentokentät: ''')
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
    update_location(dest, game_id)
    current_airport = dest

    question, correct_answer, display_answer = get_question()
    answer = input(f"{question}: ")
    if answer == correct_answer:
        stamp += 1
        print("Oikein. Saat leiman.")
    else:
        print(f"Väärin. Oikea vastaus on {display_answer}.")
    if stamp == max_stamp:
        print("Olet kerännyt tarvittavan määrän leimoja.")
        break

#_______________________________________________________
# tästä alkaa euroopan jälkeinen osio

# turkey
def get_airport1():
    sql = """SELECT iso_country, ident, name, latitude_deg, longitude_deg
        FROM airport
        WHERE ident = 'LTAC'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

# get current airport info
airport = get_airport_info(current_airport)
# show game status
print(f'''You are at {airport['name']}.''')
# pause
input('\033[32mPress Enter to continue...\033[0m')

#turkin lentokenttä
airports = get_airport1()
print(f'''Seuraava kohteesi on: ''')
for airport in airports:
    ap_distance = calculate_distance(current_airport, airport['ident'])
    print(f'''{airport['name']}, distance: {ap_distance:.0f}km''')
dest = airport['ident']

selected_distance = calculate_distance(current_airport, dest)
update_location(dest, game_id)
current_airport = dest
#pause
input('\033[32mPress Enter to continue...\033[0m')

#turkin kysymys
vastaus1 = input('''Vaikuttaako lentäminen otsonikerrokseen? A) Ei vaikuta B) Vaikuttaa : ''')
if vastaus1 == 'a' or 'A':
    print("Vastasit oikein.")
    budget += 500
    print(f"Tämän hetkinen budjettisi on {budget}")
else:
    print("Vastasit väärin, oikea vastaus on A) Ei vaikuta.")
    print(f"Tämän hetkinen budjettisi on {budget}.")

#________________________________________________
# Afganistan

def get_airport2():
    sql = """Select iso_country, ident, name, latitude_deg, longitude_deg
        from airport
        where ident = 'OAKB'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

airport = get_airport_info(current_airport)

print(f'''You are at {airport['name']}.''')
# pause
input('\033[32mPress Enter to continue...\033[0m')

# turkista afganistaniin
# afganistanin lentokenttä
airports = get_airport2()
print(f'''Seuraava kohteesi on: ''')
for airport in airports:
    ap_distance = calculate_distance(current_airport, airport['ident'])
    print(f'''{airport['name']}, distance: {ap_distance:.0f}km''')
dest = airport['ident']

selected_distance = calculate_distance(current_airport, dest)
update_location(dest, game_id)
current_airport = dest
input('\033[32mPress Enter to continue...\033[0m')

# afganistanin kysymys
vastaus2 = input("Kuinka monta prosenttia maailman päästöistä syntyy lennoista? A) 15% B) 0,5-1% C) 2-3% : ")
if vastaus2 == 'c' or 'C':
    print("Vastasit oikein.")
    budget += 500
    print(f"Tämän hetkinen budjettisi on {budget}.")
else:
    print("Vastasit väärin, oikea vastaus on C) 2-3%.")
    print(f'Tämän hetkinen budjettisi on {budget}.')

def get_airport3():
    sql = """SELECT iso_country, ident, name, latitude_deg, longitude_deg
        FROM airport
        WHERE ident = 'RJAA'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

airport = get_airport_info(current_airport)
# show game status
print(f'''You are at {airport['name']}.''')
# pause
input('\033[32mPress Enter to continue...\033[0m')

#------------------------------------------------
#japani
airports = get_airport3()
print(f'''Seuraava kohteesi on: ''')
for airport in airports:
    ap_distance = calculate_distance(current_airport, airport['ident'])
    print(f'''{airport['name']}, distance: {ap_distance:.0f}km''')
dest = airport['ident']

selected_distance = calculate_distance(current_airport, dest)
update_location(dest, game_id)
current_airport = dest
input('\033[32mPress Enter to continue...\033[0m')

#japanin kysymys
vastaus3 = input("Kysymys? A) vastaus B) vastaus : ")
if vastaus3 == 'a' or 'A':
    print("Vastasit oikein.")
    budget += 500
    print(f"Tämän hetkinen budjettisi on {budget}")
else:
    print("Vastasit väärin, oikea vastaus on A) vastaus.")
    print(f"Tämän hetkinen budjettisi on {budget}.")

# yhdysvallat
def get_airport4():
    sql = """SELECT iso_country, ident, name, latitude_deg, longitude_deg
        FROM airport
        WHERE ident = 'KBFI'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

airport = get_airport_info(current_airport)
# show game status
print(f'''You are at {airport['name']}.''')
# pause
input('\033[32mPress Enter to continue...\033[0m')

airports = get_airport4()
print(f'''Seuraava kohteesi on: ''')
for airport in airports:
    ap_distance = calculate_distance(current_airport, airport['ident'])
    print(f'''{airport['name']}, distance: {ap_distance:.0f}km''')
dest = airport['ident']

selected_distance = calculate_distance(current_airport, dest)
update_location(dest, game_id)
current_airport = dest
input('\033[32mPress Enter to continue...\033[0m')

#usan kysymys
vastaus4 = input("Kysymys? A) vastaus B) vastaus : ")
if vastaus4 == 'a' or 'A':
    print("Vastasit oikein.")
    budget += 500
    print(f"Tämän hetkinen budjettisi on {budget}")
else:
    print("Vastasit väärin, oikea vastaus on A) vastaus.")
    print(f"Tämän hetkinen budjettisi on {budget}.")

#formerly in the game loop (eu part), removed since u can't win in the europe part of the game
if win:
    print(f'''You won!''')
    game_over = True

# if game is over loop stops
# show game result
print(f'''{'You won!' if win else 'You lost!'}''')