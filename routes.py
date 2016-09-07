from flask import Flask, url_for, request, render_template
from app import app
import redis

# connect to redis data store, charset over because redis saves data as 8bit
r = redis.StrictRedis(host='flasktest1.redis.cache.windows.net', port='6380',
                      password='xLxIFsNSpKIYx6G2tF4vyHiKvuCnrCpixfSmugdlPxA=' , ssl=True,
                      charset="utf-8", decode_responses=True)

# Server
@app.route('/')
def hello():

    create_link = "<a href='" + url_for('create') + "'> Create a question</a>"
    return  '''<html>
                    <head>
                        <title>is TAb</title>
                    </head>
                    <body>
                        ''' + create_link + '''
                    </body>
                </html>'''

# server/create
@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        #send user the form
        return render_template('create_question.html')
    elif request.method == 'POST':
        #read form data and save it
        title = request.form['title']
        question = request.form['question']
        answer = request.form['answer']

        # Store data in data store
        # Key name will be title : question
        r.set(title + ':question', question)
        r.set(title + ':answer', answer)

        return render_template('created_question.html',
                               question = question)
    else:
        return "<h2>Invalid Request</h2>"

# server/question/<title>
@app.route('/question/<title>', methods=['GET', 'POST'])
def question(title):
    if request.method == 'GET':
        #send user the form

        #Read question from data store
        question = r.get(title+':question')

        return render_template('answer_question.html',
                               question = question)
    elif request.method == 'POST':
        # User attempted answer. check if they are correct
        submitted_answer = request.form['submitted_answer']

        #read from data store
        answer = r.get(title+':answer')

        if submitted_answer == answer:
            return render_template('correct.html')
        else:
            return render_template('incorrect.html',
                                   submitted_answer = submitted_answer,
                                   answer = answer)
    return "<h2>" + title + "</h2>"

