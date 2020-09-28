import unittest
from unittest.mock import Mock
import Calendar
# Add other imports here if needed


class CalendarTest(unittest.TestCase):
    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"
        
        mock_api = Mock()
        events = Calendar.get_upcoming_events(mock_api, time, num_events) #creates a mock of the calendar api object so it can be varried safely
                                                                          #instead of the actual calendar.
        
        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1) # asserts that the call has been made once.
        
        args, kwargs = mock_api.events.return_value.list.call_args_list[0] # assigns the parameter list at index 0 (only list in this case) to
                                                                           # variables so they can be used for comparison later.
    
        self.assertEqual(kwargs['maxResults'], num_events) #asserts that the number of events specified is equal to the one found at the query.

        #tests if an exeption is raised when the number of events entered is less than 1
        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_upcoming_events(mock_api, time, 0)
            
        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_upcoming_events(mock_api, time, -1)


    # Add more test cases here
    def test_get_past_years_events(self):
        start_time = "2020-09-28T00:00:00.000000Z"
        num_years = 2

        mock_api = Mock()
        events = Calendar.get_year_past_events(mock_api, start_time, num_years)#creates a mock of the calendar api object so it can be varried safely
                                                                              #instead of the actual calendar.
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]# assigns the parameter list at index 0 (only list in this case) to
                                                                        # variables so they can be used for comparison later.

        # Tests that we are querying for events from at least 2 years ago
        self.assertEqual(int(kwargs['timeMax'][:4]) - int(kwargs['timeMin'][:4]), num_years)

        #tests if an exeption is raised when the number of events entered is less than 1
        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_year_past_events(mock_api, start_time, 0)
            
        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_year_past_events(mock_api, start_time, -1)

def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
