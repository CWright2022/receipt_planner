from __future__ import print_function
from datetime import * #type: ignore
import pytz

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']


def main():
    """Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('tasks', 'v1', credentials=creds)

        # get a list of the task lists

        task_lists = service.tasklists().list(maxResults=10).execute()
        task_lists = task_lists.get('items', [])

        if not task_lists:
            print('No task lists found.')
            return

        # create aware time objects for 12AM today and 11:59 today, thus to include all tasks for today
        this_morning = datetime.combine(date.today(), datetime.min.time(), tzinfo=None)
        tonight = datetime.combine(date.today(), datetime.max.time(), tzinfo=None)
        # serialize time objects, remove offsets too
        this_morning = this_morning.astimezone(pytz.utc).isoformat()[:-6]+"Z"
        tonight = tonight.astimezone(pytz.utc).isoformat()[:-6]+"Z"

        for list in task_lists:
            print(u'{0} ({1})'.format(list['title'], list['id']))
            tasks = service.tasks().list(tasklist=list['id'], dueMin=this_morning, dueMax=tonight).execute()
            tasks = tasks.get('items', [])
            for task in tasks:
                print(task['title'])

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
