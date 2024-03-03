import pandas as pd
import numpy as np
from flask import Flask, request, render_template, redirect, url_for, session, flash
import mysql.connector
import warnings
import  re
from datetime import date
import datetime
from datetime import timedelta, date
import smtplib
from email.message import Message
from email.mime.text import MIMEText
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)
app.secret_key = 'your secret key'

#database connection
mydb = mysql.connector.connect(
  host="localhost",
  port=3306,
  user="root",
  password="",
  database='clinic_management_system'
)
print(mydb)
mycursor = mydb.cursor()


# mycursor.execute("CREATE TABLE IF NOT EXISTS Patient_Master (p_id int(11) NOT NULL AUTO_INCREMENT, username VARCHAR(50), fullname VARCHAR(255), mobileno VARCHAR(50), emailid VARCHAR(255), password VARCHAR(100), PRIMARY KEY (p_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS Booked_Appointment (a_id int(11) NOT NULL AUTO_INCREMENT, p_id int(11), fullname VARCHAR(255), age int, gender VARCHAR(50), mobileno VARCHAR(15), a_date VARCHAR(25), a_time VARCHAR(100), a_status VARCHAR(100), PRIMARY KEY (a_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS Doctor_Prescription (dp_id int(11) NOT NULL AUTO_INCREMENT, a_id int(11),  p_id int(11), symptoms VARCHAR(100), prescription LONGTEXT, PRIMARY KEY (dp_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS Feedback_m (fb_id int(11) NOT NULL AUTO_INCREMENT,  p_id int(11), feedback_message LONGTEXT, f_date VARCHAR(25), PRIMARY KEY (fb_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS Admin_Master (admin_id int(11) NOT NULL AUTO_INCREMENT,  username VARCHAR(50), password VARCHAR(100), PRIMARY KEY (admin_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS Time_Master (t_id int(11) NOT NULL AUTO_INCREMENT,  Timing VARCHAR(255), PRIMARY KEY (t_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS Dr_Unavailability (uav_id int(11) NOT NULL AUTO_INCREMENT,  unavail_date VARCHAR(25), PRIMARY KEY (uav_id))")
# mycursor.execute("CREATE TABLE IF NOT EXISTS Email_Reminder (er_id int(11) NOT NULL AUTO_INCREMENT,  email_date VARCHAR(25), PRIMARY KEY (er_id))")


#create table function:
#create_tables(mycursor)

mycursor = mydb.cursor(dictionary=True)

#flask code
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'pass' in request.form:
        username = request.form['username']
        password = request.form['pass']
        sql="SELECT * FROM Patient_Master WHERE username = %s AND password = %s"
        mycursor.execute(sql,(username, password, ))
        userdata = mycursor.fetchone()
        if userdata:
            session['loggedin'] = True
            session['p_id'] = userdata['p_id']
            session['username'] = userdata['username']
            msg = session['username']
            return redirect(url_for('index'))
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
        
    return render_template('signin.html', msg = msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('p_id', None)
    session.pop('username', None)
    return redirect(url_for('signin'))


@app.route('/signup')
def signup():
    return redirect(url_for('register'))


@app.route('/signin')
def signin():
    return redirect(url_for('login'))


@app.route('/index', methods =['GET'])
def index(): 
    if 'username' not in session.keys():
        return redirect(url_for('login'))
    else:
        msg = session['username']
        return render_template('index.html',msg = msg)


@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'pass' in request.form and 'emailid' in request.form and 'fullname' in request.form and 'mobileno' in request.form :
        username = request.form['username']
        password = request.form['pass']
        emailid = request.form['emailid']
        fullname = request.form['fullname']
        mobileno = request.form['mobileno']
        mycursor = mydb.cursor(dictionary=True)
        sql="SELECT * FROM Patient_Master WHERE username = %s"
        mycursor.execute(sql, (username, ))
        userdata = mycursor.fetchone()
        if userdata:
            msg = 'User already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailid):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not emailid or not fullname or not mobileno:
            msg = 'Please fill out the details properly !'
        else:
            sql="INSERT INTO Patient_Master VALUES (NULL, %s, %s, %s, %s, %s)"
            mycursor.execute(sql, (username, fullname, mobileno, emailid, password, ))
            mydb.commit()
            msg = 'You have successfully registered !'

    elif request.method == 'POST':
        msg = 'Please fill out the details !'
    return render_template('signup.html', msg = msg)




if __name__ == '__main__':
    # Run the application
    app.run(debug=False)




