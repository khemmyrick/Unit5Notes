import re

import urllib.request
from bs4 import BeautifulSoup
from flask import (Flask, g, render_template, flash, redirect, url_for,
                   abort)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'aumesh.boquoastuh.43,uoawu4opuosth3ou1npa.auboub!'

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
@app.route('/entries/edit/<post_slug>', methods=('GET', 'POST'))
@login_required
def post(post_slug=None):
    """Add/Edit an entry to the stream."""
    form = forms.PostForm()
    if post_slug:
        try:
            edeet = models.Post.select().where(
              models.post.slug == post_slug
            ).get()
        except models.DoesNotExist:
            abort(404)
        else:
            etags = edeet.all_tags()
            if form.validate_on_submit():
                edeet.title = form.title.data
                edeet.learned = link_it(form.learned.data)
                edeet.resources = link_it(r_lister(form.resources.data))
                edeet.minutes = form.minutes.data
                edeet.datestamp = form.datestamp.data
                edeet.save()
                tag_maker(form, edeet)
                flash("Message saved.", "success")
                return redirect(url_for('index'))
        if edeet:
            return render_template('edit.html', form=form, edeet=edeet, etags=etags)
        else:
            abort(404)
    elif form.validate_on_submit():
        new_post = models.Post.create(
          title=form.title.data,
          learned=link_it(form.learned.data),
          resources=link_it(r_lister(form.resources.data)),
          minutes=form.minutes.data,
          datestamp=form.datestamp.data,
          slug=slugify(form.title.data)
        )
        tag_maker(form, new_post)
        flash("Message posted. Thanks!", "success")
        return redirect(url_for('index'))
    return render_template('new.html', form=form)


@app.route('/')
@app.route('/entries')
@app.route('/entries/tag/<tagname>')
def index(tagname=None):
    """Populates stream.html with db posts."""
    if tagname:
        tag_target = models.Tag.select().where(
          models.Tag.slug == tagname
        ).get()
        stream = tag_target.all_posts()
    else:
        stream = models.Post.select().limit(100)
    # Passes first 100 db posts to stream.
    return render_template('index.html', stream=stream)


@app.route('/entries/delete/<post_slug>')
@login_required
def delete(post_slug):
    """Delete an entry from our db."""
    try:
        dleet = models.Post.select().where(models.post.slug == post_slug).get()
    except models.DoesNotExist:
        flash("Can't delete what isn't there.")
        return redirect(url_for('index'))
    else:
        dleet.delete_instance()
        flash("Message deleted.", "success")
        return redirect(url_for('index'))


@app.route('/details/<post_slug>')
@login_required
def view_post(post_slug):
    """View a specific post (in detail)."""
    try:
        deets = models.Post.select().where(models.post.slug == post_slug).get()
    except models.DoesNotExist:
        abort(404)
    else:
        tags = deets.all_tags()
    return render_template('detail.html', deets=deets, tags=tags)


@app.errorhandler(404)
def not_found(error):
    """Open 404 page if file not found."""
    return render_template('404.html'), 404


def tag_maker(form, post):
    """Add tag instances to the db."""
    tag_list = form.tags.data.split(',')
    tag_list = set(tag_list)
    tag_list = list(tag_list)
    for tag in tag_list:
        try:
            add_tag = models.Tag.select().where(
              models.Tag.term == tag.strip()
            ).get()
        except models.DoesNotExist:
            add_tag = models.Tag.create(term=tag.strip(),
                                        slug=slugify(tag))
        finally:
            models.TagTrend.create(post_call=add_tag,
                                   tag_by=post)
    return


def link_it(learned):
    """Apply anchor tags to certain user inputs."""
    final_string = learned
    l_list = re.findall(r'(http\S+)', learned)
    if l_list:
        for a_tag in l_list:
            a_page = urllib.request.urlopen(a_tag)
            html = BeautifulSoup(a_page.read(), "html.parser")
            newstr = '<a href="{}">{}</a>'.format(a_tag, html.title.string)
            final_string = final_string.replace(a_tag, newstr)
        learned = final_string
    return learned


def r_lister(resources):
    final_string = resources
    if len(re.findall(r'([\S ]+\r)', resources)) > 1:
        final_string = "{}\r".format(final_string)
        r_list = re.findall(r'([\S ]+\r)', final_string)
        for reso in r_list:
            newreso = '<li>{}</li>'.format(reso)
            final_string = final_string.replace(reso, newreso)
        final_string = '<ul>{}</ul>'.format(final_string)
    return final_string


def slugify(o_str):
    """Spawn slugs."""
    o_str = o_str.lower()
    for chara in [' ', '-', '.', '/']:
        o_str = o_str.replace(chara, '_')
    o_str = re.sub('\W', '', o_str)
    # Delete non-word characters, other than ones caught by previous line.
    # This would also catch spaces, hence swapping them out for unders.
    o_str = o_str.replace('_', ' ')
    o_str = re.sub('\s+', ' ', o_str)
    # Replace any instances of multiple spaces with a single space.
    o_str = o_str.strip()
    o_str = o_str.replace(' ', '-')
    return o_str


if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            password='project5'
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
