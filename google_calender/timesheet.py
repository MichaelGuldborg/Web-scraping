from __future__ import print_function

import csv
import os.path
import pickle
from datetime import datetime

from dateutil import parser
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def get_creds():
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
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    print('Fetching credentials')
    creds = get_creds()
    service = build('calendar', 'v3', credentials=creds)

    name_default = "Michael Guldborg"

    calendar_id_work = "5drdnd66pka1v7m5n2o7usn1n0@group.calendar.google.com"
    calendar_id_sidecourt = "qmb4l18ht68lehg6mgrdv9o2b8@group.calendar.google.com"
    calender_id_default = calendar_id_sidecourt

    # Define Caleder API request params
    name = name_default  # input("Name:") or name_default
    calendarId = calender_id_default  # input("CalendarId:") or calender_id_default
    timeMin = datetime(2019, 2, 19, 00, 00, 00).isoformat() + 'Z'  # 'Z' indicates UTC time
    timeMax = datetime(2019, 3, 20, 23, 59, 00).isoformat() + 'Z'  # 'Z' indicates UTC time
    # now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    print("\nHello, {}".format(name))
    print("You picked the calender with id:\n{}\n".format(calendarId))

    # Call the Calendar API
    events_response = service.events().list(calendarId=calendarId, orderBy='startTime', timeMin=timeMin,
                                            timeMax=timeMax, singleEvents=True).execute()
    print("Fetched events from: \"{}\"".format(events_response['summary']))
    print("From:\t{}\nTo:  \t{}\n".format(timeMin, timeMax))

    output_file = open('time_sheet.csv', mode='w', newline='')  # to prevent csv writer making double newline
    # output_file.write("\"sep=,\"\n") # tell excel to parse with ',' as separator
    output_file.write("{}\n".format(name))

    writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    events = events_response['items']
    duration_total = None
    for event in events:
        summary = event['summary']
        #        if "MinEjendom".lower() not in summary.lower():
        #            continue

        start = parser.parse(event['start']['dateTime'])
        end = parser.parse(event['end']['dateTime'])

        date = start.date()
        start_time = "{:02d}:{:02d}".format(start.hour, start.minute)
        end_time = "{:02d}:{:02d}".format(end.hour, end.minute)
        duration = end - start

        duration_total = duration_total + duration if duration_total else duration
        print("{}, {}, {}, {}, {}".format(summary, date, start_time, end_time, duration))
        writer.writerow([date, start_time, end_time, duration])

    days = duration_total.days
    hours, remainder = divmod(duration_total.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print("days: {}, hours: {}, minutes: {}".format(days, hours, minutes))

    hours_total = days * 24 + hours + minutes / 60
    print("hours_total: {}".format(hours_total))
    writer.writerow(["", "", "", "Total", hours_total])


if __name__ == '__main__':
    main()
