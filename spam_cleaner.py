from __future__ import print_function
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Required scope to delete emails
SCOPES = SCOPES = ['https://mail.google.com/']


def authenticate():
    """Authenticate and return valid credentials."""
    # Delete old token if exists to force fresh auth
    if os.path.exists('token.pickle'):
        os.remove('token.pickle')
        print("Old token.pickle removed to ensure correct scopes.")

    creds = None
    if os.path.exists('credentials.json'):
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the new token
        with open('token.pickle', 'wb') as token_file:
            pickle.dump(creds, token_file)
        print("✅ Authentication successful. New 'token.pickle' created!")
    else:
        print("❌ Error: 'credentials.json' not found in the folder.")
        return None
    return creds

def delete_spam(creds, max_results=50):
    """Delete spam emails using given credentials."""
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(userId='me', labelIds=['SPAM'], maxResults=max_results).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No spam emails found!")
        return

    print(f"Found {len(messages)} spam emails. Deleting them now...")

    for msg in messages:
        service.users().messages().delete(userId='me', id=msg['id']).execute()

    print("✅ Spam emails deleted successfully!")

def main():
    creds = authenticate()
    if creds:
        delete_spam(creds)

if __name__ == '__main__':
    main()
