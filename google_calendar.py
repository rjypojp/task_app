from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import json
from dotenv import load_dotenv
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():

    token_json = os.getenv("GOOGLE_TOKEN_JSON")
    
    if not token_json:
        raise ValueError("GOOGLE_TOKEN_JSON is not set")
    
    token_data = json.loads(token_json)

    creds = Credentials.from_authorized_user_info(
        token_data,
        SCOPES
    )

    # トークン更新
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    service = build("calendar", "v3", credentials=creds)
    
    return service


def add_event(title, due_date):
    service = get_calendar_service()

    event = {
        "summary": title,
        "start": {"date": due_date},
        "end": {"date": due_date}
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event
    ).execute()

    return created_event["id"]


def update_event(event_id, title, due_date):
    service = get_calendar_service()

    event = {
        "summary": title,
        "start": {"date": due_date},
        "end": {"date": due_date}
    }

    service.events().update(
        calendarId="primary",
        eventId=event_id,
        body=event
    ).execute()


def delete_event(event_id):
    service = get_calendar_service()

    service.events().delete(
        calendarId="primary",
        eventId=event_id
    ).execute()