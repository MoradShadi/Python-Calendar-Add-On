import sys
import unittest
from io import StringIO
from unittest.mock import Mock, patch
import Calendar

# Add other imports here if needed
import datetime
from dateutil.relativedelta import relativedelta


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
        
        for i in range(4, 7):
            start_time = datetime.datetime.utcnow().isoformat() + 'Z'
            num_years = i

            mock_api = Mock()
            if num_years <= 4:
                with self.assertRaises(ValueError):
                    Calendar.get_year_past_events(mock_api, start_time, num_years)
                continue
            # Creates a mock of the calendar api object so it can be varied safely instead of the actual calendar.
            events = Calendar.get_year_past_events(mock_api, start_time, num_years)

            # Asserts that the call has been made once.
            self.assertEqual(
                mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

            # Assigns the parameter list at index 0 (only list in this case) to variables so they can be used for
            # comparison later.
            args, kwargs = mock_api.events.return_value.list.call_args_list[0]

            # Tests that we are accurately querying for events from at least 5 years ago (as specified)
            self.assertEqual(int(kwargs['timeMax'][:4]) - int(kwargs['timeMin'][:4]), num_years)

    def test_get_past_year_events(self):
        for iteration in range(3, 7):
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

        for i in range(1, 4):
            start_time = datetime.datetime.utcnow().isoformat() + 'Z'
            num_years = i

            mock_api = Mock()
            if num_years <= 1:
                with self.assertRaises(ValueError):
                    Calendar.get_year_past_events(mock_api, start_time, num_years)
                continue
            # Creates a mock of the calendar api object so it can be varied safely instead of the actual calendar.
            events = Calendar.get_year_future_events(mock_api, start_time, num_years)

            # Asserts that the call has been made once.
            self.assertEqual(
                mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

            # Assigns the parameter list at index 0 (only list in this case) to variables so they can be used for
            # comparison later.
            args, kwargs = mock_api.events.return_value.list.call_args_list[0]

            # Tests that we are accurately querying for events from at least next 2 years (as specified)
            self.assertEqual(int(kwargs['timeMax'][:4]) - int(kwargs['timeMin'][:4]), num_years)

    def test_get_future_year_events(self):
        for iteration in range(-2, 4):
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
        year_events_before = len(Calendar.get_specific_time_events(api, year))
        
        # gets the events in given month
        month_events_before = len(Calendar.get_specific_time_events(api, year, month))

        # gets the events in given day
        day_events_before = len(Calendar.get_specific_time_events(api, year, month, day))

        # gets the events on different day for checking later
        check_day_events_before = len(Calendar.get_specific_time_events(api, year, month, 9))

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
        self.assertEqual(len(Calendar.get_specific_time_events(api, year)), year_events_before + 1)

        # check updated number of events in month
        self.assertEqual(len(Calendar.get_specific_time_events(api, year, month)), month_events_before + 1)

        # check updated number of events in day
        self.assertEqual(len(Calendar.get_specific_time_events(api, year, month, day)), day_events_before + 1)

        # check that others days haven't changed
        self.assertEqual(len(Calendar.get_specific_time_events(api, year, month, 9)), check_day_events_before)

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
            Calendar.get_specific_time_events(mock_api, 2020, -1)

        mock_api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_specific_time_events(mock_api, 2020, 15)

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

    # This test was created to test out a menu that takes in user input. However, we later
    # found out that we do not have to write out tests for menus, but since it has already
    # been written (and took a lot of time), it is left as it is.
    def test_navigate_calendar(self):
        api = Calendar.get_calendar_api()
        year = 2100
        month = 7
        day = 15

        # Inserts a test event in same given day
        start_time = (datetime.datetime.utcnow().replace(year=year, month=month, day=day, hour=0, minute=0, second=0,
                                                         microsecond=0))
        end_time = (start_time + relativedelta(days=+1))
        start_time = start_time.isoformat() + "Z"
        end_time = end_time.isoformat() + "Z"
        body = {'summary': '__testing__', 'start': {'dateTime': start_time},
                'end': {'dateTime': end_time}}
        api.events().insert(calendarId='primary', body=body).execute()

        # -----User input test 1 - Testing showing events by providing year-----
        old_stdout = sys.stdout
        # Suppresses the printing in the menu so that it does not show when conducting the test
        suppress_text = StringIO()
        sys.stdout = suppress_text

        # Input provided to function on every occurrence of input(): 1, 2100, 1, 4
        # This represents getting events from the year 2100, selecting the first event to view detailed
        # information, then exiting the menu
        sys.stdin = StringIO("1\n2100\n1\n4")
        Calendar.navigate_calendar(api)
        sys.stdin = sys.__stdin__

        sys.stdout = old_stdout

        menu_year = "------------------------------------\n" + \
                    "Welcome to the calendar, please choose a date format to view events.\n" + \
                    "1. Year \n" + "2. Year + Month \n" + "3. Year + Month + Date \n" + "4. Exit\n" + \
                    "------------------------------------\nEnter option: Please input year: \nResults:"

        # Ensures that the starting menu is correctly printed
        self.assertEqual(suppress_text.getvalue()[0:243], menu_year)
        # Ensures the event can be obtained and is correctly printed
        self.assertEqual(suppress_text.getvalue()[246:345],
                         "1 : 2100-07-15T08:00:00+08:00 __testing__ | Reminders ->  "
                         "{Time: 10 minutes before, Method: pop-up}")
        # Ensures that the detailed information is printed correctly by checking its summary
        self.assertEqual(suppress_text.getvalue()[729:749], "Summary: __testing__")

        # -----User input test 2 - Testing showing events by providing year and month-----
        old_stdout = sys.stdout
        # Suppresses the printing in the menu so that it does not show when conducting the test
        suppress_text = StringIO()
        sys.stdout = suppress_text

        # Input provided to function on every occurrence of input(): 2, 2100, 7, 1, 4
        # This represents getting events from July of the year 2100, selecting the first event to view detailed
        # information, then exiting the menu
        sys.stdin = StringIO("2\n2100\n7\n1\n4")
        Calendar.navigate_calendar(api)
        sys.stdin = sys.__stdin__

        sys.stdout = old_stdout

        menu_year_month = "------------------------------------\n" + \
                          "Welcome to the calendar, please choose a date format to view events.\n" + \
                          "1. Year \n" + "2. Year + Month \n" + "3. Year + Month + Date \n" + "4. Exit\n" + \
                          "------------------------------------\nEnter option: Please input year: Please input " \
                          "month: \nResults:"

        # Ensures that the starting menu is correctly printed
        self.assertEqual(suppress_text.getvalue()[0:263], menu_year_month)
        # Ensures the event can be obtained and is correctly printed
        self.assertEqual(suppress_text.getvalue()[266:365],
                         "1 : 2100-07-15T08:00:00+08:00 __testing__ | Reminders ->  "
                         "{Time: 10 minutes before, Method: pop-up}")
        # Ensures that the detailed information is printed correctly by checking its summary
        self.assertEqual(suppress_text.getvalue()[749:769], "Summary: __testing__")

        # -----User input test 3 - Testing showing events by providing year, month, and day-----
        old_stdout = sys.stdout
        # Suppresses the printing in the menu so that it does not show when conducting the test
        suppress_text = StringIO()
        sys.stdout = suppress_text

        # Input provided to function on every occurrence of input(): 3, 2100, 7, 15, 1, 4
        # This represents getting events from 15th July of the year 2100, selecting the first event to view detailed
        # information, then exiting the menu
        sys.stdin = StringIO("3\n2100\n7\n15\n1\n4")
        Calendar.navigate_calendar(api)
        sys.stdin = sys.__stdin__

        sys.stdout = old_stdout

        menu_year_month_day = "------------------------------------\n" + \
                              "Welcome to the calendar, please choose a date format to view events.\n" + \
                              "1. Year \n" + "2. Year + Month \n" + "3. Year + Month + Date \n" + "4. Exit\n" + \
                              "------------------------------------\nEnter option: Please input year: Please input " \
                              "month: Please input day: \nResults:"

        # Ensures that the starting menu is correctly printed
        self.assertEqual(suppress_text.getvalue()[0:281], menu_year_month_day)
        # Ensures the event can be obtained and is printed correctly
        self.assertEqual(suppress_text.getvalue()[284:383],
                         "1 : 2100-07-15T08:00:00+08:00 __testing__ | Reminders ->  {Time: 10 minutes before, "
                         "Method: pop-up}")
        # Ensures that the detailed information is printed correctly by checking its summary
        self.assertEqual(suppress_text.getvalue()[767:787], "Summary: __testing__")
        Calendar.delete_event_by_name(api, '__testing__')

        # -----User input test 4 - Testing events that uses date instead of datetime-----
        body = {'summary': '__testing__', 'start': {'date': '2100-07-15'},
                'end': {'date': '2100-07-16'}, 'reminders': {'useDefault': False, 'overrides': [
                {'method': 'email', 'minutes': 24 * 60}, {'method': 'popup', 'minutes': 10}, ], }}
        api.events().insert(calendarId='primary', body=body).execute()

        old_stdout = sys.stdout
        # Suppresses the printing in the menu so that it does not show when conducting the test
        suppress_text = StringIO()
        sys.stdout = suppress_text

        # Input provided to function on every occurrence of input(): 1, 2100, 1, 4
        # This represents getting events from the year 2100, selecting the first event to view detailed
        # information, then exiting the menu
        sys.stdin = StringIO("1\n2100\n1\n4")
        Calendar.navigate_calendar(api)
        sys.stdin = sys.__stdin__

        sys.stdout = old_stdout
        # Ensures that creating an event with date instead of datetime works as well by testing the detailed information
        # shown
        self.assertEqual(suppress_text.getvalue()[852:869], "Start: 2100-07-15")

        # -----User input test 5 - Testing events that uses date instead of datetime-----
        old_stdout = sys.stdout
        # Suppresses the printing in the menu so that it does not show when conducting the test
        suppress_text = StringIO()
        sys.stdout = suppress_text

        # Input provided to function on every occurrence of input(): 1, 2200, 4
        # This represents getting events from the year 2200, selecting the first event to view detailed
        # information (For which there is none), then exiting the menu
        sys.stdin = StringIO("1\n2200\n4")
        Calendar.navigate_calendar(api)
        sys.stdin = sys.__stdin__

        sys.stdout = old_stdout
        # Ensures that the correct message is printed when there are no events found
        self.assertEqual(suppress_text.getvalue()[246:262], "No events found.")

        # Deletes the added event after testing
        Calendar.delete_event_by_name(api, '__testing__')

    # This test was created to test out a menu that takes in user input. However, we later
    # found out that we do not have to write out tests for menus, but since it has already
    # been written (and took a lot of time), it is left as it is.
    def test_navigate_event_error_input(self):
        api = Calendar.get_calendar_api()
        year = 2100
        month = 7
        day = 15

        # Inserts a test event in same given day
        start_time = (datetime.datetime.utcnow().replace(year=year, month=month, day=day, hour=0, minute=0, second=0,
                                                         microsecond=0))
        end_time = (start_time + relativedelta(days=+1))
        start_time = start_time.isoformat() + "Z"
        end_time = end_time.isoformat() + "Z"
        body = {'summary': '__testing__', 'start': {'dateTime': start_time},
                'end': {'dateTime': end_time}}
        api.events().insert(calendarId='primary', body=body).execute()

        # -----User input error test 1 - Testing inputting characters for a year input-----
        old_stdout = sys.stdout
        # Suppresses the printing in the menu so that it does not show when conducting the test
        suppress_text = StringIO()
        sys.stdout = suppress_text

        # Input provided to function on every occurrence of input(): 1, test, 4
        # This represents typing string for the year input (which is invalid)
        sys.stdin = StringIO("1\ntest\n4")
        Calendar.navigate_calendar(api)
        sys.stdin = sys.__stdin__

        sys.stdout = old_stdout
        # Ensures that the correct message is printed when characters are provided for the year input
        self.assertEqual(suppress_text.getvalue()[234:266], "Invalid input. Please try again.")

        # -----User input error test 2 - Testing providing out of bounds input when choosing to view detailed
        # information about an event-----
        old_stdout = sys.stdout
        # Suppresses the printing in the menu so that it does not show when conducting the test
        suppress_text = StringIO()
        sys.stdout = suppress_text

        # Input provided to function on every occurrence of input(): 1, 2100, 10, 4
        # This represents getting events from the year 2200, selecting the first event to view detailed
        # information, then exiting the menu
        sys.stdin = StringIO("1\n2100\n10\n4")
        Calendar.navigate_calendar(api)
        sys.stdin = sys.__stdin__

        sys.stdout = old_stdout
        # Ensures that the correct message is printed when an out of bounds input is provided when choosing to view
        # detailed information about an event
        self.assertEqual(suppress_text.getvalue()[463:495], "Invalid input. Please try again.")

        # Deletes the added event after testing
        Calendar.delete_event_by_name(api, '__testing__')

    # Patches the calendar search event function to mock_search_event
    @patch('googleapiclient.discovery.Resource')
    def test_search_event_mock(self, mock_calendar_api):
        # Sample event with the summary 'john'
        event_item = [{'kind': 'calendar#event', 'etag': '"3203969478692000"', 'id': '0m1rmn75frd3jpn2cd6ha3015p', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=MG0xcm1uNzVmcmQzanBuMmNkNmhhMzAxNXAgbWFibzAwMDNAc3R1ZGVudC5tb25hc2guZWR1', 'created': '2020-10-06T11:45:22.000Z', 'updated': '2020-10-06T11:45:22.831Z', 'summary': 'john', 'creator': {'email': 'mabo0003@student.monash.edu', 'self': True}, 'organizer': {'email': 'mabo0003@student.monash.edu', 'self': True}, 'start': {'dateTime': '2020-10-08T10:00:00+08:00'}, 'end': {'dateTime': '2020-10-08T10:30:00+08:00'}, 'iCalUID': '0m1rmn75frd3jpn2cd6ha3015p@google.com', 'sequence': 0, 'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 10}, {'method': 'email', 'minutes': 50}]}}]
        # Assigns the event to be returned when api.events.list.execute.get() is called
        mock_calendar_api.events.return_value.list.return_value.execute.return_value.get.return_value = event_item

        # Tests that the event is correctly returned when we search using keyword 'john' or any of its substrings
        self.assertEqual(Calendar.search_event(mock_calendar_api, 'john'), event_item)
        self.assertEqual(Calendar.search_event(mock_calendar_api, 'joh'), event_item)
        self.assertEqual(Calendar.search_event(mock_calendar_api, 'jo'), event_item)
        self.assertEqual(Calendar.search_event(mock_calendar_api, 'j'), event_item)

        # Tests that the event is not returned if we search using other keywords
        self.assertEqual(Calendar.search_event(mock_calendar_api, 'testing'), [])

    def test_search_event(self):
        api = Calendar.get_calendar_api()

        # Ensures that the results obtained when querying using the self written method matches the
        # results when querying using Google Calendar API methods
        self.assertEqual(Calendar.search_event(api, 'vnjfnvjfenvjefnvienbfivbefbvhejbf'), api.events().list(calendarId='primary', q='vnjfnvjfenvjefnvienbfivbefbvhejbf').execute().get('items', []))
        self.assertEqual(Calendar.search_event(api, 'test123'), api.events().list(calendarId='primary', q='test123').execute().get('items', []))
        self.assertEqual(Calendar.search_event(api, '123456789'), api.events().list(calendarId='primary', q='123456789').execute().get('items', []))
        # Get the amount of events in the calendar when searching before adding the new test event
        len_before_insert = len(Calendar.search_event(api, '__testing__'))

        # Adds a new test event
        body = {'summary': '__testing__', 'start': {'dateTime': datetime.datetime.utcnow().isoformat() + "Z"},
                'end': {'dateTime': (datetime.datetime.utcnow() + relativedelta(hours=+2)).isoformat() + "Z"}}
        api.events().insert(calendarId='primary', body=body).execute()

        # Ensures that the inserted event can be obtained using the search function
        self.assertEqual(len(Calendar.search_event(api, '__testing__')), len_before_insert+1)
        # test to ensure event can be found with name variations but not exact name
        self.assertEqual(len(Calendar.search_event(api, 'testing')), len_before_insert+1)
        self.assertEqual(len(Calendar.search_event(api, 'test')), len_before_insert+1)
        self.assertEqual(len(Calendar.search_event(api, '__test')), len_before_insert+1)
        self.assertEqual(len(Calendar.search_event(api, 'tes')), len_before_insert+1)
        self.assertEqual(len(Calendar.search_event(api, 'sting')), len_before_insert+1)
        self.assertEqual(len(Calendar.search_event(api, '__')), len_before_insert+1)
        # Deletes the created event
        Calendar.delete_event_by_name(api, '__testing__')

    @patch('Calendar.search_event')
    def test_delete_event_by_name_mock(self, mock_delete_event_by_name_search):
        # When deleting events, the function search_event is called to look for the event
        # to be deleted, we mock the return of the search_event to be a sample return
        mock_delete_event_by_name_search.return_value = [{'kind': 'calendar#event', 'etag': '"3205310083330000"', 'id': '2rf8r17o1jmier8f0eahofj2uo', 'status': 'confirmed', 'htmlLink': 'https://www.google.com/calendar/event?eid=MnJmOHIxN28xam1pZXI4ZjBlYWhvZmoydW8gd3RlbzAwMTFAc3R1ZGVudC5tb25hc2guZWR1', 'created': '2020-10-14T05:57:21.000Z', 'updated': '2020-10-14T05:57:21.665Z', 'summary': 'testing', 'creator': {'email': 'wteo0011@student.monash.edu', 'self': True}, 'organizer': {'email': 'wteo0011@student.monash.edu', 'self': True}, 'start': {'dateTime': '2020-10-14T15:30:00+08:00'}, 'end': {'dateTime': '2020-10-14T16:30:00+08:00'}, 'iCalUID': '2rf8r17o1jmier8f0eahofj2uo@google.com', 'sequence': 0, 'reminders': {'useDefault': True}}]
        mock_api = Mock()
        # Tests that the delete is successful if search returns something
        self.assertEqual(Calendar.delete_event_by_name(mock_api, 'testing'), True)

        # When deleting events, the function search_event is called to look for the event
        # to be deleted, we mock the return of the search_event to be empty
        mock_delete_event_by_name_search.return_value = []
        mock_api = Mock()
        # Tests that an error is raised if search does not return anything
        with self.assertRaises(ProcessLookupError):
            Calendar.delete_event_by_name(mock_api, 'testing')

    def test_delete_event_by_name(self):
        api = Calendar.get_calendar_api()
        # tests if exception is correctly raised when trying to delete event that doesnt exist
        with self.assertRaises(ProcessLookupError):
            Calendar.delete_event_by_name(api, '__test1__')

        # prepares information for test event to be added to calendar   
        body = {'summary': '__test1__',
                'start': {'dateTime': '2020-10-28T09:00:00-07:00'}, 'end': {'dateTime': '2020-10-28T17:00:00-07:00'}}
        # Inserts an event to the calendar so it can be deleted later on to test if function carries out correctly
        api.events().insert(calendarId='primary', body=body).execute()
        # tests that the event is deleted successfully with no issues
        self.assertEqual(Calendar.delete_event_by_name(api, '__test1__'), True)
        # test again to make sure that an error is raised after the event has been deleted
        with self.assertRaises(ProcessLookupError):
            Calendar.delete_event_by_name(api, '__test1__')

    def test_delete_event_reminder(self):
        api = Calendar.get_calendar_api()
        # tests if exception is correctly raised when trying to delete event that doesnt exist
        with self.assertRaises(IndexError):
            Calendar.delete_event_reminder(api, '__test1__', 0, 10)

        # prepares information for test event to be added to calendar
        body = {'summary': '__test1__',
                'start': {'dateTime': '2020-10-28T09:00:00-07:00'},
                'end': {'dateTime': '2020-10-28T17:00:00-07:00'},
                'reminders': {'useDefault': False, 'overrides': [{'method': 'popup', 'minutes': 20},
                                                                 {'method': 'popup', 'minutes': 30},
                                                                 {'method': 'popup', 'minutes': 180},
                                                                 {'method': 'popup', 'minutes': 500}], }}
        # Inserts an event to the calendar so it can be deleted later on to test if function carries out correctly
        api.events().insert(calendarId='primary', body=body).execute()

        Calendar.delete_event_reminder(api, '__test1__', 0, 20)

        test_event = Calendar.search_event(api, "__test1__")[0]
        for reminder in test_event['reminders'].get('overrides'):
            self.assertNotEqual(reminder['minutes'], 20)
        self.assertEqual(len(test_event['reminders'].get('overrides')), 3)

        with self.assertRaises(ProcessLookupError):
            Calendar.delete_event_reminder(api, '__test1__', 0, 1000)

        Calendar.delete_event_reminder(api, '__test1__', 0)
        test_event = Calendar.search_event(api, "__test1__")[0]
        self.assertEqual(test_event['reminders'].get('overrides'), None)

        Calendar.delete_event_by_name(api, '__test1__')

        # prepares information for test event to be added to calendar
        body = {'summary': '__test1__',
                'start': {'dateTime': '2020-10-28T09:00:00-07:00'},
                'end': {'dateTime': '2020-10-28T17:00:00-07:00'},
                'reminders': {'useDefault': True}}
        # Inserts an event to the calendar so it can be deleted later on to test if function carries out correctly
        api.events().insert(calendarId='primary', body=body).execute()

        Calendar.delete_event_reminder(api, '__test1__', 0, 100)
        test_event = Calendar.search_event(api, "__test1__")[0]
        self.assertEqual(test_event['reminders'].get('useDefault'), True)
        Calendar.delete_event_reminder(api, '__test1__', 0, 10)
        test_event = Calendar.search_event(api, "__test1__")[0]
        self.assertEqual(test_event['reminders'].get('useDefault'), False)

        Calendar.delete_event_by_name(api, '__test1__')


def main():
    # Create the test suite from the cases above.
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTest)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
