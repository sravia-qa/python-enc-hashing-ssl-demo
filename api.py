from flask import Flask
from flask import request
import bcrypt
from cryptography.fernet import Fernet
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
        #Get salt for this username
        mycursor = mydb.cursor()
        sql = "SELECT usalt from secureusers WHERE uname = '"+uname+"'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            return "incorrect username or password"
        mysalt = myresult[0][0]
        
        #hash password
        
        myencodedhash = bcrypt.hashpw(upass.encode('utf-8'), mysalt.encode("utf-8"))
        myhash = myencodedhash.decode("utf-8")
        

        sql = "select usecret, ukey from secureusers WHERE uname ='"+uname+"' AND upass ='" + myhash + "'" 
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if len(myresult) == 0:
            return "incorrect username or password"
        scrt = myresult[0][0]
        mykey = myresult[0][1]
        # decrypt secret
        decryptor = Fernet(mykey)
        dec_usecret = decryptor.decrypt(scrt)
        dec_usecret = dec_usecret.decode('utf-8')
        return dec_usecret

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
        #encrypt secret
        mykey = Fernet.generate_key()
        encryptor = Fernet(mykey)
        enc_usecret = encryptor.encrypt(usecret.encode())
        
        # hash pass
        byt = upass.encode('utf-8')
        mysalt = bcrypt.gensalt()
        myhash = bcrypt.hashpw(byt, mysalt)

        
        mycursor = mydb.cursor()
        sql = "INSERT into secureusers (uname, upass, usecret, ukey, usalt ) VALUES (%s, %s, %s, %s, %s)"
        #replace with correct encrypted and hashed values
        val = (uname, myhash, enc_usecret, mykey, mysalt)
        mycursor.execute(sql, val)
        mydb.commit()
        if mycursor.rowcount == 1:
            return "User Successfully Created"
        else:
            return "there was a problem creating user, try again after sometime"

        
app.run('0.0.0.0')
