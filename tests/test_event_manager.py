import unittest
from unittest.mock import patch
from event_manager import EventManager

class TestEventManager(unittest.TestCase):

    def setUp(self):
        self.event_manager = EventManager()
        self.sample_event = {
            'title': 'Sample Event',
            'description': 'This is a sample event',
            'location': 'Sample Location',
            'date': '2023-01-01'
        }

    def test_event_creation(self):
        created_event = self.event_manager.create_event(**self.sample_event)
        self.assertIsNotNone(created_event)
        self.assertEqual(created_event['title'], self.sample_event['title'])

    def test_event_update(self):
        created_event = self.event_manager.create_event(**self.sample_event)
        update_data = {'title': 'Updated Sample Event'}
        updated_event = self.event_manager.update_event(created_event['id'], **update_data)
        self.assertEqual(updated_event['title'], update_data['title'])

    def test_event_deletion(self):
        created_event = self.event_manager.create_event(**self.sample_event)
        deletion_result = self.event_manager.delete_event(created_event['id'])
        self.assertTrue(deletion_result)

    def test_event_creation_no_title(self):
        incomplete_event = self.sample_event.copy()
        del incomplete_event['title']
        with self.assertRaises(ValueError):
            self.event_manager.create_event(**incomplete_event)

    @patch.dict('os.environ', {'MAX_EVENTS': '10'})
    def test_max_event_limit(self):
        max_events = int(os.environ.get('MAX_EVENTS', 10))
        for _ in range(max_events):
            self.event_manager.create_event(**self.sample_event)
        with self.assertRaises(RuntimeError):
            self.event_manager.create_event(**self.sample_event)

    @patch('event_manager.EventManager.send_event_invitations')
    def test_event_invitations_sent(self, mock_send_invitations):
        self.event_manager.create_event(**self.sample_event)
        mock_send_invitations.assert_called_once()

    def tearDown(self):
        self.event_manager.delete_all_events()

if __name__ == '__main__':
    unittest.main()