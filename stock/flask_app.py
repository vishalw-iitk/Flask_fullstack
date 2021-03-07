from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from train import process
from os import environ

from tkinter import *
from datetime import *
from threading import *



app = Flask(__name__)

cors = CORS(app)


app.config['MYSQL_HOST'] =  environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = environ.get('MYSQL_DB')

db_connection_str = 'mysql+pymysql://'+str(environ.get('MYSQL_USER'))+':'+str(environ.get('MYSQL_PASSWORD'))+'@'+str(environ.get('MYSQL_HOST'))+'/'+str(environ.get('MYSQL_DB'))
db_connection = create_engine(db_connection_str)

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, email) VALUES (%s, %s)", (username, email))
        mysql.connection.commit()
        cur.close()
        return "success"
    # return render_template('index.html')
    return "success"

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    users = cur.execute("SELECT * FROM stock_table")
    
    # users = cur.execute("SELECT * FROM users")
    if users > 0:
        userDetails = cur.fetchall()
        # print(userDetails)
        # return render_template('users.html', userDetails=userDetails)
        return {"data":userDetails}
        # return "ttt"

@app.route('/put_to_sql') #read data from csv and put to SQL
def put_sql():
    df = pd.read_csv('GE.csv')
    df.to_sql(con=db_connection, name='stock_table', if_exists='replace')
    return "put to sql"

@app.route('/process')
def get_sql():
    df = pd.read_sql('SELECT * FROM stock_table', con=db_connection)
    df.drop(columns=['index'], inplace=True)
    
    print(df.columns)
    l = process(df, db_connection)
    # print("ppppppppppppppppppp")
    return l



if __name__ == "__main__":
    app.run(debug=True)
