import unittest
from unittest.mock import patch, MagicMock
import os
from event_manager import EventManager

class TestEventManager(unittest.TestCase):

    def setUp(self):
        self.event_manager = EventManager()
        self.attendee_manager = self.event_manager.attendee_manager
        self.sample_event = {
            'title': 'Sample Event',
            'description': 'This is a sample event',
            'location': 'Sample Location',
            'date': '2023-01-01'
        }
        self.sample_attendee = {
            'name': 'John Doe',
            'email': 'johndoe@example.com',
        }

    def test_event_creation(self):
        created_event = self.event_manager.create_event(**self.sample_event)
        self.assertIsNotNone(created_event)
        self.assertEqual(created_event['title'], self.sample_event['title'])

    def test_add_attendee_to_event(self):
        created_event = self.event_manager.create_event(**self.sample_event)
        self.assertIsNotNone(created_event)
        add_result = self.attendee_manager.add_attendee(event_id=created_event['id'], **self.sample_attendee)
        self.assertTrue(add_result)

    def test_remove_attendee_from_event(self):
        created_event = self.event_manager.create_event(**self.sample_event)
        add_result = self.attendee_manager.add_attendee(event_id=created_event['id'], **self.sample_attendee)
        self.assertTrue(add_result)
        remove_result = self.attendee_manager.remove_attendee(email=self.sample_attendee['email'])
        self.assertTrue(remove_result)

    @patch('event_manager.EventManager.notify_attendees')
    def test_notify_attendees(self, mock_notify_attendees):
        created_event = self.event_manager.create_event(**self.sample_event)
        self.attendee_manager.add_attendee(event_id=created_event['id'], **self.sample_attendee)
        self.event_manager.notify_attendees(created_event['id'], "Event Cancelled")
        mock_notify_attendees.assert_called_once()

    def test_search_event_by_date(self):
        self.event_manager.create_event(**self.sample_event)
        search_results = self.event_manager.search_events_by_date('2023-01-01')
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0]['date'], self.sample_event['date'])

    def tearDown(self):
        self.event_manager.delete_all_events()

if __name__ == '__main__':
    unittest.main()