from .db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    expenses = db.relationship('Expense', back_populates='author', lazy=True)
    categories = db.relationship('Category', back_populates='author', lazy=True)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    author = db.relationship('User', back_populates='categories')
    expenses = db.relationship('Expense', back_populates='category', lazy=True)

    __table_args__ = (
        db.UniqueConstraint('name', 'author_id', name='uq_category_name_author'),
    )


class Expense(db.Model):
    __tablename__ = 'expense'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    author = db.relationship('User', back_populates='expenses')
    category = db.relationship('Category', back_populates='expenses')

    @property
    def category_name(self):
        return self.category.name if self.category else None
