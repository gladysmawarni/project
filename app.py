from logging import setLogRecordFactory
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect
from helpers import login_required
from datetime import date, datetime
from sqlalchemy import asc
import os



app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False
app.config.update(SECRET_KEY=os.urandom(24))
app.config.from_object(__name__)
Session(app)


ENV = 'dev'

if ENV == 'dev':
    #development mode
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:gladysm123@localhost/project'
else:
    #production mode
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String(200))
    desc = db.Column(db.Text) 
    deadline = db.Column (db.Date)
    finished = db.Column(db.Boolean)
    datefinished = db.Column(db.Date)

    def __init__(self, user_id, title, desc, deadline, finished, datefinished):
        self.user_id = user_id
        self.title = title
        self.desc = desc
        self.deadline = deadline
        self.finished = finished
        self.datefinished = datefinished


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['id']
        password = request.form['pass']
        confirmation = request.form['conf']
        
        if not request.form['id'] or not request.form['pass'] or not request.form['conf']:
            return render_template('register.html', message='Please enter username and password')

        if password != confirmation:
            return render_template('register.html', message='Password does not match')
        
        user = Users.query.filter_by(username= username).first()
        
        if user:
            return render_template('register.html', message='Username already exists')
        
        new_user = Users(username= username, password= generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()


        return redirect('/')

    else:
        return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    session.clear()

    if request.method == 'POST':
        username = request.form['id']
        password = request.form['pass']

        if not request.form['id'] or not request.form['pass']:
            return render_template('login.html', message='Please enter username and password')
        
        user = Users.query.filter_by(username= username).first()

        if not user or not check_password_hash(user.password, password):
            return render_template('login.html', message='Invalid username and/or password')

        session['user'] = username
        session['user_id'] = user.id
 
        return redirect('/')
        
    else:
        return render_template('login.html')


@app.route('/', methods= ['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        currentTime = datetime.now()
        if currentTime.hour < 12:
            greeting ='Good morning,'
        elif 12 <= currentTime.hour < 18:
            greeting = 'Good afternoon,'
        else:
            greeting = 'Good evening,'


        user = Users.query.filter_by(username= session['user']).first()
        today = date.today()
        d1 = today.strftime("%B %d, %Y")

        current_user = session['user_id']
        title = request.form['title']
        desc = request.form['desc']
        deadline = request.form['deadline']

        new_entry = Entry(user_id= current_user, title= title, desc= desc, deadline= deadline, finished=False, datefinished= today)
        db.session.add(new_entry)
        db.session.commit()

        entries = Entry.query.filter_by(user_id= current_user).filter_by(finished= False).order_by(asc(Entry.deadline)).all()



        return render_template('index.html', user = user, date = d1, entries= entries, greeting= greeting)

    else:
        currentTime = datetime.now()
        if currentTime.hour < 12:
            greeting ='Good morning,'
        elif 12 <= currentTime.hour < 18:
            greeting = 'Good afternoon,'
        else:
            greeting = 'Good evening,'

        user = Users.query.filter_by(username= session['user']).first()
        today = date.today()
        d1 = today.strftime("%B %d, %Y")

        current_user = session['user_id']
        entries = Entry.query.filter_by(user_id= current_user).filter_by(finished= False).order_by(asc(Entry.deadline)).all()

        return render_template('index.html', user = user, date = d1, entries= entries, greeting= greeting)


@app.route('/finished/<mid>', methods= ['POST', 'GET'])
def delete_entry(mid):
    entries = Entry.query.filter_by(id= mid).first()
    datenow = date.today()

    if entries:
        entries.finished = True
        entries.datefinished = datenow
    
        new_entry = entries
        db.session.add(new_entry)
        db.session.commit()

    return redirect('/')

@app.route('/history')
@login_required
def history():
    currentTime = datetime.now()
    if currentTime.hour < 12:
        greeting ='Good morning,'
    elif 12 <= currentTime.hour < 18:
        greeting = 'Good afternoon,'
    else:
        greeting = 'Good evening,'

    user = Users.query.filter_by(username= session['user']).first()
    today = date.today()
    d1 = today.strftime("%B %d, %Y") 
    
    current_user = session['user_id']
    entries = Entry.query.filter_by(user_id= current_user).filter_by(finished= True).order_by(asc(Entry.datefinished)).all()

    return render_template('history.html', user = user, date = d1, entries= entries, greeting= greeting)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

 

if __name__ == '__main__':
    app.run()