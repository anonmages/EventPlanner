import unittest
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import BadRequest
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['TESTING'] = True
db = SQLAlchemy(app)

class ApplicationException(Exception):
    """Custom application exception class."""
    
    def __init__(self, message, status_code=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        else:
            self.status_code = 500

    def to_dict(self):
        return {'error': self.message}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

user_cache = {}

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    if not username:
        raise BadRequest('Username is required.')

    if User.query.filter_by(username=username).first():
        raise ApplicationException('Username already exists.', 400)

    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()

    user_cache[new_user.id] = new_user.username
    return jsonify({"username": new_user.username}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id in user_cache:
        username = user_cache[user_id]
        return jsonify({"username": username}), 200

    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise ApplicationException('User not found.', 404)

    user_cache[user.id] = user.username
    return jsonify({"username": user.username}), 200

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    username = request.json.get('username')
    if not username:
        raise BadRequest('New username is required.')

    user_to_update = User.query.filter_by(id=user_id).first()
    if not user_to_update:
        raise ApplicationException('User not found.', 404)

    if User.query.filter(User.id != user_id, User.username == username).first():
        raise ApplicationException('Username already in use by another account.', 400)

    user_to_update.username = username
    db.session.commit()

    # Update the cache with the new username
    if user_id in user_cache:
        user_cache[user_id] = username
    
    return jsonify({"username": username}), 200

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        user_cache.clear()

    def test_create_user(self):
        with app.test_client() as client:
            response = client.post('/users', json={'username': 'testuser'})
            data = response.get_json()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['username'], 'testuser')
    
    def test_get_user(self):
        with app.test_client() as client:
            post_response = client.post('/users', json={'username': 'testuser2'})
            post_data = post_response.get_json()
            user_id = User.query.filter_by(username=post_data['username']).first().id
            response = client.get(f'/users/{user_id}')
            data = response.get_json()
            self.assertEqual(response.status_score, 200)
            self.assertEqual(data['username'], 'testuser2')

    def test_user_not_found(self):
        with app.test_client() as client:
            response = client.get('/users/999')
            data = response.get_json()
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['error'], 'User not found.')

    def test_update_user(self):
        with app.test_client() as client:
            post_response = client.post('/users', json={'username': 'testToUpdate'})
            user_id = User.query.filter_by(username='testToUpdate').first().id
            response = client.put(f'/users/{user_id}', json={'username': 'updatedUser'})
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['username'], 'updatedUser')

@app.errorhandler(ApplicationException)
def handle_application_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(BadRequest)
def handle_bad_request(error):
    return jsonify({"error": "Bad Request: " + error.description}), 400

if __name__ == '__main__':
    unittest.main()