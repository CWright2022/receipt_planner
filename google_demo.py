from __future__ import print_function

import datetime
import os.path
import requests

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


def get_events_from_file(filename, service):
    '''
    returns all upcoming events from a given file
    containing calendar IDs one per line'''
    calendar_ids = []
    events = []

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    with open(filename) as file:
        for line in file:
            calendar_ids.append(line.strip())
    for id in calendar_ids:
        events_result = service.events().list(calendarId=id, timeMin=now,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])
        if not events:
            print("NO EVENTS")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
        print("DONE WITH THIS CALENDAR")


def main():

    service = load_api()
    get_events_from_file("./calendar_ids.txt", service)


if __name__ == '__main__':
    main()
