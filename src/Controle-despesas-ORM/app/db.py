import click
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


@click.command('init-db')
def init_db_command():
    db.create_all()
    click.echo('Initialized the database.')


def init_app(app):
    db.init_app(app)
    app.cli.add_command(init_db_command)