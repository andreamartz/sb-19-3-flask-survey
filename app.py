from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# ********************************************
# GLOBAL VARIABLES
# responses -> initialize responses; this is the variable that will store survey answers
#     e.g. responses = ['Yes', 'No', 'Less than $10,000', 'Yes']
responses = []
# survey -> stores the survey questions and choices
survey = satisfaction_survey
# *********************************************


@app.route('/')
def home_page():
    """Shows survey start page"""
    return render_template('home.html', survey=survey)


@app.route('/questions/<int:idx>')
def show_question(idx):
    """Shows question from the survey"""
    question = survey.questions[idx].question
    choices = survey.questions[idx].choices
    return render_template('question.html', survey=survey, question=question, choices=choices, idx=idx)


@app.route('/answer', methods=['POST'])
def add_answer():
    answer = request.form['answer']
    # Add to pretend database
    responses.append(answer)
    if len(responses) < len(survey.questions):
        return redirect(f'/questions/{len(responses)}')
    else:
        return redirect('/thank-you')


@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')
