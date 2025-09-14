#!/usr/bin/env python3
# -- coding: utf-8

'''
this program uses flask to create a login page, registration page and saves it in infor.txt file
if you login there is a quiz page and after answers the questions it take you to a new page to show you result
'''

from flask import Flask,render_template,request,redirect,url_for
import os

app = Flask(__name__)

questions = [
    {'question': 'What is the capital of France?', 
     'options':{
         'A':'Berlin',
         'B':'Madrid', 
         'C':'Paris', 
         'D': 'Rome'
         } ,
     'answer': 'C'
    },
    {'question': 'which Planet is know as the red planet?',
     'options': {
         'A':'Earth',
         'B':'Mars',
         'C':'Jupiter',
         'D':'Saturn'
         },
     'answer': 'B'
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
                    if name == username and pwd ==password:
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

        with open('infor.txt', 'a') as f:  
            f.write(f'{username},{password},{email}\n')    
        return 'Registration successful'   

    
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
