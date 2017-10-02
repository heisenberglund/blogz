from flask import Flask, request, render_template
import os
from cgi import escape''
from signup.py import user_signup


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route('/signup', methods=['POST'])
def signup():

@app.route('/', methods=['POST'])
def index():

app.run()