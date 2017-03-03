# import urllib.request
# url=r'http://bulk.openweathermap.org/sample/city.list.json.gz'
# urllib.request.urlretrieve(url, 'city.list.json.gz')
#


import requests, os, gzip, json, datetime
path=os.path.join(os.getcwd(),'data')
os.chdir(path)
if not 'city.list.json.gz' in os.listdir():
    url = "http://bulk.openweathermap.org/sample/city.list.json.gz"
    r = requests.get(url)
    with open("city.list.json.gz", "wb") as handle:
        handle.write(r.content)

    file=os.path.join(os.getcwd(),'city.list.json.gz')
    with gzip.open(file,'rb') as f:
        city=f.read()
    with open('city.json','wb',) as f:
        f.write(city)

spisok=set()
with open('city.json', 'r', encoding='UTF-8') as f:
    for line in f:
        read_data = json.loads(line)
        spisok.add(read_data['country'])

def country(count):
    country=[]
    with open('city.json', 'r', encoding='UTF-8') as f:
        for line in f:
            read_data = json.loads(line)
            if read_data['country']==count:
                c=read_data['name']
                country.append(c)
    return country

def town(tow):
    with open('city.json', 'r', encoding='UTF-8') as f:
        for line in f:
            read_data = json.loads(line)
            if read_data['name']==tow:
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

# url='http://api.openweathermap.org/data/2.5/weather?id=511196&units=metric&appid=2dcdcf456f540b93ab78c43467e1a070'
r = requests.get(url)
page=(r.text)

# page={"coord":{"lon":56.29,"lat":58.02},
#       "weather":[{"id":804,"main":"Clouds","description":"overcast clouds","icon":"04d"}],
#       "base":"stations",
#       "main":{"temp":-1,"pressure":1017,"humidity":86,"temp_min":-1,"temp_max":-1},
#       "visibility":10000,"wind":{"speed":8,"deg":210},
#       "clouds":{"all":90},
#       "dt":1488537000,
#       "sys":{"type":1,"id":7312,"message":0.0032,"country":"RU","sunrise":1488510179,"sunset":1488549085},
#       "id":511196,
#       "name":"Perm",
#       "cod":200
#       }


id_town=page['id']
print(id_town)
name=page['name']
cur_date=page['dt']
cur_temp=(page['main']['temp'])
l1=page['weather']
l=l1[0]
id_weather=l['id']
a=(id_town,name,cur_date,cur_temp,id_weather)

import sqlite3,sys
con=sqlite3.connect('test.db')
with con:
    try:
        cur=con.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS weather( id_города INTEGER PRIMARY KEY, Город VARCHAR(255), Дата DATE, Температура INTEGER, id_погоды INTEGER )')
        cur.execute('INSERT INTO weather VALUES(?,?,?,?,?)',a)

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

