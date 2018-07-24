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
# DEBUG, PORT and HOST variables are established up here and 
# Referenced when the run() method is called on app at the bottom.

app = Flask(__name__)
# I have no idea what this is.
app.secret_key = 'auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!'
# A secret key allows the app to create a session, or something?
# Not sure what that is, or what it means.

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def load_user(userid):
#    try:
#        return models.User.get(models.User.id == userid)
#    except models.DoesNotExist:
#        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    # g is a global variable.
    # In these 2 functions, g opens and closes the database.
    # I'm not actually sure what g is or why it's needed to do that...
    # Unless database manipulation can only happen from an external object?
    # g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


# @app.route('/register', methods=('GET', 'POST'))
# def register():
#    form = forms.RegisterForm()
#    if form.validate_on_submit():
#        flash("Yay, you registered!", "success")
#        models.User.create_user(
#            username=form.username.data,
#            email=form.email.data,
#            password=form.password.data
#        )
#        return redirect(url_for('index'))
#    return render_template('register.html', form=form)


# @app.route('/login', methods=('GET', 'POST'))
# def login():
#    form = forms.LoginForm()
#    if form.validate_on_submit():
#        try:
#            user = models.User.get(models.User.email == form.email.data)
#        except models.DoesNotExist:
#            flash("Your email or password doesn't match!", "error")
#        else:
#            if check_password_hash(user.password, form.password.data):
#                login_user(user)
#                flash("You've been logged in!", "success")
#                return redirect(url_for('index'))
#            else:
#                flash("Your email or password doesn't match!", "error")
#    return render_template('login.html', form=form)


# @app.route('/logout')
# @login_required
# def logout():
#    logout_user()
#    flash("You've been logged out! Come back soon!", "success")
#    return redirect(url_for('index'))


@app.route('/entry', methods=('GET', 'POST'))
@app.route('/entry/edit/<int:post_id>', methods=('GET', 'POST'))
# @login_required
def post(post_id=None):  # add post_id=None
    """Post a new entry to the stream."""
    form = forms.PostForm()  # pass a PostForm instance to form.
    if post_id and form.validate_on_submit():
        try:
            edeet = models.Post.select().where(models.Post.id == post_id).get()
        except models.DoesNotExist:
            flash("We got a Does Not Exist error on that post_id.")
            return redirect(url_for('index'))
        else:
            edeet.title = form.title.data
            edeet.learned = form.learned.data
            edeet.resources = form.resources.data
            edeet.minutes = form.minutes.data
            edeet.datestamp = form.datestamp.data
            edeet.save()
            flash("Message saved.", "success")
            return redirect(url_for('index'))
    elif form.validate_on_submit():  # Is this checking if the form has valid entries?
        models.Post.create(title=form.title.data,
                           learned=form.learned.data,
                           resources=form.resources.data,
                           minutes=form.minutes.data,
                           datestamp=form.datestamp.data)
        # Passes form's content text string to new post's content attribute.
        flash("Message posted. Thanks!", "success")
        # Alerts user that the message posted.  Is working rn.
        return redirect(url_for('index'))  # Sends user to main index page.
    return render_template('post.html', form=form)  # Is this reloading the page we're already on?


@app.route('/')
def index():
    """Populates stream.html with db posts."""
    stream = models.Post.select().limit(100)
    # Passes first 100 db posts to stream.
    return render_template('stream.html', stream=stream)  # Renders stream.html and passes stream variable to html file.


@app.route('/entries')
def stream():
    """Also renders stream?
    Not sure how this differs from index view."""
    template = 'stream.html'  # Passes stream.html into template variable.
    stream = models.Post.select()  # Passes all db posts to stream variable.
    return render_template(template, stream=stream)  # Renders exact same thing as index view?


@app.route('/entries/delete/<int:post_id>')
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
def view_post(post_id):
    """View a specific post (in detail)."""
    posts = models.Post.select().where(models.Post.id == post_id)
    # Get posts where post.id attribute matches post_id arg in view.
    if posts.count() == 0:
        abort(404)  # If nothing's there, bring up 404 page.
    singular = True
    return render_template('stream.html', stream=posts, singular=singular)  # Otherwise, render every post that matches search.


# @app.route('/follow/<username>')
# @login_required
# def follow(username):
#     try:
#        to_user = models.User.get(models.User.username**username)
#    except models.DoesNotExist:
#        abort(404)
#    else:
#        try:
#            models.Relationship.create(
#                from_user=g.user._get_current_object(),
#                to_user=to_user
#            )
#        except models.IntegrityError:
#            pass
#        else:
#            flash("You're now following {}!".format(to_user.username), "success")
#    return redirect(url_for('stream', username=to_user.username))

# @app.route('/unfollow/<username>')
# @login_required
# def unfollow(username):
#    try:
#        to_user = models.User.get(models.User.username**username)
#    except models.DoesNotExist:
#        abort(404)
#    else:
#        try:
#            models.Relationship.get(
#                from_user=g.user._get_current_object(),
#                to_user=to_user
#            ).delete_instance()
#        except models.IntegrityError:
#            pass
#        else:
#            flash("You've unfollowed {}!".format(to_user.username), "success")
#    return redirect(url_for('stream', username=to_user.username))


@app.errorhandler(404)
def not_found(error):
    """Open 404 page if file not found."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    models.initialize()
#    try:
#        models.User.create_user(
#            username='kennethlove',
#            email='kenneth@teamtreehouse.com',
#            password='password',
#            admin=True
#        )
#    except ValueError:
#        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
