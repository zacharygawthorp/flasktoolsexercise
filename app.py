from flask import Flask, flash, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey


# Intialize empty array to store answers
RESPONSES = []

app = Flask(__name__)
app.config['SECRET_KEY'] = "don't-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

dedug = DebugToolbarExtension(app)


@app.route("/")
def show_survey_start():
    """Select a survey."""


    return render_template("survey_start.html", survey=survey)


@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question"""
    responses = RESPONSES

    if (responses is None):
        # trying to access questions page too soon.
        return redirect("/")
    
    if(len(responses) == len(survey.questions)):
        # All questions have been answered, redirect to thank you page.
        return redirect("/complete")

    if(len(responses) != qid):
        # trying to access questions out of order
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template("question.html", question_num=qid, question=question)


@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to the next question."""
    
    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = RESPONSES
    responses.append(choice)
    
    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    """Survey complete, show completion page"""

    return render_template("completion.html")