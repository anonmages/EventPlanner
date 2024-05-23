from flask import Flask, request, jsonify
import os

app = Flask(__name__)

event_database = {
    "users": {},
    "events": {},
    "registrations": []
}

app.config['CATERING_SERVICE_API'] = os.getenv('CATERING_SERVICE_URL')
app.config['VENUE_MANAGEMENT_API'] = os.getenv('VENUE_MANAGEMENT_URL')

@app.route('/users', methods=['POST'])
def add_user():
    user_data = request.get_json()
    if 'id' in user_data:
        event_database['users'][user_data['id']] = user_data
        return jsonify(user_data), 201
    else:
        return jsonify({"error": "Missing user ID"}), 400

@app.route('/users/<int:user_id>', methods=['GET'])
def fetch_user_details(user_id):
    user_info = event_database['users'].get(str(user_id))
    if user_info:
        return jsonify(user_info)
    return jsonify({"error": "User not found"}), 404

@app.route('/events', methods=['POST'])
def add_event():
    event_data = request.get_json()
    if 'id' in event_data:
        event_database['events'][event_data['id']] = event_data
        return jsonify(event_data), 201
    else:
        return jsonify({"error": "Missing event ID"}), 400

@app.route('/events/<int:event_id>', methods=['GET'])
def fetch_event_details(event_id):
    event_info = event_database['events'].get(str(event_id))
    if event_info:
        return jsonify(event_info)
    return jsonify({"error": "Event not found"}), 404

@app.route('/registrations', methods=['POST'])
def register_for_event():
    registration_data = request.get_json()
    event = event_database['events'].get(str(registration_data.get('event_id')))
    user = event_database['users'].get(str(registration_data.get('user_id')))
    if not event:
        return jsonify({"error": "Event not found"}), 404
    if not user:
        return jsonify({"error": "User not found"}), 404
    event_database['registrations'].append(registration_data)
    return jsonify(registration_data), 201

@app.route('/catering', methods=['GET'])
def fetch_catering_options():
    catering_options = {"services": ["Buffet", "A la carte", "Cocktail"]}
    return jsonify(catering_options)

@app.route('/venues', methods=['GET'])
def fetch_venue_options():
    venue_options = {"list": ["Venue A", "Venue B", "Venue C"]}
    return jsonify(venue_options)

if __name__ == '__main__':
    app.run(debug=True)