from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def list_calendars():
    service = get_service()
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list["items"]:
            print(calendar_list_entry["id"], calendar_list_entry["summary"])
        page_token = calendar_list.get("nextPageToken")
        if not page_token:
            break


def to_datetime(event_time):
    s = event_time.get("dateTime", event_time.get("date"))
    return datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def get_events():
    service = get_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    then = (
        datetime.datetime.utcnow() + datetime.timedelta(days=7)
    ).isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    calendar_id = "family09636652538022017705@group.calendar.google.com"
    # https://developers.google.com/calendar/api/v3/reference/calendars
    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,
            timeMin=now,
            timeMax=then,
            maxResults=100,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    # Prints the start and name of the next 10 events
    today = datetime.datetime.today()
    result = []
    for event in events:

        start = to_datetime(event["start"])
        days_to_event = (start - today).days
        end = to_datetime(event["end"])
        if days_to_event == 0:
            date_part = "Today"
        elif days_to_event == 1:
            date_part = "Tomorrow"
        else:
            date_part = start.strftime("%a %-d %b")
        result.append(
            (
                date_part,
                f"{start.strftime('%H:%M')}-{end.strftime('%H:%M')}",
                event["summary"],
            )
        )
    return result


def get_service():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    dirname = os.path.dirname(__file__)
    token_path = os.path.join(dirname, "token.json")
    creds_path = os.path.join(dirname, "credentials.json")
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    service = build("calendar", "v3", credentials=creds)
    return service


def main():
    events = get_events()
    print(events)


if __name__ == "__main__":
    main()
