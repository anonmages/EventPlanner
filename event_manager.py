import os
import json
import requests
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class EventManager:
    def __init__(self, filename='events.json'):
        self.filename = filename
        self.events = self.load_events()

    def save_events(self):
        with open(self.filename, 'w') as file:
            json.dump(self.events, file, indent=4, default=str)

    def load_events(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return {}

    def create_event(self, event_id, name, location, start_time, end_time):
        if event_id in self.events:
            print(f"Event {event_id} already exists.")
            return False
        self.events[event_id] = {
            "name": name,
            "location": location,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "attendees": []
        }
        self.save_events()
        return True

    def read_event(self, event_id):
        event = self.events.get(event_id)
        if event:
            event_formatted = {
                "name": event["name"],
                "location": event["location"],
                "start_time": datetime.fromisoformat(event["start_time"]).strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": datetime.fromisoformat(event["end_time"]).strftime('%Y-%m-%d %H:%M:%S'),
                "attendees": event["attendees"]
            }
            return event_formatted
        else:
            print("Event not found.")
            return None

    def update_event(self, event_id, **kwargs):
        if event_id in self.events:
            for key, value in kwargs.items():
                if key in self.events[event_id]:
                    self.events[event_id][key] = value.isoformat() if isinstance(value, datetime) else value
                    self.save_events()
                else:
                    print(f"{key} is not a valid property.")
            return True
        else:
            print("Event not found.")
            return False

    def delete_event(self, event_id):
        if event_id in self.events:
            del self.events[event_id]
            self.save_events()
            return True
        else:
            print("Event not found.")
            return False

    def add_attendee(self, event_id, attendee):
        event = self.events.get(event_id)
        if event:
            event['attendees'].append(attendee)
            self.save_events()
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
            detailed_forecast = {
                "condition": forecast['day']['condition']['text'],
                "max_temp": forecast['day']['maxtemp_c'],
                "min_temp": forecast['day']['mintemp_c'],
                "chance_of_rain": forecast['day']['daily_chance_of_rain']
            }
            return detailed_forecast
        else:
            print("Failed to fetch weather data.")
            return None

    def check_event_reminder(self, hours_before=24):
        reminders = []
        now = datetime.now()
        for event_id, event in self.events.items():
            start_time = datetime.fromisoformat(event["start_time"])
            if 0 < (start_time - now).total_seconds() <= hours_before * 3600:
                reminders.append(f"Reminder: The event '{event['name']}' is starting soon at {start_time.strftime('%Y-%m-%d %H:%M:%S')}.")
                self.send_email_reminder(event['name'], start_time, event['attendees'])
        return reminders

    def send_email_reminder(self, event_name, event_start_time, attendees):
        email_address = os.getenv('EMAIL_ADDRESS')
        email_password = os.getenv('EMAIL_PASSWORD')
        
        if not email_address or not email_password:
            print("Email credentials are missing.")
            return

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_address, email_password)
            for attendee in attendees:
                msg = EmailMessage()
                msg['Subject'] = f'Reminder: Upcoming Event - {event_name}'
                msg['From'] = email_address
                msg['To'] = attendee
                msg.set_content(f'Hello, \n\nThis is a reminder that the event "{event_name}" is starting soon at {event_start_time.strftime("%Y-%m-%d %H:%M:%S")}. \n\nSee you there!')
                
                smtp.send_message(msg)
                print(f"Reminder email sent to {attendee}.")

if __name__ == "__main__":
    event_manager = EventManager()
    event_manager.create_event("1", "Tech Conference", "New York", datetime.now(), datetime.now() + timedelta(hours=2))
    event_manager.add_attendee("1", "john.doe@example.com")
    event_manager.add_attendee("1", "jane.doe@example.com")
    print(event_manager.read_event("1"))
    print(event_manager.get_weather_forecast("New York"))
    reminders = event_manager.check_event_reminder()
    if reminders:
        for reminder in reminders:
            print(reminder)