from geopy import distance
import mysql.connector
import random

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
    sql = """SELECT country.name AS countryName, airport.iso_country, airport.ident, airport.name AS airportName, airport.latitude_deg, airport.longitude_deg, airport.type
        FROM country
        LEFT JOIN airport
        ON airport.iso_country = country.iso_country
        WHERE airport.continent = 'EU' 
        AND airport.type = 'large_airport'
        ORDER by RAND()
        LIMIT 3;"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

# starting airport
def get_airports_start():
    sql = """SELECT country.name AS countryName, airport.iso_country, airport.ident, airport.name AS airportName, airport.latitude_deg, airport.longitude_deg
        FROM country
        LEFT JOIN airport
        ON airport.iso_country = country.iso_country
        WHERE airport.ident = 'EFHK'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall() # pitääkö tässä olla fetchone fetchall:n tilalle? #keep as is
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
    sql = f'''SELECT country.name AS countryName, airport.iso_country, airport.ident, airport.name AS airportName, airport.latitude_deg, airport.longitude_deg
                  FROM country
                  LEFT JOIN airport
                  ON airport.iso_country = country.iso_country
                  WHERE airport.ident = %s'''
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

# hätälaskut
hatalasku_reason = ['lämpötila alle - 20', 'clear sky', 'lämpötila yli +25C',
                    'lämpotila alle 0C', 'säätila on tuulinen',
                    'Säätila on pilvinen', 'clear sky']

def country_hatalasku(maa):
    for i in range(1):
        reason_hatalasku = random.choice(hatalasku_reason)
        happening =maa+'ssa' + ' ' + reason_hatalasku.lower()
    if reason_hatalasku == 'clear sky':
        print('')
    else:
        print(f" {happening}, nyt tulee hätälasku!")

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
country_list = []
all_airports = get_airports_start()
start_airport = all_airports[0]['ident']
current_airport = start_airport
game_id = create_game(start_airport, player, all_airports)

# GAME LOOP

while not game_over:
    # get current airport info
    airport = get_airport_info(current_airport)
    # show current airport
    print(f'''Olet kohteessa {airport['airportName']}, {airport['countryName']}.''')
    # pause
    input('\033[32mPaina Enter jatkaaksesi...\033[0m')

    airports = get_airports()
    print(f'''Lentokentät: ''')
    for airport in airports:
        ap_distance = calculate_distance(current_airport, airport['ident'])
        print(f'''{airport['airportName']}, icao: {airport['ident']}, {airport['countryName']}, matkan pituus: {ap_distance:.0f}km''')
    # ask for destination
    dest = input('Kirjoita määränpään icao: ')
    if dest in country_list:
        print(f"Olet jo käynyt kohteessas {dest}. Valitse uusi kohde.")
        dest = input('Kirjoita määränpään icao: ')
    else:
        country_list.append(dest)
    # makes sure the input is valid
    while dest != airports[0]['ident'] and dest != airports[1]['ident'] and dest != airports[2]['ident']:
        print('Virheellinen syöte, kokeile uudestaan.')
        dest = input('Kirjoita määränpään icao: ')
        if dest in country_list:
            print(f"Olet jo käynyt kohteessa {dest}. Valitse uusi kohde.")
            dest = input('Kirjoita määränpään icao: ')
        else:
            country_list.append(dest)

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
        print("Saat passin. \nVoit suuntautua Euroopan ulkopuolelle.\n")
        break

#_______________________________________________________
# tästä alkaa euroopan jälkeinen osio
input('\033[32mPaina Enter jatkaaksesi...\033[0m')
# turkki
def get_airport1():
    sql = """SELECT country.name as countryName, airport.iso_country, airport.ident, airport.name as airportName, airport.latitude_deg, airport.longitude_deg
        FROM country
        LEFT join airport
        ON airport.iso_country = country.iso_country 
        WHERE airport.ident = 'LTAC'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

airport = get_airport_info(current_airport)
print(f'''Olet kohteessa {airport['airportName']}, {airport['countryName']}.''')

#turkin lentokenttä
airports = get_airport1()
print(f'''Seuraava kohteesi on: ''')
for airport in airports:
    ap_distance = calculate_distance(current_airport, airport['ident'])
    print(f'''{airport['airportName']}, {airport['countryName']}, matkan pituus: {ap_distance:.0f}km''')
dest = airport['ident']

selected_distance = calculate_distance(current_airport, dest)
update_location(dest, game_id)
current_airport = dest
#pause
input('\033[32mPaina Enter jatkaaksesi...\033[0m')

#hätälasku check
country_hatalasku("Turki")

#turkin kysymys
vastaus1 = input("Vaikuttaako lentäminen otsonikerrokseen? A) Ei vaikuta B) Vaikuttaa : ")
if vastaus1.upper() == "A":
    print("Vastasit oikein.")
    budget += 500
    print(f"Tämän hetkinen budjettisi on {budget}")
else:
    print("Vastasit väärin, oikea vastaus on A) Ei vaikuta.")
    budget = budget * 0.90
    print(f"Tämän hetkinen budjettisi on {budget}.")
input('\033[32mPaina Enter jatkaaksesi...\033[0m')

# Afganistan
def get_airport2():
    sql = """SELECT country.name as countryName, airport.iso_country, airport.ident, airport.name as airportName, airport.latitude_deg, airport.longitude_deg
        FROM country
        LEFT join airport
        ON airport.iso_country = country.iso_country 
        WHERE airport.ident = 'OAKB'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

airport = get_airport_info(current_airport)
print(f'''Olet kohteessa {airport['airportName']}, {airport['countryName']}.''')

# turkista afganistaniin
# afganistanin lentokenttä
airports = get_airport2()
print(f'''Seuraava kohteesi on: ''')
for airport in airports:
    ap_distance = calculate_distance(current_airport, airport['ident'])
    print(f'''{airport['airportName']}, {airport['countryName']}, matkan pituus: {ap_distance:.0f}km''')
dest = airport['ident']

selected_distance = calculate_distance(current_airport, dest)
update_location(dest, game_id)
current_airport = dest
input('\033[32mPaina Enter jatkaaksesi...\033[0m')

country_hatalasku("Afganistani")

# afganistanin kysymys
vastaus2 = input("Kuinka monta prosenttia maailman päästöistä syntyy lennoista? A) 15% B) 0,5-1% C) 2-3% : ")
if vastaus2.upper() == "C":
    print("Vastasit oikein.")
    budget += 500
    print(f"Tämän hetkinen budjettisi on {budget}.")
else:
    print("Vastasit väärin, oikea vastaus on C) 2-3%.")
    budget = budget * 0.90
    print(f'Tämän hetkinen budjettisi on {budget}.')
input('\033[32mPaina Enter jatkaaksesi...\033[0m')

# Japani
def get_airport3():
    sql = """SELECT country.name as countryName, airport.iso_country, airport.ident, airport.name as airportName, airport.latitude_deg, airport.longitude_deg
        FROM country
        LEFT join airport
        ON airport.iso_country = country.iso_country 
        WHERE airport.ident = 'RJAA'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

airport = get_airport_info(current_airport)
print(f'''Olet kohteessa {airport['airportName']}, {airport['countryName']}.''')

airports = get_airport3()
print(f'''Seuraava kohteesi on: ''')
for airport in airports:
    ap_distance = calculate_distance(current_airport, airport['ident'])
    print(f'''{airport['airportName']}, {airport['countryName']}, matkan pituus: {ap_distance:.0f}km''')
dest = airport['ident']

selected_distance = calculate_distance(current_airport, dest)
update_location(dest, game_id)
current_airport = dest
input('\033[32mPaina Enter jatkaaksesi...\033[0m')

country_hatalasku("Japani")

#japanin kysymys
vastaus3 = input("Mikä on yhden henkilön CO2-päästöt lentomatkalla Tokiosta Dubliniin? A) 1336.5kg B) 1335.6kg C) 1563.3kg : ")
if vastaus3.upper() == "B":
    print("Vastasit oikein.")
    budget += 500
    print(f"Tämän hetkinen budjettisi on {budget}")
else:
    print("Vastasit väärin, oikea vastaus on B) 1335.6kg.")
    budget = budget * 0.90
    print(f"Tämän hetkinen budjettisi on {budget}.")
input('\033[32mPaina Enter jatkaaksesi...\033[0m')

# yhdysvallat
def get_airport4():
    sql = """SELECT country.name as countryName, airport.iso_country, airport.ident, airport.name as airportName, airport.latitude_deg, airport.longitude_deg
        FROM country
        LEFT join airport
        ON airport.iso_country = country.iso_country 
        WHERE airport.ident = 'KBFI'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

airport = get_airport_info(current_airport)
print(f'''Olet kohteessa {airport['airportName']}, {airport['countryName']}.''')

airports = get_airport4()
print(f'''Seuraava kohteesi on: ''')
for airport in airports:
    ap_distance = calculate_distance(current_airport, airport['ident'])
    for country in airports:
        print(f'''{airport['airportName']}, {airport['countryName']}, matkan pituus: {ap_distance:.0f}km''')
dest = airport['ident']

selected_distance = calculate_distance(current_airport, dest)
update_location(dest, game_id)
current_airport = dest
input('\033[32mPaina Enter jatkaaksesi...\033[0m')

country_hatalasku("Yhdysvalloi")

#usan kysymys
vastaus4 = input("Kuinka paljon hiilidioksidia syntyy yhdestä kilosta kerosiinia polttaessa? A) 3.16kg B) 0.54kg C) 2.7kg : ")
if vastaus4.upper() == "A":
    print("Vastasit oikein.")
    budget += 500
    print(f"Tämän hetkinen budjettisi on {budget}")
else:
    print("Vastasit väärin, oikea vastaus on a) 3.16kg.")
    budget = budget * 0.90
    print(f"Tämän hetkinen budjettisi on {budget}.")
input('\033[32mPaina Enter jatkaaksesi...\033[0m')

# Kanada

def get_airport5():
    sql = """SELECT country.name as countryName, airport.iso_country, airport.ident, airport.name as airportName, airport.latitude_deg, airport.longitude_deg
        FROM country
        LEFT join airport
        ON airport.iso_country = country.iso_country 
        WHERE airport.ident = 'CYVR'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

airport = get_airport_info(current_airport)
# show game status
print(f'''Olet kohteessa {airport['airportName']}, {airport['countryName']}.''')

airports = get_airport5()
print(f'''Seuraava kohteesi on: ''')
for airport in airports:
    ap_distance = calculate_distance(current_airport, airport['ident'])
    print(f'''{airport['airportName']}, {airport['countryName']}, matkan pituus: {ap_distance:.0f}km''')
dest = airport['ident']

selected_distance = calculate_distance(current_airport, dest)
update_location(dest, game_id)
current_airport = dest
input('\033[32mPaina Enter jatkaaksesi...\033[0m')

country_hatalasku("Kanada")

# Kanadan kysymys
vastaus5 = input("Paljonko merenpinnan ennustetaan nousevan 2100-luvulle mennessä? A) 5km B) 1-1,5m C) 60-80cm : ")
if vastaus5.upper() == "C":
    print("Vastasit oikein.")
    budget += 500
    print(f"Tämän hetkinen budjettisi on {budget}")
else:
    print("Vastasit väärin, oikea vastaus on C) 60-80cm.")
    budget = budget * 0.90
    print(f"Tämän hetkinen budjettisi on {budget}.")
input('\033[32mPaina Enter jatkaaksesi...\033[0m')

#___________________________________________________________________

# Grönlanti
def get_airport6():
    sql = """SELECT country.name as countryName, airport.iso_country, airport.ident, airport.name as airportName, airport.latitude_deg, airport.longitude_deg
        FROM country
        LEFT join airport
        ON airport.iso_country = country.iso_country 
        WHERE airport.ident = 'BGJN'"""
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

airport = get_airport_info(current_airport)
print(f'''Olet kohteessa {airport['airportName']}, {airport['countryName']}.''')

airports = get_airport6()
print(f'''Seuraava kohteesi on: ''')
for airport in airports:
    ap_distance = calculate_distance(current_airport, airport['ident'])
    print(f'''{airport['airportName']}, {airport['countryName']}, matkan pituus: {ap_distance:.0f}km''')
dest = airport['ident']

selected_distance = calculate_distance(current_airport, dest)
update_location(dest, game_id)
current_airport = dest
input('\033[32mPaina Enter jatkaaksesi...\033[0m')

# Grönlannin kysymys
vastaus6 = input("Kuinka monen (prosentin) eurooppalaisen koti uhkaa jäädä merenpinnan alle 2100-luvulle mennessä? A) 5% B) 15% C) 30% : ")
if vastaus6.upper() == "C":
    print("Vastasit oikein.")
    win = True
else:
    print("Vastasit väärin, oikea vastaus on C) 30%.")

# show game result
print(f'''{f'Voitit pelin :) Lopullinen bubjettisi on {budget}' if win else f'Hävisit pelin :( Budjettisi on {budget}'}''')
