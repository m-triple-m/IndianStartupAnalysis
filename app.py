from flask import Flask, render_template, request, jsonify, redirect, session, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = "i don't have a secret!!"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(20), nullable = True)
    password = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return f'self.username, self.email, self.password'

class Record(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    product = db.Column(db.String(30), nullable = False)
    created = db.Column(db.String(20), nullable = True)
    pages = db.Column(db.String(30), nullable = False)
    data = db.Column(db.String(30), nullable = False)
    user = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return f'self.username, self.email, self.password'


db.create_all()

@app.route('/')
@app.route('/home')
def home():
    if not session.get('user'):
        return redirect('/signin')
    return render_template('home.html', loggedin = session.get('user'))

@app.route('/signin', methods = ["POST", "GET"])
def Signin():
    
    if request.method == 'POST':
        data = request.form
        
        user = User.query.filter_by(username = data.get('username')).first()
        if user:
            print(user)
            if user.password == data.get('password'):
                print('login success')
                session['user'] = user.username
                return jsonify('success')
                
            else:
                return jsonify('failed')
        else:
            return jsonify('failed')

    return render_template('signin.html')

@app.route('/signup', methods = ["POST", "GET"])
def Signup():
    if request.method == 'POST':
        data = request.form
        user = User(username = data.get('username'), email = data.get('email'), password = data.get('password'))
        db.session.add(user)
        db.session.commit()
        print('data saved!!')
        return jsonify('success')

    return render_template('signup.html')

@app.route('/logout')
def Logout():
    session['user'] = None
    return redirect('/signin')


@app.route('/report')
def report():
    data = Record.query.all()
    return render_template('report.html', data = data, loggedin = session.get('user'))


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    if not session.get('user'):
        return redirect('/login')
    return send_file(filename_or_fp=f'csvfiles/{filename}')

@app.route('/visualize')
def Visualize():
    return render_template('visualize.html')

@app.route('/wordcloud')
def Wordcloud():
    return render_template('wordcloud.html')

if __name__ == "__main__":
    app.run(debug=True)