# testing zone or something idk lol
# muistiinpanot ?

# turkki - ankara (LTAC), afganistan - kabul (OAKB), japani - tokyo (RJAA)
# yhdysvallat - seattle (KBFI), kanada - vancouver (CYVR), grönlanti - ilulissat (BGJN)
# muistiinpanot ?

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
