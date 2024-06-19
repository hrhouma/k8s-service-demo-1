from flask import Flask, Response, request
from redis import Redis
from datetime import datetime
import MySQLdb
import hashlib
import os

app = Flask(__name__)
startTime = datetime.now()
R_SERVER = redis.Redis(host=os.environ.get('REDIS_HOST', 'redis'), port=6379)

# Connexion à la base de données MySQL en utilisant les variables d'environnement
db = MySQLdb.connect(
    host=os.environ.get('MYSQL_HOST', 'mysql'),
    user=os.environ.get('MYSQL_USER', 'root'),
    passwd=os.environ.get('MYSQL_PASSWORD', 'root'),
    db=os.environ.get('MYSQL_DATABASE', 'userdb')
)
cursor = db.cursor()

@app.route('/init')
def init():
    cursor.execute("DROP DATABASE IF EXISTS USERDB")
    cursor.execute("CREATE DATABASE USERDB")
    cursor.execute("USE USERDB")
    sql = """CREATE TABLE users (
         ID int,
         USER char(30)
     )"""
    cursor.execute(sql)
    db.commit()
    return "DB Init done" 

@app.route("/users/add", methods=['POST'])
def add_users():
    req_json = request.get_json()   
    cursor.execute("INSERT INTO USERDB.users (ID, USER) VALUES (%s,%s)", (req_json['uid'], req_json['user']))
    db.commit()
    return Response("Added", status=200, mimetype='application/json')

@app.route('/users/<uid>')
def get_users(uid):
    hash = hashlib.sha224(str(uid).encode('utf-8')).hexdigest()
    key = "sql_cache:" + hash
    
    if R_SERVER.get(key):
        return R_SERVER.get(key).decode('utf-8') + "(c)"
    else:
        cursor.execute("select USER from USERDB.users where ID=" + str(uid))
        data = cursor.fetchone()
        if data:
            R_SERVER.set(key, data[0])
            R_SERVER.expire(key, 36)
            return R_SERVER.get(key).decode('utf-8')
        else:
            return "Record not found"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
