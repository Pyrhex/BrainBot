import discord
import asyncio
import os
import math
import requests
import datetime
import os.path
import pandas as pd
import numpy as np
import re
import pytz  # You can also use zoneinfo in Python 3.9+

from pytz import timezone
from brainbot import guildList
from discord.ext import commands
from discord.commands import slash_command
from discord import option

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime
import os.path
import pytz
import requests
import pandas as pd
import numpy as np
from discord.ext import commands
from discord.commands import slash_command
from discord import option
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Vancouver time zone
vancouver_tz = pytz.timezone('America/Vancouver')

# Helper function to convert 12-hour format to 24-hour format
def convert_to_24_hour(time_str):
    try:
        # Strip whitespace and separate the time part and period
        time_str = time_str.strip()
        period = time_str[-2:].upper()  # Extract and normalize AM/PM
        time_part = time_str[:-2].strip()  # Extract the time part
        
        if period not in {"AM", "PM"}:
            raise ValueError("Invalid period. Must be 'AM' or 'PM'.")
        
        # Split the time part into hour and minute if ':' is present
        if ':' in time_part:
            hour, minute = map(int, time_part.split(':'))
        else:
            hour = int(time_part)  # Handle cases like "6AM"
            minute = 0  # Default minute is 0
        
        # Validate hour and minute ranges
        if not (0 <= hour <= 12 and 0 <= minute < 60):
            raise ValueError("Invalid time values.")
        
        # Convert to 24-hour format
        if period == "PM" and hour != 12:
            hour += 12
        elif period == "AM" and hour == 12:
            hour = 0
        
        return hour, minute
    
    except Exception as e:
        # Handle any parsing or value errors
        raise ValueError(f"Error processing time string '{time_str}': {e}")

# Helper function to extract initial time from a list of datetime ranges
def extract_initial_time(datetime_list):
    result = []
    for dt, time_range in datetime_list:
        initial_time = time_range.split('-')[0].strip()
        hour, minute = convert_to_24_hour(initial_time)
        new_datetime = dt.replace(hour=hour, minute=minute, second=0, microsecond=0)
        localized_dt = vancouver_tz.localize(new_datetime)
        result.append(localized_dt)
    return result

# Google Calendar upload function
def upload_to_google_calendar(event_times):
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    creds = None
    
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        existing_events = service.events().list(
            calendarId='primary', timeMin=datetime.datetime.utcnow().isoformat() + 'Z', 
            timeMax=(datetime.datetime.utcnow() + datetime.timedelta(days=365)).isoformat() + 'Z', 
            singleEvents=True, orderBy='startTime'
        ).execute()

        existing_event_times = set()
        for event in existing_events.get('items', []):
            event_start = event['start']['dateTime']
            event_start_dt = datetime.datetime.fromisoformat(event_start).astimezone(vancouver_tz)
            existing_event_times.add(event_start_dt)

        # Avoid adding duplicate events
        for event_start_time in event_times:
            if event_start_time not in existing_event_times:
                event = {
                    'summary': 'Work',
                    'location': '9351 Bridgeport Rd, Richmond, BC V6X 1S3',
                    'start': {
                        'dateTime': event_start_time.isoformat(),
                        'timeZone': 'America/Vancouver',
                    },
                    'end': {
                        'dateTime': (event_start_time + datetime.timedelta(hours=8)).isoformat(),
                        'timeZone': 'America/Vancouver',
                    },
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'popup', 'minutes': 24 * 60},
                            {'method': 'popup', 'minutes': 60},
                        ],
                    },
                }
                event = service.events().insert(calendarId='primary', body=event).execute()
                print(f"Event created: {event.get('htmlLink')}")
            else:
                print(f"Event already exists: {event_start_time.isoformat()}")
    except HttpError as error:
        print(f"An error occurred: {error}")

class WorkScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='upload', description="Uploads work schedule onto Google calendar", guild_ids=[928169465475133440])
    @option(
    "attachment",
    discord.Attachment,
    description="A file to attach to the message",
    required=False,  # The default value will be None if the user doesn't provide a file.
)
    async def upload(self, ctx, attachment:discord.Attachment):
        if attachment:
            # Responding with the file URL
            await ctx.respond(f"Received your file: {attachment.url}")
            response = requests.get(attachment.url)
            with open('schedule.xlsx', 'wb') as f:
                f.write(response.content)

            # Step 1: Read the Excel file, skipping the first 2 rows
            sched = pd.read_excel('schedule.xlsx', skiprows=2)

            # Step 2: Drop the first three columns
            sched = sched.iloc[:, 3:]

            # Step 3: Remove empty columns
            sched = sched.dropna(axis=1, how='all')

            # Step 4: Drop the first row
            sched = sched.iloc[1:].reset_index(drop=True)

            # Convert column names from numeric format to dates
            columns = sched.columns[1:].tolist()
            sched.columns = ['Name'] + columns

            # Step 5: Filter rows where 'Name' contains 'BRIAN' (case insensitive)
            sched_filtered = sched[sched['Name'].str.contains('BRIAN', case=False, na=False)]
            tuples = [tuple(zip(sched_filtered.columns, row)) for row in sched_filtered.values]
            times = list(tuples[0][1:-1])

            # Extract working times from the schedule
            working_times = []
            for i in times:
                if i[1] == '-' or "REQ" in i[1]:
                    continue
                else:
                    working_times.append((i[0], i[1]))

            # Extract initial times in the correct time zone
            event_times = extract_initial_time(working_times)

            # Upload the events to Google Calendar
            upload_to_google_calendar(event_times)
        else:
            await ctx.respond("You didn't give me a file to upload! :sob:")


def setup(bot):
    bot.add_cog(WorkScheduler(bot))