from __future__ import print_function

from datetime import datetime
from datetime import date
import pytz
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def load_calendar_api():
    '''
    starts the Gcal API - shamelessly stole most of this code from a google example
    https://developers.google.com/calendar/api/quickstart/python

    Returns an object (i think?) called service that represents the API
    '''
    scopes = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/home/pi/raspberry/receipt_planner/token.json'):
        creds = Credentials.from_authorized_user_file('/home/pi/raspberry/receipt_planner/token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/pi/raspberry/receipt_planner/credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('/home/pi/raspberry/receipt_planner/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        return service

    except HttpError as error:
        print('An HTTP error occurred: %s' % error)
        return None


def event_start_sorting_key(event):
    '''
    used for sorting the list of events
    '''
    if event['start'].get('dateTime') is None:
        return event['start'].get('date')
    return event['start'].get('dateTime')


def get_events_from_file(filename):
    service = load_calendar_api()
    '''
    returns all upcoming events from a given file containing calendar IDs one per line

    filename:string of where to find said file
    service:object returned by load_api
    '''

    # empty list to store the calendar IDs
    calendar_ids = []
    # empty list to store all events in
    events = []

    # create aware time objects for 12AM today and 11:59 today, thus to include all events for today
    this_morning = datetime.combine(date.today(), datetime.min.time(), tzinfo=None)
    tonight = datetime.combine(date.today(), datetime.max.time(), tzinfo=None)
    # serialize time objects, remove offsets too
    this_morning = this_morning.astimezone(pytz.utc).isoformat()[:-6]+"Z"
    tonight = tonight.astimezone(pytz.utc).isoformat()[:-6]+"Z"
    # read ids from file
    with open(filename) as file:
        for line in file:
            calendar_ids.append(line.strip())
    # then get events for every calendar specified and append to list
    for id in calendar_ids:
        # query is run here
        events_result = service.events().list(calendarId=id, singleEvents=True,  # type:ignore
                                              orderBy='startTime', maxResults=5,
                                              timeMax=tonight, timeMin=this_morning,
                                              ).execute()
        events += events_result.get('items', [])
    events.sort(key=event_start_sorting_key)
    return events
