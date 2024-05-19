import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class EventManager:
    def __init__(self):
        self.events = {}

    def create_event(self, event_id, name, location, start_time, end_time):
        if event_id in self.events:
            print(f"Event {event_id} already exists.")
            return False
        self.events[event_id] = {
            "name": name,
            "location": location,
            "start_time": start_time,
            "end_time": end_time,
            "attendees": []
        }
        return True

    def read_event(self, event_id):
        event = self.events.get(event_id)
        if event:
            return event
        else:
            print("Event not found.")
            return None

    def update_event(self, event_id, **kwargs):
        if event_id in self.events:
            for key, value in kwargs.items():
                if key in self.events[event_id]:
                    self.events[event_id][key] = value
                else:
                    print(f"{key} is not a valid property.")
            return True
        else:
            print("Event not found.")
            return False

    def delete_event(self, event_id):
        if event_id in self.events:
            del self.events[event_id]
            return True
        else:
            print("Event not found.")
            return False

    def add_attendee(self, event_id, attendee):
        event = self.events.get(event_id)
        if event:
            event['attendees'].append(attendee)
            return True
        else:
            print("Event not found.")
            return False

    def list_attendees(self, event_id):
        event = self.events.get(event_id)
        if event:
            return event['attendees']
        else:
            print("Event not found.")
            return None

    def get_weather_forecast(self, location):
        api_key = os.getenv('WEATHER_API_KEY')
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=1&aqi=no&alerts=no"
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            forecast = weather_data['forecast']['forecastday'][0]
            return forecast['day']['condition']['text']
        else:
            print("Failed to fetch weather data.")
            return None

if __name__ == "__main__":
    event_manager = EventManager()
    event_manager.create_event("1", "Tech Conference", "New York", datetime.now(), datetime.now())
    event_manager.add_attendee("1", "John Doe")
    event_manager.add_attendee("1", "Jane Doe")
    print(event_manager.read_event("1"))
    print(event_manager.get_weather_forecast("New York"))