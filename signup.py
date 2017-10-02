from flask import Flask, request, redirect, render_template
import os
from cgi import escape

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['POST'])
def user_signup():
    user = request.form['user-name']
    password = request.form['password']
    vpass = request.form['vpass']
    email = request.form['email']
    name_err = ''
    password_err = ''
    vpass_err = ''
    email_err = ''


    if len(user) > 20 or len(user) < 3:
        name_err = 'Your user name does not fit the parameters'
        user = ''
    
    if len(password) > 20 or len(password) < 3:
        password_err =  'Your password does not fit the parameters'
        password = ''

    if len(vpass) > 20 or len(vpass) < 3:
        vpass_err = 'Your verification does not fit the parameters'
        vpass = ''
    
    if password != vpass:
        vpass_err = 'Your password and verification do not match'
        vpass = ''

    if email != '':
        if '@' not in email or '.' not in email or ' ' in email or len(email) <3 or len(email) >20:
            email_err = 'Invalid email' 
            email = ''
    
    if not name_err and not password_err and not vpass_err and not email_err:
        return render_template('welcome.html', user=user) 
          

    else:
        return render_template('index.html', user=user, name_err=name_err,
        password=password, password_err=password_err,
        vpass=vpass, vpass_err=vpass_err, 
        email=email, email_err=email_err)


@app.route('/')
def index():
    return render_template('index.html')
