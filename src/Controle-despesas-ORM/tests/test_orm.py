from app import create_app
from app.db import db
from app.models import User


def test_sqlalchemy_models_are_available():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test',
    })

    with app.app_context():
        db.create_all()
        user = User(username='alice', password='hashed-password')
        db.session.add(user)
        db.session.commit()

        stored = db.session.execute(
            db.select(User).where(User.username == 'alice')
        ).scalar_one()

        assert stored.username == 'alice'
