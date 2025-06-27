import pytest
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

def test_get_messages(test_client):
    with app.app_context():
        message = Message(body="Hello 👋", username="Liza")
        db.session.add(message)
        db.session.commit()

        response = test_client.get('/messages')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['body'] == "Hello 👋"