from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config
import MySQLdb.cursors
from werkzeug.security import check_password_hash
app = Flask(__name__)

app.config.from_object(Config)
mysql = MySQL(app)
class Bank:
    def __init__(self, code, name, city, address):
        self.code = code
        self.name = name
        self.city = city
        self.address = address

    @classmethod
    def create(cls, name, city, address):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO BANK (BANK_NAME, CITY, ADDRESS) VALUES (%s, %s, %s)", (name, city, address))
        mysql.connection.commit()
        cur.close()

    @classmethod
    def read(cls, code):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM BANK WHERE CODE = %s", [code])
        bank_data = cur.fetchone()
        cur.close()
        return bank_data

    @classmethod
    def update(cls, code, name, city, address):
        cur = mysql.connection.cursor()
        cur.execute("UPDATE BANK SET BANK_NAME=%s, CITY=%s, ADDRESS=%s WHERE CODE=%s", (name, city, address, code))
        mysql.connection.commit()
        cur.close()

    @classmethod
    def delete(cls, code):
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM BANK WHERE CODE = %s", [code])
        mysql.connection.commit()
        cur.close()
