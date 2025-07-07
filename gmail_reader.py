"""
📬 Gmail Attachment Extractor (TXT only)

This script connects to your Gmail account and downloads all `.txt` attachments
from emails within a specific date range.

🔧 REQUIRED FILES:
- credentials.json → Download from your Google Cloud Console (OAuth 2.0 client credentials)
- token.json       → Will be generated automatically after first login

📦 REQUIRED PYTHON LIBRARIES:
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib

📥 TO INSTALL REQUIRED LIBRARIES:
Run the following command in your terminal:

    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

📝 USER SETUP INSTRUCTIONS:
1. Replace the `CREDENTIALS_FILE`, `TOKEN_FILE`, and `OUTPUT_DIR` values below with paths on your system.
2. Set `START_DATE` and `END_DATE` using the format YYYY/MM/DD.
3. Run the script. A browser window will open the first time to let you log in to your Gmail account.

"""

import os
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# === USER CONFIGURATION ===
# 👇 Replace these paths with your own local file locations

CREDENTIALS_FILE = '/your/path/to/credentials.json'     # OAuth 2.0 credentials (downloaded from Google Cloud)
TOKEN_FILE = '/your/path/to/token.json'                 # Path to store Gmail API token after login (auto-generated)
OUTPUT_DIR = '/your/path/to/drs_reports'              # Directory to save .txt files (will be created if missing)

# 📅 Set your Gmail search window here (YYYY/MM/DD format)
START_DATE = '2025/06/30'                               # Start of the date range (inclusive)
END_DATE = '2025/07/06'                                 # End of the date range (exclusive)

# 📭 Gmail API scope: read-only access to Gmail inbox
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# === CREATE OUTPUT FOLDER IF IT DOESN’T EXIST ===
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === AUTHENTICATE WITH GMAIL API ===
# If token file doesn't exist, perform OAuth login and save token for future use
if not os.path.exists(TOKEN_FILE):
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)  # Opens a browser window for you to log in
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())
else:
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

# === CONNECT TO GMAIL API ===
# Create a service object to interact with Gmail using authenticated credentials
service = build('gmail', 'v1', credentials=creds)

# === DEFINE SEARCH QUERY ===
# Use Gmail's advanced search operators: https://support.google.com/mail/answer/7190
# This query pulls emails sent between START_DATE and END_DATE
query = f'after:{START_DATE} before:{END_DATE}'

# === FETCH LIST OF MATCHING EMAILS ===
# This API call retrieves metadata (IDs) of matching messages
results = service.users().messages().list(userId='me', q=query).execute()
messages = results.get('messages', [])

print(f"📬 Found {len(messages)} matching email(s).")

# === RECURSIVE FUNCTION TO TRAVERSE MIME PARTS AND DOWNLOAD .TXT ATTACHMENTS ===
# Many emails have nested MIME structures (e.g. forwarded messages), so this function
# walks through all nested parts and downloads any attachment ending in `.txt`

def walk_parts(msg_id, parts):
    for part in parts:
        if 'parts' in part:
            # If this part contains sub-parts (e.g. multipart/mixed), walk those too
            walk_parts(msg_id, part['parts'])
        else:
            filename = part.get('filename')
            # Only process attachments with filenames ending in `.txt` (case-insensitive)
            if filename and filename.lower().endswith('.txt'):
                att_id = part.get('body', {}).get('attachmentId')
                if att_id:
                    # Fetch the attachment body using its attachmentId
                    att = service.users().messages().attachments().get(
                        userId='me', messageId=msg_id, id=att_id
                    ).execute()
                    # Decode the base64 attachment content and write it to disk
                    file_data = base64.urlsafe_b64decode(att['data'].encode('UTF-8'))
                    filepath = os.path.join(OUTPUT_DIR, filename)
                    with open(filepath, 'wb') as f:
                        f.write(file_data)
                    print(f"✅ Downloaded: {filepath}")

# === PROCESS EACH EMAIL AND PASS TO walk_parts() ===
# For each message ID found earlier, retrieve its full payload and scan for attachments
for msg in messages:
    msg_detail = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
    payload = msg_detail.get('payload', {})
    parts = payload.get('parts', [])
    walk_parts(msg['id'], parts)
