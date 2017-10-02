from flask import Flask, request, render_template
import os
from cgi import escape
from signup.py import user_signup
from main import db, Blog
db.create_all()
db.session.commit()


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/signup', methods=['POST'])
def signup():
    
@app.route('/blog', methods=['POST'])
def blog():
    
@app.route('/newpost', methods=['POST'])
def newpost():

@app.route('/', methods=['POST'])
def index():

app.run()