import re

from flask import (Flask, g, render_template, flash, redirect, url_for,
                   abort)
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required, current_user)

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    """Load user i guess"""
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/login', methods=('GET', 'POST'))
def login():
    """Login user."""
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.select().get()
        except models.DoesNotExist:
            flash("Your credentials are invalid.", "error")
            return 'i do not see your model'
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your credentials are invalid", "error")
    return render_template('login.html', form=form)


@app.route('/logout', methods=('GET', 'POST'))
@login_required
def logout():
    """Logout user."""
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))


@app.route('/entry', methods=('GET', 'POST'))
@app.route('/entries/edit/<int:post_id>', methods=('GET', 'POST'))
@login_required
def post(post_id=None):
    """Add/Edit an entry to the stream."""
    form = forms.PostForm()
    if post_id:
        try:
            edeet = models.Post.select().where(models.Post.id == post_id).get()
        except models.DoesNotExist:
            flash("We got a Does Not Exist error on that post_id.")
            return redirect(url_for('index'))
        else:
            if form.validate_on_submit():
                edeet.title = form.title.data
                edeet.learned = mark_up(form.learned.data)
                edeet.resources = form.resources.data
                edeet.minutes = form.minutes.data
                edeet.datestamp = form.datestamp.data
                edeet.save()
                flash("Message saved.", "success")
                return redirect(url_for('index'))
        if edeet:
            return render_template('edit.html', form=form, edeet=edeet)
        else:
            return 'something went wrong'
    elif form.validate_on_submit():
        models.Post.create(title=form.title.data,
                           learned=mark_up(form.learned.data),
                           resources=form.resources.data,
                           minutes=form.minutes.data,
                           datestamp=form.datestamp.data)
        flash("Message posted. Thanks!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/')
@app.route('/entries')
def index():
    """Populates stream.html with db posts."""
    stream = models.Post.select().limit(100)
    return render_template('index.html', stream=stream)


@app.route('/entries/delete/<int:post_id>')
@login_required
def delete(post_id):
    """Delete an entry from our db."""
    try:
        dleet = models.Post.select().where(models.Post.id == post_id).get()
    except models.DoesNotExist:
        flash("We got a Does Not Exist error on that post_id.")
        return redirect(url_for('index'))
    else:
        dleet.delete_instance()
        flash("Message deleted.", "success")
        return redirect(url_for('index'))


@app.route('/details/<int:post_id>')
@login_required
def view_post(post_id):
    """View a specific post (in detail)."""
    posts = models.Post.select().where(models.Post.id == post_id)
    if posts.count() == 0:
        abort(404)
    if posts.count() == 1:
        singular = True
    else:
        singular = False
    return render_template('detail.html', stream=posts, singular=singular)


@app.errorhandler(404)
def not_found(error):
    """Open 404 page if file not found."""
    return render_template('404.html'), 404


def mark_up(learned):
    """Apply anchor tags to certain user inputs."""
    final_string = learned
    l_list = re.findall(r'^(\[[\w+:/.]+ [\w+ ,.]\])$', learned)
    # Not sure how to get the proper regex pattern for this.
    if l_list:
        for a_tag in l_list:
            newstr = a_tag.replace('[', '<a href="')
            newstr = newstr.replace(' ', '">', 1)
            newstr = newstr.replace(']', '</a>')
            final_string = final_string.replace(a_tag, newstr)
        learned = final_string
    return learned


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            password='project5'
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
