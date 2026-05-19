from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import json
import tempfile

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_calendar_service():
    # Render の Environment Variables から credentials.json の中身を取得
    credentials_json = os.getenv("GOOGLE_CREDENTIALS")

    # 環境変数が設定されていない場合はエラー
    if not credentials_json:
        raise ValueError("GOOGLE_CREDENTIALS is not set.")

    # 一時ファイルとして credentials.json を作成
    with tempfile.NamedTemporaryFile(
        mode="w",
        delete=False,
        suffix=".json",
        encoding="utf-8"
    ) as f:
        f.write(credentials_json)
        temp_path = f.name

    creds = None

    # token.json が存在する場合はそれを使用
    token_json = os.getenv("GOOGLE_TOKEN")
    
    if token_json:
        creds = Credentials.from_authorized_user_info(
            json.loads(token_json),
            SCOPES
        )

    # 認証情報がない、または無効な場合は再認証
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            temp_path,
            SCOPES
        )
        creds = flow.run_local_server(port=0)

        # token.json を保存
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    # Google Calendar API サービスを作成
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