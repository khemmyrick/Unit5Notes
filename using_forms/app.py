from flask import Flask, request, render_template, redirect, url_for

from models import Entry
import forms

app = Flask(__name__)


@app.route('/')  # The route CALLS the function.
@app.route('/<name>')  # '/' or '/<name>' calls the index function.
def index(name="the Crystal Gems"):
    log = Entry.select()
    return render_template("index.html", log=log, name=name)


@app.route('/new', methods=['POST'])  # Called from within a webpage of a different function.
def new():
    form = forms.PostEntry()
    if form.validate_on_submit():
        Entry.create(timestamp=form.timestamp.data,
                     user_name=form.user_name.data,
                     task_name=form.task_name.data,
                     task_minutes=form.task_minutes.data,
                     task_notes=form.task_notes.data.strip())
        flash("Entry posted!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)

# @app.route('/new', methods=['POST'])
# def new():
    
    # try:
    #    Entry.create(user_name=user_name,
    #                 task_name=task_name,
    #                 task_minutes=task_minutes,
    #                 task_notes=task_notes
    #                 timestamp=timestamp)
    # except ValueError:
#        return render_template('new.html')
#    else:
#        return redirect(url_for('index'))

@app.route('/add/<float:num1>/<int:num2>')
@app.route('/add/<float:num1>/<float:num2>')
@app.route('/add/<int:num1>/<float:num2>')
@app.route('/add/<int:num1>/<int:num2>')  # Calls the add function.
def add(num1, num2):
    return render_template("add.html", num1=num1, num2=num2)  # Render template takes the url of the html as the first argument, and any variables being passed to it as additional arguments.

app.run(debug=True, port=8000, host='0.0.0.0')
