from flask import Flask
from flask import request
app = Flask(__name__)
import mysql.connector
mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="yankeeD00dle!",
        database="sitedb"
        )
@app.route("/", methods = ['GET', 'POST'])
def home():
    if request.method == 'GET':
        f = open("home.html", 'r')
        c = f.read()
        f.close()
        return c
    if request.method == 'POST':
        uname = request.form['uname']
        upass = request.form['upass']
        mycursor = mydb.cursor()
        sql = "select * from users WHERE uname ='"+uname+"' AND upass ='" + upass + "'" 
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            return "user doesn't exist"
        user = myresult[0]
        return user[2]

@app.route("/newuser", methods = ['GET', 'POST'])
def createUser():
    if request.method == 'GET':
        f = open("create.html", 'r')
        c = f.read()
        f.close()
        return c
    if request.method == 'POST':
       uname = request.form['uname']
        upass = request.form['upass']
        usecret = request.form['usecret']
        mycursor = mydb.cursor()
        sql = "INSERT into users (uname, upass, usecret) VALUES (%s, %s, %s)"
        val = (uname, upass, usecret)
        mycursor.execute(sql, val)
        mydb.commit()
        if mycursor.rowcount == 1:
            return "User Successfully Created"
        else:
            return "there was a problem creating user, try again after sometime"

        
app.run('0.0.0.0')
