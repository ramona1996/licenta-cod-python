#!/usr/bin/python

import _thread
import http.server
import json
import socketserver
import sqlite3
import time
from datetime import datetime
from random import randrange
import Adafruit_DHT

DHT_SENSOR=Adafruit_DHT.DHT22
DHT_PIN1 = 18
DHT_PIN2 = 17

# portul la care va rula serverul
PORT = 80
REFRESH_TIME_IN_SECONDS=4

# query creare tabela de valori
sql_create_valori_table = """ CREATE TABLE IF NOT EXISTS valori (
                                        id INTEGER PRIMARY KEY,
                                        tip_senzor text NOT NULL,
                                        valoare text NOT NULL,
                                        data text
                                    ); """


s1h = 0
s2h = 0
s1t = 0
s2t = 0

cs1h = 0
cs2h = 0
cs1t = 0
cs2t = 0

#functia de citire senzor
def read_sensor():
    global s1h
    global s2h
    global s1t
    global s2t
    while True:
        ts1h, ts1t = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN1)
        ts2h, ts2t = Adafruit_DHT.read_retry(DHT_SENSOR,17)
        cs1h = int(ts1h)
        cs1t = int(ts1t)
        cs2h = int(ts2h)
        cs2t = int(ts2t)
        if cs1h != s1h or cs1t != s1t or cs2h != s2h or cs2t != s2t:
            s1h = cs1h
            s1t = cs1t
            s2h = cs2h
            s2t = cs2t
            save_data(s1h, s2h, s1t, s2t)
            print("dummy sensor new data at " + str(datetime.now()))
        time.sleep(REFRESH_TIME_IN_SECONDS)


# creare conexiune la baza de date
def get_new_connection():
    return sqlite3.connect("sql_lite.db")

# executa un query la o conexiune catre o baza de date
def connection_execute(conn, create_table_sql):
    c = conn.cursor()
    c.execute(create_table_sql)
    c.close()

#numara inregistrarile dintr-o tabela
def count_rows(conn, table):
    c = conn.cursor();
    c.execute("SELECT * FROM " + table)
    results = c.fetchall()
    rows = len(results)
    c.close()
    return rows

def date_to_string(date):
    return date.strftime('%Y-%m-%d %H:%M:%S')

def save_data(ps1h, ps2h, ps1t, ps2t):
    global inregistrari
    now = date_to_string(datetime.now());
    try:
        local_connection = get_new_connection()
        c = local_connection.cursor()
        c.execute( "INSERT INTO valori (tip_senzor, valoare, data) VALUES (?, ?, ?)", ('s1h', ps1h, now))
        c.execute( "INSERT INTO valori (tip_senzor, valoare, data) VALUES (?, ?, ?)", ('s2h', ps2h, now))
        c.execute( "INSERT INTO valori (tip_senzor, valoare, data) VALUES (?, ?, ?)", ('s1t', ps1t, now))
        c.execute( "INSERT INTO valori (tip_senzor, valoare, data) VALUES (?, ?, ?)", ('s2t', ps2t, now))
        c.close()
        local_connection.commit()
        local_connection.close()
        inregistrari += 4
        print("saved at  = " + now + " >>" + str(inregistrari) + " inregistrari")
    except:
        print(now + " failed to store data")


def get_data():
    res = []
    try:
        local_connection = get_new_connection()
        c = local_connection.cursor()
        c.execute("SELECT * FROM valori ORDER BY data")
        rows = c.fetchall()
        for row in rows:
            res.append(row)
        c.close()
        local_connection.close()
    except:
        print("get_data failed")
    return res




#creare baza de date daca nu exista
connection = get_new_connection()

# creare tabela
connection_execute(connection, sql_create_valori_table)

# stabilire numar de inregistrari initial si afisare
inregistrari = count_rows(connection, "valori")
print(str(inregistrari) + " inregistrari existente")
connection.commit()

# inchidere conexiune la baza de date
connection.close()

#clasa handler pentru request-urile de la severul web
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.serveContent();

    def serveContent(self):
        if self.path == '/dataset':
            self.serveFile("application/json", "dataset.json")
        elif self.path == '/history':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(get_data()).encode())
            # self.wfile.write("{}".encode())
        elif self.path == '/sensors':
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write( ('{ '
                             '"sensors": {'
                                 '"s1h": ' + str(s1h) + ','
                                 '"s2h": ' + str(s2h) + ','
                                 '"s1t": ' + str(s1t) + ','
                                 '"s2t": ' + str(s2t) + ','
                                 '"date": \"' + date_to_string(datetime.now()) + '\"'
                             '}}').encode())
        else:
            self.serveFile("text/html", "main.html")

    def serveFile(self, content_type, path):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        with open(path, 'rb') as file:
            self.wfile.write(file.read())

#pornire thread de citire senzor
_thread.start_new_thread(read_sensor, ())

#pornire server web
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
