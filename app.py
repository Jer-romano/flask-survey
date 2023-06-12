from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "My super secret key" 

debug = DebugToolbarExtension(app)
responses = []
questions_answered_count = 0
@app.route("/")
def show_homepage():
    return render_template("base.html", title=satisfaction_survey.title,
    instructions=satisfaction_survey.instructions)

@app.route("/questions/<int:q_number>")
def show_question(q_number):
    if q_number != questions_answered_count:
        flash("Error: You're attempting to access an invalid question.", "error")
        return redirect(f"/questions/{questions_answered_count}")
    elif q_number == len(satisfaction_survey.questions):
        return redirect("/thanks")
    else:    
        return render_template("question.html", question=satisfaction_survey.questions[q_number],
        q_number=q_number, title=satisfaction_survey.title)

@app.route("/answer", methods=["POST"])
def handle_answer():
    global questions_answered_count
    questions_answered_count += 1
    answer = request.form["options"]
    responses.append(answer)
    print(answer)
    return redirect(f"/questions/{questions_answered_count}")

@app.route("/thanks")
def say_thanks():
    return render_template("thanks.html", title=satisfaction_survey.title)
