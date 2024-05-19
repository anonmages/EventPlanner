from flask import Flask, request, jsonify
import os

app = Flask(__name__)

DATABASE = {
    "users": [],
    "events": [],
    "registrations": []
}

app.config['CATERING_SERVICE_URL'] = os.getenv('CATERING_SERVICE_URL')
app.config['VENUE_MANAGEMENT_URL'] = os.getenv('VENUE_MANAGEMENT_URL')

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    DATABASE['users'].append(data)
    return jsonify(data), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in DATABASE['users'] if user['id'] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    DATABASE['events'].append(data)
    return jsonify(data), 201

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = next((event for event in DATABASE['events'] if event['id'] == event_id), None)
    if event:
        return jsonify(event)
    return jsonify({"error": "Event not found"}), 404

@app.route('/registrations', methods=['POST'])
def create_registration():
    data = request.get_json()
    if not next((event for event in DATABASE['events'] if event['id'] == data['event_id']), None):
        return jsonify({"error": "Event not found"}), 404
    if not next((user for user in DATABASE['users'] if user['id'] == data['user_id']), None):
        return jsonify({"error": "User not found"}), 404
    DATABASE['registrations'].append(data)
    return jsonify(data), 201

@app.route('/catering', methods=['GET'])
def get_catering_services():
    catering_services = {"services": ["Buffet", "A la carte", "Cocktail"]}
    return jsonify(catering_services)

@app.route('/venues', methods=['GET'])
def get_venues():
    venues = {"list": ["Venue A", "Venue B", "Venue C"]}
    return jsonify(venues)

if __name__ == '__main__':
    app.run(debug=True)