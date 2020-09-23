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
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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


def get_year_future_events(api, starting_time, number_of_years):
    """
    Given a fixed number of years, prints the start and name of upcoming (future)
    events that are scheduled on the user's calendar from today to the next specified
    year.
    """
    new_max = (datetime.datetime.utcnow() + datetime.timedelta(days=365*number_of_years)).isoformat() + 'Z'
    if number_of_years <= 0:
        raise ValueError("Number of years must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      timeMax=new_max, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def get_year_past_events(api, starting_time, number_of_years):
    """
    Given a fixed number of years, prints the start and name of past events
    that have occurred on the user's calendar during the specified past years up
    till today.
    """
    new_min = (datetime.datetime.utcnow() - datetime.timedelta(days=365*number_of_years)).isoformat() + 'Z'
    if number_of_years <= 0:
        raise ValueError("Number of years must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=new_min,
                                      timeMax=starting_time, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def search_event(api, keyword):
    """
    Searches through the user's calendar for events that contain the specified
    keyword and returns them.
    """
    events_result = api.events().list(calendarId='primary', q=keyword,
                                      singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def delete_event(api, event_id):
    """
    Deletes events in the user's calendar based on the given ID.
    """
    api.events().delete(calendarId='primary', eventId=event_id).execute()
    return True


def main():
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    events = get_upcoming_events(api, time_now, 10)
    # events = get_year_past_events(api, time_now, 5)
    # events = get_year_future_events(api, time_now, 2)
    # events = search_event(api, 'SanityCheck')

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()
