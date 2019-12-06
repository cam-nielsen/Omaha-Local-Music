from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
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

    service = build('calendar', 'v3', credentials=creds)

########################################################

    with open('shows.csv', mode='r') as csvFile:
        reader = csv.DictReader(csvFile)

        service.calendars().clear(calendarId='primary').execute()
        for row in reader:
            event = {
                'summary': row['EventTitle'],
                'location': row['Location'],
                'description': row['Link'],
                'start': {
                    'dateTime': row['StartDateTime'][:10]+'T'+row['StartDateTime'][-8:],
                    'timeZone': 'America/Chicago'
                },
                'end': {
                    'dateTime': row['EndDateTime'][:10]+'T'+row['EndDateTime'][-8:],
                    'timeZone': 'America/Chicago'
                }
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            print('Event created: '+row['EventTitle']+' %s' % (event.get('htmlLink')))

    csvFile.close()

########################################################


if __name__ == '__main__':
    main()
