import sqlite3
import DEFINE
sqlite_file = str(DEFINE.DB_NAME)+".sqlite"

def init_db():
	
    # Get a cursor object
    db = sqlite3.connect(sqlite_file)
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE sensors_values(id INTEGER PRIMARY KEY AUTOINCREMENT , timestamp TEXT,
	CH4 TEXT, LPG TEXT , CO2 TEXT, Dust TEXT, Temperature TEXT, Humidity TEXT, Lat TEXT, Long TEXT)
	''')
    db.commit()


def insert_in_db(ts, ch4, lpg, co2, dust, tmp, hum, lat, lng):
	
    db = sqlite3.connect(sqlite_file)
    c= db.cursor()
    c.execute('''INSERT INTO sensors_values(timestamp, CH4, LPG, CO2, Dust, Temperature, Humidity, Lat, Long)
    VALUES(?,?,?,?,?,?,?,?,?)''', (ts,ch4,lpg,co2,dust,tmp,hum,lat,lng))
    db.commit()




#init_db()
