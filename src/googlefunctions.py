import pickle
import os
from googleapiclient import _auth, errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request, AuthorizedSession
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from dotenv import load_dotenv

load_dotenv()
GOOGLE_APP_SCRIPT = os.getenv('GOOGLE_APP_SCRIPT')

SCOPES = [
    'https://www.googleapis.com/auth/forms',
    'https://www.googleapis.com/auth/script.send_mail'
]

creds = None
# Getting credentials from file if available
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If credentials file not available, login from browser
else:
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        SCOPES
    )
    creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('script', 'v1', credentials=creds)

async def create_form(title, email):
    """
    To create google form by running the Google Apps Script
    """
    global creds
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    request = {
        'function': 'createForm',
        'parameters': [title, email]
    }
    loop = asyncio.get_event_loop()
    http = _auth.authorized_http(creds)
    partialfunction = partial(
        service.scripts().run(
            body=request,
            scriptId=f'{GOOGLE_APP_SCRIPT}'
        ).execute,
        http=http
    )
    response = await loop.run_in_executor(ThreadPoolExecutor(), partialfunction)
    return response['response']['result']
