import requests, os, gzip, json
from datetime import datetime
path = os.path.join(os.getcwd(), 'data')
os.chdir(path)
if not 'city.list.json.gz' in os.listdir():
    url = "http://bulk.openweathermap.org/sample/city.list.json.gz"
    r = requests.get(url)
    with open("city.list.json.gz", "wb") as handle:
        handle.write(r.content)

    file = os.path.join(os.getcwd(), 'city.list.json.gz')
    with gzip.open(file, 'rb') as f:
        city = f.read()
    with open('city.json', 'wb',) as f:
        f.write(city)

spisok = set()
with open('city.json', 'r', encoding='UTF-8') as f:
    for line in f:
        read_data = json.loads(line)
        spisok.add(read_data['country'])


def country(count):
    country = []
    with open('city.json', 'r', encoding='UTF-8') as f:
        for line in f:
            read_data = json.loads(line)
            if read_data['country'] == count:
                c = read_data['name']
                country.append(c)
    return country


def town(tow):
    with open('city.json', 'r', encoding='UTF-8') as f:
        for line in f:
            read_data = json.loads(line)
            if read_data['name'] == tow:
                t=read_data['_id']
        return t

print('список стран', spisok)
count=input('выберите страну ')
print(country(count))

tow=input('укажите город ')
id_town=town(tow)
print('ID города=',id_town)

appid='2dcdcf456f540b93ab78c43467e1a070'
url='http://api.openweathermap.org/data/2.5/weather?id='+str(id_town)+'&units=metric&appid='+appid
r = requests.get(url)
with open('town.json', 'wb') as handle:
    handle.write(r.content)

with open('town.json','r', encoding='UTF-8') as f:
    read_data=json.load(f)

id_town=read_data['id']
name = read_data['name']
date1 = read_data['dt']
date2 = datetime.date(datetime.fromtimestamp(date1))
cur_date = str(date2)
cur_temp = (read_data['main']['temp'])
l1 = read_data['weather']
l = l1[0]
id_weather = l['id']
a = (id_town, name, cur_date, cur_temp, id_weather)

import sqlite3, sys
con = sqlite3.connect('test.db')

with con:
    try:
        cur=con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS weather(id_города INTEGER PRIMARY KEY, Город VARCHAR(255), Дата DATE, Температура INTEGER, id_погоды INTEGER )')
        cur.execute('SELECT * from weather')
        sel=cur.fetchone()
        if sel!= None and sel[0]==id_town:
            cur.execute('UPDATE weather  SET Дата = ?  where id_города = ?',(cur_date, id_town))
            cur.execute('UPDATE weather  SET Температура = ?  where id_города = ?', (cur_temp, id_town))
            cur.execute('UPDATE weather  SET id_погоды = ?  where id_города = ?', (id_weather, id_town))

        else:
            cur.execute('INSERT INTO weather VALUES(?,?,?,?,?)',a)
        cur.execute('SELECT * FROM weather')
        print(cur.fetchall())

        #добавление всех городов в базу
        # with open('city.json', 'r', encoding='UTF-8') as f:
        #     for line in f:
        #         read_data = json.loads(line)
        #         a=(read_data['_id'],read_data['name'])
        #
        #         try:
        #             cur.execute('INSERT INTO weather VALUES(?,?,NULL,NULL,NULL)',a)
        #         except sqlite3.Error as e:
        #             pass




    except sqlite3.Error as e:
        print("Error %s:" % e.args[0])
        sys.exit(1)

