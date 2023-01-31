'''
A cool project that will load all calendar events and print them out

By Cayden Wright
29 January 2023
'''

from __future__ import print_function

from datetime import datetime
from datetime import date
import pytz
from tzlocal import get_localzone
import os.path
from print_helper import print_event

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def load_api():
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
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
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
    return event['start'].get('dateTime')


def get_events_from_file(filename, service):
    '''
    returns all upcoming events from a given file containing calendar IDs one per line

    filename:string of where to find said file
    service:object returned by load_api
    '''

    # empty list to store the calendar IDs
    calendar_ids = []
    # empty list to store all events in
    events = []

    # create naive time objects for 12AM today and 11:59 today, thus to include all events for today
    this_morning = datetime.combine(date.today(), datetime.min.time())
    tonight = datetime.combine(date.today(), datetime.max.time())
    #localize time objects
    timezone = get_localzone()
    this_morning = timezone.localize(this_morning)
    tonight = timezone.localize(tonight)
    #serialize time objects, remove offsets too
    this_morning=this_morning.astimezone(pytz.utc).isoformat()[:-6]+"Z"
    tonight = tonight.astimezone(pytz.utc).isoformat()[:-6]+"Z"
    # read ids from file
    with open(filename) as file:
        for line in file:
            calendar_ids.append(line.strip())

    print(calendar_ids)
    # then get events for every calendar specified and append to list
    for id in calendar_ids:
        #query is run here
        events_result = service.events().list(calendarId=id, singleEvents=True,
                                              orderBy='startTime', maxResults=5,
                                              timeMax=tonight, timeMin=this_morning,
                                              ).execute()
        events += events_result.get('items', [])

        events.sort(key=event_start_sorting_key)

    # if not events:
    #     print("NO EVENTS")
    # for event in events:
    #     start = event['start'].get('dateTime')
    #     print(start, event['summary'])

    return events


def main():

    service = load_api()
    events = get_events_from_file("./calendar_ids.txt", service)
    for event in events:
        print_event(event)


if __name__ == '__main__':
    main()
