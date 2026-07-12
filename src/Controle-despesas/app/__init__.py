import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import expenses
    app.register_blueprint(expenses.bp)
    app.add_url_rule('/', endpoint='index')

    @app.template_filter('date_format')
    def date_format(value):
        from datetime import datetime
        return datetime.strptime(value, '%Y-%m-%d').strftime('%d %b %Y')

    return app