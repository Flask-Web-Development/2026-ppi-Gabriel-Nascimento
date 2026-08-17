from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import db
from app.models import Category, Expense

bp = Blueprint('expenses', __name__)


@bp.route('/')
def index():
    if g.user is None:
        return redirect(url_for('auth.register'))

    expenses = (
        Expense.query
        .filter_by(author_id=g.user.id)
        .order_by(Expense.date.desc())
        .all()
    )

    return render_template('expenses/index.html', expenses=expenses)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    categories = (
        Category.query
        .filter_by(author_id=g.user.id)
        .order_by(Category.name)
        .all()
    )

    if request.method == 'POST':
        description = request.form['description']
        category_id = request.form['category_id']
        date = request.form['date']
        amount = request.form['amount']
        error = None

        if error is not None:
            flash(error)
        else:
            expense = Expense(
                description=description,
                category_id=category_id,
                date=date,
                amount=float(amount),
                author_id=g.user.id,
            )
            db.session.add(expense)
            db.session.commit()
            flash('Despesa criada com sucesso.')
            return redirect(url_for('expenses.index'))

    return render_template('expenses/create.html', categories=categories)


@bp.route('/createCategory', methods=('GET', 'POST'))
@login_required
def createcategory():
    if request.method == 'POST':
        name = request.form['name']

        category = Category.query.filter_by(name=name, author_id=g.user.id).first()

        if category is not None:
            flash('Categoria já existe.')
        else:
            category = Category(name=name, author_id=g.user.id)
            db.session.add(category)
            db.session.commit()
            flash('Categoria criada com sucesso.')
            return redirect(url_for('expenses.index'))

    return render_template('expenses/createCategory.html')


def get_expense(id, check_author=True):
    expense = db.session.get(Expense, id)

    if expense is None:
        abort(404, f"O gasto {id} não existe.")

    if check_author and expense.author_id != g.user.id:
        abort(403)

    return expense


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    expense = get_expense(id)
    categories = (
        Category.query
        .filter_by(author_id=g.user.id)
        .order_by(Category.name)
        .all()
    )

    if request.method == 'POST':
        expense.description = request.form['description']
        expense.category_id = request.form['category_id']
        expense.date = request.form['date']
        expense.amount = float(request.form['amount'])
        db.session.commit()
        return redirect(url_for('expenses.index'))

    return render_template('expenses/update.html', expense=expense, categories=categories)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    expense = get_expense(id)
    db.session.delete(expense)
    db.session.commit()
    return redirect(url_for('expenses.index'))