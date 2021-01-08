from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from . import auth
from . import db

bp = Blueprint('news', __name__)


@bp.route('/')
def index():
    database = db.get_db()
    posts = database.execute(
        'SELECT p.id, title, body, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
    ).fetchall()
    return render_template('news/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@auth.login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            database = db.get_db()
            database.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            database.commit()
            return redirect(url_for('news.index'))

    return render_template('news/create.html')


def get_post(id, check_author=True):
    post = db.get_db().execute(
        'SELECT p.id, title, body, p.create_date, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@auth.login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            database = db.get_db()
            database.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            database.commit()
            return redirect(url_for('news.index'))

    return render_template('news/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@auth.login_required
def delete(id):
    get_post(id)
    database = db.get_db()
    database.execute('DELETE FROM post WHERE id = ?', (id,))
    database.commit()
    return redirect(url_for('news.index'))
