from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from datetime import datetime
from app.auth import login_required
from app.db import get_db

bp = Blueprint('expenses', __name__)

@bp.route('/')
def index():
    db = get_db()

    if g.user is None:
        return redirect(url_for('auth.register'))
    
    expenses = db.execute(
    '''
    SELECT e.*, u.username, c.name AS category_name
    FROM expense e
    JOIN user u ON e.author_id = u.id
    JOIN category c ON e.category_id = c.id
    ORDER BY e.date DESC
    '''
    ).fetchall()
    return render_template('expenses/index.html', expenses=expenses)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    db = get_db()

    categories = db.execute(
        '''
        SELECT id, name
        FROM category
        WHERE author_id = ?
        ORDER BY name
        ''',
        (g.user['id'],)
    ).fetchall()

    if request.method == 'POST':
        description = request.form['description']
        category = request.form['category_id']
        date = request.form['date']
        amount = request.form['amount']
        author_id = g.user['id']
        error = None
        

        if error is not None:
            flash(error)
                
        else:
            db.execute(
                '''
                INSERT INTO expense
                (description, category_id, date, amount, author_id)
                VALUES (?, ?, ?, ?, ?)
                ''',
                (description, category, date, amount, author_id)
            )
            db.commit()
            flash('Despesa criada com sucesso.')
            return redirect(url_for('expenses.index'))

    return render_template(
        'expenses/create.html', categories=categories
    )


@bp.route('/createCategory', methods=('GET', 'POST'))
@login_required
def createcategory():
    db = get_db()

    if request.method == 'POST':
        name = request.form['name']

        categories = db.execute(
            '''
            SELECT id
            FROM category
            WHERE name = ? AND author_id = ?
            ORDER BY name
            ''',
            (name, g.user['id'])
        ).fetchone()
        
        if categories is not None:
            flash('Categoria já existe.')
        else:
            db.execute(
                '''
                INSERT INTO category
                (name, author_id)
                VALUES (?, ?)
                ''',
                (name, g.user['id'])
            )
            db.commit()
            flash('Categoria criada com sucesso.')
            return redirect(url_for('expenses.index'))

    return render_template('expenses/createCategory.html')


def get_expense(id, check_author=True):
    expense = get_db().execute(
        '''
        SELECT e.*, u.username
        FROM expense e
        JOIN user u ON e.author_id = u.id
        WHERE e.id = ?
        ''',
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
    db = get_db()

    expense = get_expense(id)

    categories = db.execute(
        '''
        SELECT id, name
        FROM category
        WHERE author_id = ?
        ORDER BY name
        ''',
        (g.user['id'],)
    ).fetchall()

    if request.method == 'POST':
        description = request.form['description']
        category = request.form['category_id']
        date = request.form['date']
        amount = request.form['amount']

        db.execute(
            '''
            UPDATE expense
            SET description = ?, category_id = ?, date = ?, amount = ?
            WHERE id = ?
            ''',
            (description, category, date, amount, id)
        )
        db.commit()

        return redirect(url_for('expenses.index'))

    return render_template(
        'expenses/update.html',
        expense=expense,
        categories=categories
    )

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_expense(id)
    db = get_db()
    db.execute('DELETE FROM expense WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('expenses.index'))