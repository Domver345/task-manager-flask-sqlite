from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# db config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Task model


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, default=False)


# Create db
with app.app_context():
    db.create_all()

# Home page


@app.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

# Task page route


@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    if title:
        new_task = Task(title=title)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for("index"))

# Mark Task as completed


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed  # toggle
        db.session.commit()
    return redirect(url_for("index"))

# Delete Task


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
