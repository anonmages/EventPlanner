import unittest
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
app.config['TESTING'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json['username']
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"username": new_user.username}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return jsonify({"username": user.username}), 200
    else:
        return jsonify({"error": "User not found"}), 404

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_user(self):
        with app.test_client() as client:
            response = client.post('/users', json={'username': 'testuser'})
            data = response.get_json()
            self.assertEqual(response.status_code, 201)
            self.assertEqual(data['username'], 'testuser')
    
    def test_get_user(self):
        with app.test_client() as client:
            client.post('/users', json={'username': 'testuser2'})
            response = client.get('/users/1')
            data = response.get_json()
            self.assertEqual(response.status_status_code, 200)
            self.assertEqual(data['username'], 'testuser2')
    
    def test_user_not_found(self):
        with app.test_client() as client:
            response = client.get('/users/999')
            self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()