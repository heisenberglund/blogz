from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'ryd4docv549sdlf'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5000))
    completed = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(120))

    def __init__(self, name, owner, title):
        self.name = name
        self.completed = False
        self.owner = owner
        self.title = title
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blog_owner = db.relationship('Blog', backref='owner')

    def __init__(self, name, user):
        self.name = name
        self.user = user

@app.before_request
def require_login():
    allowed_routes = ['login','register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            return "<h1>Duplicate user</h1>"

    return render_template('register.html')

@app.route('/', methods=['POST','GET'])
def index():
    
    owner = User.query.filter_by(email=session['email']).first()

    if request.method == 'POST':
        task_name = request.form['task']
        title = request.form['title']

        new_task = Blog(task_name, owner, title)
        db.session.add(new_task, title)
        db.session.commit()

    tasks = Blog.query.filter_by(completed=False,owner=owner).all()
    completed_tasks = Blog.query.filter_by(completed=True,owner=owner).all()
    return render_template('blog.html',title="BLOGZILLA", 
        tasks=tasks, completed_tasks=completed_tasks)

@app.route('/display', methods=['POST', 'GET'])
def blog_page():

    blogs = Blog.query.all()
 
    return render_template('display.html', blogs=blogs)


@app.route('/logout')
def logout():
    del session['email']
    return redirect('/')

if __name__ == '__main__':
    app.run()