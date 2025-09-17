#!/usr/bin/env python3
# -- coding: utf-8
'''
Flask login and Quiz web application
------------------------------------
This project is a simple flask application where users can:
- login  with a username,password
-register with a username, email, password
- it saves the details in text file
- take a multiple-choice quiz after logging in or registing
-view their results at the end

The sytem uses password hashing for better security,
Developed as a group project by
[DECISIVE INNOVATORS]
'''

from flask import Flask,render_template,request,redirect,url_for
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

questions = [
    {'question': 'What is the result of 3**2 in python?', 
     'options':{
         'A':'6',
         'B':'9', 
         'C':'8', 
         'D':'5'
         } ,
     'answer': 'B'
    },
    {'question': 'which people developed python?',
     'options': {
         'A':'Guido Van Rossum',
         'B':'Mark Zuckerberg',
         'C':'James Gosling',
         'D':'Charles Babbage'
         },
     'answer': 'A'
     },
    {'question': 'What is the result of "hello.upper()"?',
     'options': {
         'A':'HELLO',
         'B':'Hello',
         'C':'hello',
         'D':'Error'
         },
     'answer': 'A'
     },
     {'question': 'which of the following is NOT a programming paradigm?',
     'options': {
         'A':'Object-Oriented',
         'B':'Functional ',
         'C':'Procedural',
         'D':'Graphical'
         },
     'answer': 'D'
     },
         {'question': 'which of the following is a compiled language?',
     'options': {
         'A':'Python',
         'B':'JavaScript',
         'C':'C++',
         'D':'Ruby'
         },
     'answer': 'C'
     }

     ]


@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])   
def login():
    username = request.form['username'] 
    password = request.form['password']          

    if os.path.exists('infor.txt'):
        with open('infor.txt','r') as f:
            for line in f:
                creds = line.strip().split(',')
                if len(creds)>=2:
                    name, pwd =creds[0], creds[1]
                    if name == username and check_password_hash(pwd, password):
                        return redirect(url_for('successfull'))
        return 'Invalid input '  
    return 'user login not found' 
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        if os.path.exists('infor.txt'):
            with open('infor.txt', 'r') as f:
                for line in f:
                    detail = line.strip().split(',')
                    if len(detail) >= 2 and detail[0] == username:
                        return 'Username already exists'

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        with open('infor.txt', 'a') as f:  
            f.write(f'{username},{hashed_password},{email}\n')    
        return redirect(url_for('successfull'))

    
    return render_template('register.html')
        
    
@app.route("/successfull")
def successfull():
    return render_template("quiz.html", questions=questions)

@app.route("/quiz", methods=['POST'])
def quiz():
    score = 0
    total = len(questions)

    for i, q in enumerate(questions):
        user_answer = request.form.get(f"q{i+1}")
        if user_answer == q["answer"]:
            score += 1
    return render_template('result.html',score=score, total=total)
  

if __name__=='__main__':
    app.run(debug=True)
