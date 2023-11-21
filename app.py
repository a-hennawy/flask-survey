from flask import Flask, render_template, request, redirect, session, flash
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
# responses = []
RESPONSES_KEY = "responses"
NEXT_Q = "next_Q"
sat_survey = satisfaction_survey


@app.route('/')
def root():
    title = satisfaction_survey.title
    instructions = sat_survey.instructions
    session[RESPONSES_KEY] = []
    print(session.get(RESPONSES_KEY))
    return render_template('home.html', title=title, instructions=instructions)


@app.route('/questions/<int:q_num>')
def quest(q_num):
    question = sat_survey.questions[q_num].question
    choice = sat_survey.questions[q_num].choices
    session[NEXT_Q] = q_num+1
    response_list = session.get(RESPONSES_KEY)
    if response_list is None:
        return redirect('/')
    if q_num != len(response_list):
        flash(f"Invalid question id: {q_num}.")
        return redirect(f"/questions/{len(response_list)}")

    # print(response_list)
    # print(session)
    return render_template('quest-form.html', question=question, choice=choice, q_num=q_num)


@app.route('/answer', methods=["post"])
def answer():

    # next_Q = request.form['next_Q']
    response = request.form['response']
    response_list = session[RESPONSES_KEY]
    response_list.append(response)
    session[RESPONSES_KEY] = response_list
    # print(session.get(RESPONSES_KEY))

    if session[NEXT_Q] < len(sat_survey.questions):
        return redirect(f'/questions/{session[NEXT_Q]}')
    else:
        # print(session)
        return redirect(f'/Thank-you-page')


@app.route('/Thank-you-page')
def thank_you():
    # print(responses)
    return render_template('thank-you-page.html')
