import pytest
from datetime import datetime
from server.app import app, db
from server.models import Message

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

class TestMessage:
    '''Tests for the Message model'''

    def test_has_correct_columns(self, test_client):
        with app.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza"
            )
            db.session.add(hello_from_liza)
            db.session.commit()

            assert hello_from_liza.body == "Hello 👋"
            assert hello_from_liza.username == "Liza"
            assert isinstance(hello_from_liza.created_at, datetime)

            db.session.delete(hello_from_liza)
            db.session.commit()

    def test_creates_message(self, test_client):
        with app.app_context():
            message = Message(body="Hello 👋", username="Liza")
            db.session.add(message)
            db.session.commit()

            saved_message = Message.query.filter_by(body="Hello 👋").first()
            assert saved_message is not None
            assert saved_message.username == "Liza"

            db.session.delete(saved_message)
            db.session.commit()
