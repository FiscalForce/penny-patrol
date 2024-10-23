from flask import Flask, render_template, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "12345"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Arun@123' 
app.config['MYSQL_DB'] = 'penny_patrol'


# Intialize MySQL
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/groups')
def home():
    return render_template('groups.html')



if __name__ =='__main__':
	app.run(debug=True)
