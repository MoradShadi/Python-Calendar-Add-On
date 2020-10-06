# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on "Enable the Google Calendar API"
# Configure your OAuth client - select "Desktop app", then proceed
# Click on "Download Client Configuration" to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the "View your calendars" permission request.


# Students must have their own api key
# No test cases needed for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function

from dateutil.relativedelta import relativedelta
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_api():
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(api, starting_time, number_of_events):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if number_of_events <= 0:
        raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()

    return events_result.get('items', [])

    # Add your methods here.


def get_year_past_events(api, starting_time, number_of_years):
    """
    (Written for functionality 1)
    Given a fixed number of years, prints the start and name of past events
    that have occurred on the user's calendar over the span of the past specified year(s) up
    till today.
    """

    new_min = (datetime.datetime.fromisoformat(starting_time[:-1]) -
               relativedelta(years=+number_of_years)).isoformat() + 'Z'

    if number_of_years <= 0:
        raise ValueError("Number of years must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=new_min,
                                      timeMax=starting_time, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def get_year_future_events(api, starting_time, number_of_years):
    """
    (Written for functionality 2)
    Given a fixed number of years, prints the start and name of upcoming
    events that are scheduled on the user's calendar from today over the span of the
    next specified year(s).
    """
    new_max = (datetime.datetime.fromisoformat(starting_time[:-1]) +
               relativedelta(years=+number_of_years)).isoformat() + 'Z'

    if number_of_years <= 0:
        raise ValueError("Number of years must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      timeMax=new_max, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def get_specific_time_events(api, year, month=0, day=0):
    """
    (Written for functionality 3)
    Given a year, month, and day, prints the start and name of the events
    that occur on that date. The month and day inputs are optional, meaning that
    if a day input is not provided, all events that occur in the specific year's
    month will be printed. Likewise, if the day and month inputs are both not provided,
    all events that occur in the specific year will be printed.
    """
    if year <= 0:
        raise ValueError("Invalid year input.")

    # If month and day are not provided, print all events in the year
    if month == 0 and day == 0:
        start_time = (datetime.datetime.utcnow().replace(year=year, month=1, day=1, hour=0, minute=0, second=0,
                                                         microsecond=0))
        end_time = (start_time + relativedelta(years=+1))
    # If only day is not provided, print all events in the year's month
    elif day == 0:
        start_time = (datetime.datetime.utcnow().replace(year=year, month=month, day=1, hour=0, minute=0, second=0,
                                                         microsecond=0))
        end_time = (start_time + relativedelta(months=+1))
    # If all are given, print events in specific date
    else:
        start_time = (datetime.datetime.utcnow().replace(year=year, month=month, day=day, hour=0, minute=0, second=0,
                                                         microsecond=0))
        end_time = (start_time + relativedelta(days=+1))

    start_time = start_time.isoformat() + "Z"
    end_time = end_time.isoformat() + "Z"

    events_result = api.events().list(calendarId='primary', timeMin=start_time,
                                      timeMax=end_time, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def search_event(api, keyword):
    """
    (Written for functionality 4)
    Searches through the user's calendar for events that contain the specified
    keyword and returns them.
    """
    events_result = api.events().list(calendarId='primary', q=keyword,
                                      singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def delete_event(api, event_id):
    """
    (Written for functionality 5)
    Deletes events in the user's calendar based on the given ID.
    """
    try:
        api.events().delete(calendarId='primary', eventId=event_id).execute()
    except HttpError as e:
        raise e
    else:
        return True


def delete_event_by_name(api, event_name):
    """
    (Written for functionality 5)
    Deletes events in the user's calendar based on the given name.
    """
    found = False
    res = search_event(api, event_name)
    for item in res:
        found = True
        delete_event(api, item['id'])
    if found == False:
        raise ProcessLookupError("No events with that name")

def main():
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    
    # events = get_upcoming_events(api, time_now, 10)
    # events = get_year_past_events(api, time_now, 5)
    events = get_year_future_events(api, time_now, 2)
    #events = get_specific_time_events(api, 2020, 8, 17)
    #events = search_event(api, 'SanityCheck')
    #delete_event(api,'test1')
    
    if not events:
        print('No events found.')
    for event in events:
        Reminders = ""
        start = event['start'].get('dateTime', event['start'].get('date'))
        if event['reminders'].get('useDefault') == True:
            Reminders += "{Time: 10 minutes before, Method: pop-up}"
        else:
            for reminder in event['reminders'].get('overrides'):
                Reminders += "{Time: "
                Reminders += str(reminder['minutes'])
                Reminders += " minutes before, Method: "
                Reminders += str(reminder['method'])
                Reminders += "}"
        print(start, event['summary'], "| Reminders -> ", Reminders)
    #delete_event_by_name(api, "test1")


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()
