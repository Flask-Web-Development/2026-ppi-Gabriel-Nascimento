from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('expenses', __name__)

@bp.route('/')
def index():
    db = get_db()
    expenses = db.execute(
        'SELECT e.*, u.*'
        ' FROM expense e JOIN user u ON e.author_id = u.id'
        ' ORDER BY date DESC'
    ).fetchall()
    return render_template('expenses/index.html', expenses=expenses)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        category = request.form['category']
        date = request.form['date']
        amount = request.form['amount']
        author_id = session['user_id']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO expense (description, category, date, amount, author_id)'
                ' VALUES (?, ?, ?, ?, ?)',
                (description, category, date, amount, author_id)
            )
            db.commit()
            return redirect(url_for('expenses.index'))

    return render_template('expenses/create.html')

def get_expense(id, check_author=True):
    expense = get_db().execute(
        'SELECT e.*, username'
        ' FROM expense e JOIN user u ON e.author_id = u.id'
        ' WHERE e.id = ?',
        (id,)
    ).fetchone()

    if expense is None:
        abort(404, f"O gasto {id} não existe.")

    if check_author and expense['author_id'] != g.user['id']:
        abort(403)

    return expense

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    expense = get_expense(id)

    if request.method == 'POST':
        description = request.form['description']
        category = request.form['category']
        date = request.form['date']
        amount = request.form['amount']
        error = None

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE expense SET description = ?, category = ?, date = ?, amount = ?'
                ' WHERE id = ?',
                (description, category, date, amount, id)
            )
            db.commit()
            return redirect(url_for('expenses.index'))

    return render_template('expenses/update.html', expense=expense)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_expense(id)
    db = get_db()
    db.execute('DELETE FROM expense WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('expenses.index'))