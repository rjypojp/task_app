from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os
import json
from dotenv import load_dotenv
load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    credentials_json = os.getenv("GOOGLE_CREDENTIALS")
    token_path = os.getenv("GOOGLE_TOKEN")

    if not credentials_json:
        raise ValueError("GOOGLE_CREDENTIALS is not set.")

    if not token_path:
        raise ValueError("GOOGLE_TOKEN is not set")

    with open(token_path, "r") as f:
        creds_data = json.load(f)

    creds = Credentials.from_authorized_user_info(
        creds_data,
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