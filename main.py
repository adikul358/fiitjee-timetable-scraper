import fiitjee_tt
import json
from datetime import datetime
import calendar
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def frmt_time(date, time):
    d = date.split(" ")
    for i in range(1, len(d)):
        d[i] = int(d[i])
    t = time.split(":")
    for i in range(len(t)):
        t[i] = int(t[i])
    return datetime.strftime(datetime(d[2], list(calendar.month_name).index(d[0]), d[1], t[0], t[1]), "%Y-%m-%dT%H:%M:%S")

def extract_events():
    with open("tt_data_file.json", 'r') as f:
        schd = json.load(f)
    events = []
    for day in schd:
        for clss in day['classes']:
            event = {}
            times = {'start' : frmt_time(day['date'], clss['start']), 'end' : frmt_time(day['date'], clss['end'])}
            event['summary'] = clss['name']
            event['start'] = {'dateTime' : times['start'], 'timeZone': 'Asia/Kolkata'}
            event['end'] = {'dateTime' : times['end'], 'timeZone': 'Asia/Kolkata'}
            event['colorId'] = fiitjee_tt.subject_color[clss['name']]
            event['location'] = "FIITJEE Limited, B-4 Opp. Metro Station, Central Auto Market, Block B, Sector 16, Noida, Uttar Pradesh 201301, India"
            events.append(event)
            event['reminders'] = {'useDefault' : False, 'overrides' : [{'method' : 'popup', 'minutes' : 0}]}
    return events

creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server()
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

event = extract_events()
for e in event:
    strx = e["summary"] + "\t" +  e["start"]["dateTime"] + "\t" +  e["end"]["dateTime"]
    print(strx)
if input("Proceed Event Creation [y/n]: ") == 'y':
    bhap = 0
    for e in event:
        event = service.events().insert(calendarId='primary', body=e).execute()
        bhap += 1
        print(bhap, 'Event created')
