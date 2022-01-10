#from app import app
from flaskext.mysql import MySQL
from datetime import datetime
from flask import Flask
app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''
mysql.init_app(app)


def getUserIdByName(name):
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("""SELECT user_id FROM heroku_124a98971759b2a.users WHERE user_name = %s""",(name))
    user_id = cursor.fetchone()
    cursor.close()
    return user_id

def getUserData(name = None):
    "get data from users database (No devuelve contraseña)"
    conn = mysql.connect()
    cursor =conn.cursor()
    if name:
        cursor.execute("""SELECT user_name,user_id,mail,birth_date,favorite_programming_language FROM heroku_124a98971759b2a.users WHERE user_name = %s """,(name))
    else:
        cursor.execute("""SELECT user_name,user_id,mail,birth_date,favorite_programming_language FROM heroku_124a98971759b2a.users""")
    data = cursor.fetchall()
    cursor.close()
    if data:
        return data,200
    
    return data,204

def logDataIntoDB(timeOfLog,typeOfLog,user_id,token):
    conn = mysql.connect()
    cursor =conn.cursor()
    query = "call heroku_124a98971759b2a.logInfoToDB(%s,%s,%s,%s)"
    values = (timeOfLog,typeOfLog,user_id,token)
    cursor.execute(query,values)
    conn.commit()
    cursor.close()

#Used by jwt functions to only generate tokens when user + password is valid    
def getUserByCredentials(username,password):
    "Used by jwt functions to only generate tokens when user + password is valid"
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("""SELECT user_id FROM 
                    heroku_124a98971759b2a.users 
                    WHERE user_name = %s AND user_password = %s""",(username,password))
    data = cursor.fetchall()
    cursor.close()
    if data:
        return True    
    return False

def getLogHistory():
    "get log history"
    conn = mysql.connect()
    cursor =conn.cursor()
    cursor.execute("""SELECT * FROM heroku_124a98971759b2a.login_history""")
    data = cursor.fetchall()
    cursor.close()
    if data:
        return data,200
    return data,204

        
def getRepositoryById(repository_id=None):
    conn = mysql.connect()
    cursor =conn.cursor()
    if repository_id:
        cursor.execute("""SELECT * FROM heroku_124a98971759b2a.repository WHERE repository_id = %s """,(repository_id))
    else:
        cursor.execute("""SELECT * FROM heroku_124a98971759b2a.repository""")
    data = cursor.fetchall()
    cursor.close()
    if data:
        return data,200
    
    return data,204