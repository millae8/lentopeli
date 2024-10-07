# testing zone or something idk lol
# muistiinpanot ?

# turkki - ankara (LTAC), afganistan - kabul (OAKB), japani - tokyo (RJAA)
# yhdysvallat - seattle (KBFI), kanada - vancouver (CYVR), grönlanti - ilulissat (BGJN)

# sain tehtyy sql joka näyttää maan nimi lentokentän tietojen mukaan, 
# mutta jossain puuttuu se, että maan nimi näkyy, koska se herjaa mulla, kun yritän saada maan nimi näkymään pelissä.
# maan nimi näkyy nyt

# FOR DATABASE TABLE "task"
'''
create table task(
id int not null auto_increment,
question varchar (40),
display_answer varchar (40),
correct_answer varchar (40),
primary key(id)
);
'''

# hakee kysymyksiä randomisti 1 kpl
def get_question():
    sql = (f"select question,answer from task order by rand() limit 1")
    #print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    result_row = cursor.fetchone()
    # palauttaa monikon, paitsi jos tyhjä tulosjoukko -> tulostaa None
    return result_row

print('peli alkaa, kysyn ekan kysymyksen')

kysymys, oikea_vastaus = get_question()
vastaus = input(f'{kysymys}: ')
print(f'vastasit {vastaus}')
print(f'Oikea vastaus on {oikea_vastaus}')
____________________________________________________________

# arpoo 3 lentokenttää euroopassa (for now monikko muotona) en oo varma tästä koodista
def get_airplane():
    sql = (f"select name, from airport, country where continent = 'EU' order by rand() limit 3;")
    #print(sql)
    cursor = connection.cursor(dictionary=True) # ??
    cursor.execute(sql)
    result_row = cursor.fetchall()
    return result_row

place = get_airplane()
print(place)

# ehkä voidaan lisätä tää for loop, jotta ne lentokenttien tiedot näkyy paremmin (?)      # jep
for i in get_airports():
    print(i)

# tässä hätälasku kohta

maa_list = ['Turkki', 'Afganistan', 'Japani', 'Yhdysvallat', 'Canada']

hatalasku_reason = ['lämpötila alle - 20', 'clear skys', 'lämpötila yli +25C',
                    'lämpotila alle 0C', 'säätila on tuulinen',
                    'Säätila on pilvinen', 'clear skys']

#def country_hatalasku():
for i in range(1):
    maa = random.choice(maa_list)
    reason_hatalasku = random.choice(hatalasku_reason)
    happening = maa.capitalize() +'ssa' + ' ' + reason_hatalasku.lower()
if reason_hatalasku == 'clear skys':
    print('')
else:
    print(f" {happening}, nyt tulee hätälasku!") # en tiiä kirjoitinko tän oikein


_______________________________________________________________________________________________________________________________________________-


# testasin peliä ja tässä on miltä se koko homma toimi (kun kaikki on vastattu oikein ja päästöjä ei ole kulunu yhtään)

Kun olet valmis aloittamaan, 
kirjoita pelaajan nimi: don
Olet kohteessa Helsinki Vantaa Airport, Finland.
Paina Enter jatkaaksesi...
Lentokentät: 
Olenya Air Base, icao: RU-4464, Russia, matkan pituus: 964km
Shannon Airport, icao: EINN, Ireland, matkan pituus: 2221km
Billund Airport, icao: EKBI, Denmark, matkan pituus: 1060km
Kirjoita määränpään icao: EINN
Mitkä ovat tärkeimmät pölyttäjät? a. muurahaiset ja ampiaiset b. kimalaiset ja mehiläiset  c. perhoset ja kärpäset: b
Oikein. Saat leiman.
Olet kohteessa Shannon Airport, Ireland.
Paina Enter jatkaaksesi...
Lentokentät: 
Marseille Provence Airport, icao: LFML, France, matkan pituus: 1469km
Verona Villafranca Airport, icao: LIPX, Italy, matkan pituus: 1653km
Helsinki Vantaa Airport, icao: EFHK, Finland, matkan pituus: 2221km
Kirjoita määränpään icao: EFHK
Missä Suomen kaupungissa oli puhtain ilma vuonna 2023? a. Kaarina b. Kouvola c. Kuusamo: c
Oikein. Saat leiman.
Olet kohteessa Helsinki Vantaa Airport, Finland.
Paina Enter jatkaaksesi...
Lentokentät: 
Shannon Airport, icao: EINN, Ireland, matkan pituus: 2221km
Václav Havel Airport Prague, icao: LKPR, Czech Republic, matkan pituus: 1322km
London Luton Airport, icao: EGGW, United Kingdom, matkan pituus: 1819km
Kirjoita määränpään icao: EINN
Olet jo käynyt kohteessa EINN. Valitse uusi kohde.
Kirjoita määränpään icao: LKPR
Kuinka monta prosenttia viljelykasveista tarvitsee hyönteispölytystä? a. noin 75% b. noin 85% c. 65%: a
Oikein. Saat leiman.
Olet kerännyt tarvittavan määrän leimoja.
Saat passin. 
Voit suuntautua Euroopan ulkopuolelle.

Paina Enter jatkaaksesi...

Olet kohteessa Václav Havel Airport Prague, Czech Republic.
Seuraava kohteesi on: 
Esenbo?a International Airport, Turkey, matkan pituus: 1836km
Paina Enter jatkaaksesi...Vaikuttaako lentäminen otsonikerrokseen? A) Ei vaikuta B) Vaikuttaa : a
Vastasit oikein.
Tämän hetkinen budjettisi on 6500
Paina Enter jatkaaksesi...
Olet kohteessa Esenbo?a International Airport, Turkey.
Seuraava kohteesi on: 
Kabul International Airport, Afghanistan, matkan pituus: 3245km
Paina Enter jatkaaksesi...
Kuinka monta prosenttia maailman päästöistä syntyy lennoista? A) 15% B) 0,5-1% C) 2-3% : c
Vastasit oikein.
Tämän hetkinen budjettisi on 7000.
Paina Enter jatkaaksesi...
Olet kohteessa Kabul International Airport, Afghanistan.
Seuraava kohteesi on: 
Narita International Airport, Japan, matkan pituus: 6333km
Paina Enter jatkaaksesi...
Mikä on yhden henkilön CO2-päästöt lentomatkalla Tokiosta Dubliniin? A) 1336.5kg B) 1335.6kg B) 1563.3kg : b
Vastasit oikein.
Tämän hetkinen budjettisi on 7500
Paina Enter jatkaaksesi...
Olet kohteessa Narita International Airport, Japan.
Seuraava kohteesi on: 
Boeing Field King County International A, United States, matkan pituus: 7671km
Paina Enter jatkaaksesi...
Kuinka paljon hiilidioksidia syntyy yhdestä kilosta kerosiinia polttaessa? A) 3.16kg B) 0.54kg C) 2.7kg : a
Vastasit oikein.
Tämän hetkinen budjettisi on 8000
Paina Enter jatkaaksesi...
Olet kohteessa Boeing Field King County International A, United States.
Seuraava kohteesi on: 
Vancouver International Airport, Canada, matkan pituus: 196km
Paina Enter jatkaaksesi...
Paljonko merenpinnan ennustetaan nousevan 2100-luvulle mennessä? A) 5km B) 1-1,5m C) 60-80cm : c
Vastasit oikein.
Tämän hetkinen budjettisi on 8500
Paina Enter jatkaaksesi...
Olet kohteessa Vancouver International Airport, Canada.
Seuraava kohteesi on: 
Ilulissat Airport, Greenland, matkan pituus: 4332km
Paina Enter jatkaaksesi...
Kuinka monen (prosentin) eurooppalaisen koti uhkaa jäädä merenpinnan alle 2100-luvulle mennessä? A) 5% B) 15% C) 30% : c
Vastasit oikein.
Voitit pelin :) Lopullinen bubjettisi on 8500

