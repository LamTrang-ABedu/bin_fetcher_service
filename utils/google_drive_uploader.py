from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

def upload_file_to_drive(filepath, drive_folder):
    credentials = service_account.Credentials.from_service_account_file('credentials.json', scopes=['https://www.googleapis.com/auth/drive'])
    service = build('drive', 'v3', credentials=credentials)

    folder_id = None
    query = f"name='{drive_folder.strip('/')}' and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, spaces='drive').execute()
    items = results.get('files', [])
    if items:
        folder_id = items[0]['id']
    else:
        file_metadata = {
            'name': drive_folder.strip('/'),
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=file_metadata, fields='id').execute()
        folder_id = folder.get('id')

    print(f"[Drive] Folder ID: {folder_id}")
    file_metadata = {'name': os.path.basename(filepath), 'parents': [folder_id]}
    media = MediaFileUpload(filepath, resumable=True)
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"[Drive] Uploaded {filepath} to {drive_folder}")

from googleapiclient.http import MediaFileUpload
