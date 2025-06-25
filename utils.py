import os
import datetime
import pytz
import re
import pandas as pd
import pytz
import traceback

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

vancouver_tz = pytz.timezone('America/Vancouver')
names = ["Brian*", "Abdi*", "Emilyn*", "Ryan*", "Jordan", "Cindy*", "KC*", "Jojo*", "Christian*", "Troy*", "Tristan*", "Ian", "Sara"]
color_codes = {
    "Brian*": 1,
    "Abdi*": 2,
    "Emilyn*": 10,
    "Ryan*": 4,
    "Jordan": 5,
    "Cindy*": 6,
    "KC*": 7,
    "Jojo*": 8,
    "Christian*": 9,
    "Troy*": 3,
    "Tristan*": 11,
    "Ian": 1,
    "Work": 6,
    "Sara": 1
}

def remove_end_star(name: str) -> str:
    return name[:-1] if name.endswith('*') else name

def convert_to_24_hour(time_str):
    time_str = time_str.strip()
    period = time_str[-2:].upper()
    time_part = time_str[:-2].strip()
    if ':' in time_part:
        hour, minute = map(int, time_part.split(':'))
    else:
        hour, minute = int(time_part), 0
    if period == "PM" and hour != 12:
        hour += 12
    elif period == "AM" and hour == 12:
        hour = 0
    return hour, minute

def extract_initial_time(datetime_list):
    result = []
    for dt, time_range in datetime_list:
        hour, minute = convert_to_24_hour(time_range.split('-')[0].strip())
        new_datetime = dt.replace(hour=hour, minute=minute, second=0, microsecond=0)
        localized_dt = vancouver_tz.localize(new_datetime)
        result.append(localized_dt)
    return result

def get_calendar_service():
    creds_path = os.path.expanduser("/home/brian/Documents/BrainBot/brainbot-435923-912b44082a6f.json")
    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=["https://www.googleapis.com/auth/calendar"])
    return build("calendar", "v3", credentials=creds)

def upload_to_google_calendar(event_times, name):
    try:
        service = get_calendar_service()

        clean_name = remove_end_star(name)
        cal_id = "primary" if name == "Work" else \
            '24bc1af315ebd0c137d1172c5dba504e0f9bc6f6236d833b7c432b19c26dc909@group.calendar.google.com'
        if not event_times:
            print("No events to upload.")
            return

        earliest_local = min(event_times)
        time_min = earliest_local.astimezone(pytz.utc).isoformat().replace('+00:00', 'Z')

        existing_events = service.events().list(
            calendarId=cal_id,
            timeMin=time_min,
            timeMax=(datetime.datetime.utcnow() + datetime.timedelta(days=365)).isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        existing_event_keys = set(
            (
                remove_end_star(event['summary']),
                datetime.datetime.fromisoformat(event['start']['dateTime']).astimezone(vancouver_tz),
                datetime.datetime.fromisoformat(event['end']['dateTime']).astimezone(vancouver_tz)
            )
            for event in existing_events.get('items', [])
            if 'dateTime' in event['start'] and 'summary' in event and 'dateTime' in event['end']
        )

        for event_start_time in event_times:
            event_end_time = event_start_time + datetime.timedelta(hours=8)
            if event_end_time.date() > event_start_time.date():
                event_end_time = event_start_time.replace(hour=23, minute=59, second=59)

            base_event = {
                'summary': clean_name,
                'location': '9351 Bridgeport Rd, Richmond, BC V6X 1S3',
                'start': {'dateTime': event_start_time.isoformat(), 'timeZone': 'America/Vancouver'},
                'end': {'dateTime': event_end_time.isoformat(), 'timeZone': 'America/Vancouver'},
                'colorId': color_codes.get(name, 1)
            }

            if (clean_name, event_start_time, event_end_time) not in existing_event_keys:
                print(f"Uploading event: {clean_name} at {event_start_time}")
                service.events().insert(calendarId=cal_id, body=base_event).execute()

            if clean_name == "Brian":
                personal_event = base_event.copy()
                personal_event['summary'] = 'Work'
                personal_event['reminders'] = {
                    'useDefault': False,
                    'overrides': [{'method': 'popup', 'minutes': 1440}, {'method': 'popup', 'minutes': 60}]
                }
                personal_event['colorId'] = 6
                service.events().insert(calendarId="personal.brian.lin@gmail.com", body=personal_event).execute()
    except HttpError as error:
        raise Exception(f"Google API error: {error}")

def upload_schedule(response):
    with open('schedule.xlsx', 'wb') as f:
                f.write(response.content)
    TIME_RANGE_PATTERN = re.compile(r"^\d{1,2}(:\d{2})?(AM|PM)\s*-\s*\d{1,2}(:\d{2})?(AM|PM)$", re.IGNORECASE)
    SKIP_VALUES = {"-", "OFF", "N/A", "AM ONLY"}
    SKIP_KEYWORDS = ["REQ", "NO"]
    for name in names:
        sched = pd.read_excel('schedule.xlsx', engine='openpyxl', skiprows=2)
        sched = sched.iloc[:, 3:].dropna(axis=1, how='all')
        sched = sched.iloc[1:].reset_index(drop=True)
        sched.columns = ['Name'] + sched.columns[1:].tolist()

        row = sched[sched['Name'].str.strip().str.lower() == name.lower()]
        if row.empty:
            print(f"⚠️ No schedule found for {name}")
            continue

        row_values = list(row.values[0])[1:]
        working_times = []
        for day, val in zip(sched.columns[1:], row_values):
            val_str = str(val).strip().upper()
            if (
                not val_str or
                val_str in SKIP_VALUES or
                any(keyword in val_str for keyword in SKIP_KEYWORDS) or
                not TIME_RANGE_PATTERN.match(val_str)
            ):
                continue
            working_times.append((day, val_str))

        event_times = extract_initial_time(working_times)

        try:
            upload_to_google_calendar(event_times, name)
        except Exception as e:
            print(e)