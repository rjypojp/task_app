from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    creds = None
    
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES
        )
        creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    service = build("calendar", "v3", credentials=creds)
    return service

def add_event(title, due_date):
    service = get_calendar_service()
    
    event = {
        "summary": title,
        "start": {
            "date": due_date
        },
        "end": {
            "date": due_date
        }
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