import pytest
import sys
from flaskr.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.debug = True
    app.testing = True
    app = app.test_client()
    return app

'''
@pytest.fixture(scope='module')
def init_database():
    # Create the database and the database table
    db.create_all()
 
    # Insert user data
    user1 = User(email='patkennedy79@gmail.com', plaintext_password='FlaskIsAwesome')
    user2 = User(email='kennedyfamilyrecipes@gmail.com', plaintext_password='PaSsWoRd')
    db.session.add(user1)
    db.session.add(user2)
 
    # Commit the changes for the users
    db.session.commit()
 
    yield db  # this is where the testing happens!
 
    db.drop_all()
'''

