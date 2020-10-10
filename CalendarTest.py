import unittest
from unittest.mock import Mock
import Calendar

# Add other imports here if needed
import datetime
from dateutil.relativedelta import relativedelta
from googleapiclient.errors import HttpError


class CalendarTest(unittest.TestCase):
    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        # Creates a mock of the calendar api object so it can be varied safely instead of the actual calendar.
        events = Calendar.get_upcoming_events(mock_api, time, num_events)

        # Asserts that the call has been made once.
        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        # Assigns the parameter list at index 0 (only list in this case) to variables so they can be used for
        # comparison later.
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]

        # Asserts that the number of events specified is equal to the one found at the query.
        self.assertEqual(kwargs['maxResults'], num_events)

        # tests if an exception is raised when the number of events entered is less than 1
        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_upcoming_events(mock_api, time, 0)

        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_upcoming_events(mock_api, time, -1)

    # Add more test cases here
    def test_get_past_years_events_mock(self):
        start_time = datetime.datetime.utcnow().isoformat() + 'Z'
        num_years = 5

        mock_api = Mock()
        # Creates a mock of the calendar api object so it can be varied safely instead of the actual calendar.
        events = Calendar.get_year_past_events(mock_api, start_time, num_years)
        # Assigns the parameter list at index 0 (only list in this case) to variables so they can be used for
        # comparison later.
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]

        # Tests that we are accurately querying for events from at least 5 years ago (as specified)
        self.assertEqual(int(kwargs['timeMax'][:4]) - int(kwargs['timeMin'][:4]), num_years)

        # Tests if an exception is raised when the number of events entered is 0 or less
        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_year_past_events(mock_api, start_time, 0)

        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_year_past_events(mock_api, start_time, -1)

    def test_get_past_year_events(self):
        for iteration in range(3,7):
            start_time = datetime.datetime.utcnow().isoformat() + 'Z'
            num_years = iteration
            api = Calendar.get_calendar_api()

            if iteration <= 4:
                with self.assertRaises(ValueError):
                    Calendar.get_year_past_events(api, start_time, num_years)
                continue
            # Get the amount of events in the calendar before adding the new test event
            len_before_insert = len(Calendar.get_year_past_events(api, start_time, num_years))

            # Inserts a test event that is num_years in the past
            body = {'summary': '__testing__', 'start': {'dateTime': (datetime.datetime.utcnow() - relativedelta(years=+num_years) + relativedelta(hours=+1)).isoformat() + "Z"},
                    'end': {'dateTime': (datetime.datetime.utcnow() - relativedelta(years=+num_years) + relativedelta(hours=+2)).isoformat() + "Z"}}
            api.events().insert(calendarId='primary', body=body).execute()

            # Ensure that the inserted test event num_years in the past can be obtained
            self.assertEqual(len(Calendar.get_year_past_events(api, start_time, num_years)), len_before_insert+1)
            # Deletes the created event
            Calendar.delete_event_by_name(api, '__testing__')

    def test_get_future_years_events_mock(self):
        start_time = datetime.datetime.utcnow().isoformat() + 'Z'
        num_years = 2

        mock_api = Mock()
        # Creates a mock of the calendar api object so it can be varied safely instead of the actual calendar.
        events = Calendar.get_year_future_events(mock_api, start_time, num_years)
        # Assigns the parameter list at index 0 (only list in this case) to variables so they can be used for
        # comparison later.
        args, kwargs = mock_api.events.return_value.list.call_args_list[0]

        # Tests that we are accurately querying for events from at least next 2 years (as specified)
        self.assertEqual(int(kwargs['timeMax'][:4]) - int(kwargs['timeMin'][:4]), num_years)

        # Tests if an exception is raised when the number of events entered is 0 or less
        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_year_past_events(mock_api, start_time, 0)

        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_year_past_events(mock_api, start_time, -1)

    def test_get_future_year_events(self):
        for iteration in range(-2,4):
            start_time = datetime.datetime.utcnow().isoformat() + 'Z'
            num_years = iteration
            api = Calendar.get_calendar_api()

            if num_years <= 1:
                with self.assertRaises(ValueError):
                    Calendar.get_year_future_events(api, start_time, num_years)
                continue
            # Get the amount of events in the calendar before adding the new test event
            len_before_insert = len(Calendar.get_year_future_events(api, start_time, num_years))

            # Inserts a test event that is num_years in the future
            body = {'summary': '__testing__', 'start': {'dateTime': (datetime.datetime.utcnow() + relativedelta(years=+num_years) - relativedelta(hours=+2)).isoformat() + "Z"},
                    'end': {'dateTime': (datetime.datetime.utcnow() + relativedelta(years=+num_years) - relativedelta(hours=+1)).isoformat() + "Z"}}
            api.events().insert(calendarId='primary', body=body).execute()

            # Ensure that the inserted test event num_years in the future can be obtained
            self.assertEqual(len(Calendar.get_year_future_events(api, start_time, num_years)), len_before_insert+1)
            # Deletes the created event
            Calendar.delete_event_by_name(api, '__testing__')

    def test_get_specific_time_events(self):
        api = Calendar.get_calendar_api()
        year = 2020
        month = 7
        day = 15

        # gets the event in the whole year
        year_events_before = len(Calendar.get_specific_time_events(api,year))
        
        # gets the events in given month
        month_events_before = len(Calendar.get_specific_time_events(api,year,month))

        # gets the events in given day
        day_events_before = len(Calendar.get_specific_time_events(api, year,month,day))

        # gets the events on different day for checking later
        check_day_events_before = len(Calendar.get_specific_time_events(api, year,month,9))

        # Inserts a test event in same given day
        start_time = (datetime.datetime.utcnow().replace(year=year, month=month, day=day, hour=0, minute=0, second=0,
                                                         microsecond=0))
        end_time = (start_time + relativedelta(days=+1))
        start_time = start_time.isoformat() + "Z"
        end_time = end_time.isoformat() + "Z"
        body = {'summary': '__testing__', 'start': {'dateTime': start_time},
                'end': {'dateTime': end_time}}
        api.events().insert(calendarId='primary', body=body).execute()

        # check updated number of events in year
        self.assertEqual(len(Calendar.get_specific_time_events(api,year)), year_events_before + 1)

        # check updated number of events in month
        self.assertEqual(len(Calendar.get_specific_time_events(api,year,month)), month_events_before + 1)

        # check updated number of events in day
        self.assertEqual(len(Calendar.get_specific_time_events(api,year,month,day)), day_events_before + 1)

        # check that others days havent changed
        self.assertEqual(len(Calendar.get_specific_time_events(api,year,month,9)), check_day_events_before)

        # removes the test event added
        Calendar.delete_event_by_name(api, '__testing__')
        
        # tests if an exception is raised when year entered is 0 or less
        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_specific_time_events(mock_api, 0)

        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_specific_time_events(mock_api, -1)

        # tests exception for invalid month entry
        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_specific_time_events(mock_api, 2020,-1)

        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_specific_time_events(mock_api, 2020,15)

        # tests exception for invalid day entry
        mock_api = Mock()
        with self.assertRaises(ValueError):
            # this one checks 30th day in Feb which doesnt exist, even in leap year
            Calendar.get_specific_time_events(mock_api, 2020, 2, 30)

        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_specific_time_events(mock_api, 2020, 11, 40)

        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_specific_time_events(mock_api, 2020, 11, -2)

    def test_search_event(self):
        api = Calendar.get_calendar_api()

        # Ensures that the results obtained when querying using the self written method matches the
        # results when querying using Google Calendar API methods
        self.assertEqual(Calendar.search_event(api, 'vnjfnvjfenvjefnvienbfivbefbvhejbf'), api.events().list(calendarId='primary', q='vnjfnvjfenvjefnvienbfivbefbvhejbf').execute().get('items', []))
        self.assertEqual(Calendar.search_event(api, 'test'), api.events().list(calendarId='primary', q='test').execute().get('items', []))
        self.assertEqual(Calendar.search_event(api, '123456789'), api.events().list(calendarId='primary', q='123456789').execute().get('items', []))

        # Get the amount of events in the calendar when searching before adding the new test event
        len_before_insert = len(Calendar.search_event(api, '__testing__'))

        # Adds a new test event
        body = {'summary': '__testing__', 'start': {'dateTime': datetime.datetime.utcnow().isoformat() + "Z"},
                'end': {'dateTime': (datetime.datetime.utcnow() + relativedelta(hours=+2)).isoformat() + "Z"}}
        api.events().insert(calendarId='primary', body=body).execute()

        # Ensures that the inserted event can be obtained using the search function
        self.assertEqual(len(Calendar.search_event(api, '__testing__')), len_before_insert+1)
        # Deletes the created event
        Calendar.delete_event_by_name(api, '__testing__')

    def test_delete_event_by_name(self):
        api = Calendar.get_calendar_api()
        # tests if exception is correctly raised when trying to delete event that doesnt exist
        with self.assertRaises(ProcessLookupError):
            Calendar.delete_event_by_name(api, '__test1__')

        # prepares information for test event to be added to calendar   
        body = {'summary': '__test1__', 'start': {'dateTime': '2020-10-28T09:00:00-07:00'}, 'end': {'dateTime': '2020-10-28T17:00:00-07:00'}}
        # Inserts an event to the calendar so it can be deleted later on to test if function carries out correctly
        api.events().insert(calendarId='primary', body=body).execute()
        # tests that the event is deleted successfully with no issues
        self.assertEqual(Calendar.delete_event_by_name(api, '__test1__'), None)
        # test again to make sure that an error is raised after the event has been deleted
        with self.assertRaises(ProcessLookupError):
            Calendar.delete_event_by_name(api, '__test1__')
        
        
def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
