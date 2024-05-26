from flask import Flask, request, jsonify
import os

app = Flask(__name__)

event_database = {
    "users": {},
    "events": {},
    "event_registrations": []
}

app.config['CATERING_SERVICE_API'] = os.getenv('CATERING_SERVICE_URL')
app.config['VENUE_MANAGEMENT_API'] = os.getenv('VENUE_MANAGEMENT_URL')

@app.route('/users', methods=['POST'])
def create_user():
    user_input = request.get_json()
    if 'id' in user_input:
        event_database['users'][user_input['id']] = user_input
        return jsonify(user_input), 201
    else:
        return jsonify({"error": "Missing user ID"}), 400

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    user_details = event_database['users'].get(str(user_id))
    if user_details:
        return jsonify(user_details)
    return jsonify({"error": "User not found"}), 404

@app.route('/events', methods=['POST'])
def create_event():
    event_input = request.get_json()
    if 'id' in event_input:
        event_database['events'][event_input['id']] = event_input
        return jsonify(event_input), 201
    else:
        return jsonify({"error": "Missing event ID"}), 400

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event_details(event_id):
    event_details = event_database['events'].get(str(event_id))
    if event_details:
        return jsonify(event_details)
    return jsonify({"error": "Event not found"}), 404

@app.route('/registrations', methods=['POST'])
def event_registration():
    registration_input = request.get_json()
    event_details = event_database['events'].get(str(registration_input.get('event_id')))
    user_details = event_database['users'].get(str(registration_input.get('user_id')))
    if not event_details:
        return jsonify({"error": "Event not found"}), 404
    if not user_details:
        return jsonify({"error": "User not found"}), 404
    event_database['event_registrations'].append(registration_input)
    return jsonify(registration_input), 201

@app.route('/catering', methods=['GET'])
def list_catering_options():
    catering_service_options = {"services": ["Buffet", "A la carte", "Cocktail"]}
    return jsonify(catering_service_options)

@app.route('/venues', methods=['GET'])
def list_venue_options():
    available_venues = {"list": ["Venue A", "Venue B", "Venue C"]}
    return jsonify(available_venues)

if __name__ == '__main__':
    app.run(debug=True)