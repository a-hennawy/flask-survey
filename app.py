from flask import Flask, render_template, request, redirect
from surveys import *

app = Flask(__name__)
responses = []
sat_survey = satisfaction_survey


@app.route('/')
def root():
    title = satisfaction_survey.title
    instructions = sat_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)


@app.route('/questions/<q_num>')
def quest(q_num):
    question = sat_survey.questions[int(q_num)].question
    choice = sat_survey.questions[int(q_num)].choices
    return render_template('quest-form.html', question=question, choice=choice, q_num=int(q_num))


@app.route('/answer', methods=["post"])
def answer():
    next_Q = request.form['next_Q']
    response = request.form['response']
    # raise
    responses.append(response)
    if int(next_Q) < len(sat_survey.questions):
        return redirect(f'/questions/{next_Q}')
    else:
        return redirect(f'/Thank-you-page')


@app.route('/Thank-you-page')
def thank_you():
    print(responses)
    return render_template('thank-you-page.html')
