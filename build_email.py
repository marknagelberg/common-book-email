from __future__ import print_function
import httplib2
import os
import random
from jinja2 import Environment, FileSystemLoader
import smtplib
from email.mime.text import MIMEText
import json

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'

COMMONPLACE_BOOK_FOLDER_ID = 'Insert ID of Commonplace Book Folder'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
    Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                    'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_folders_in_directory(service, folder_id):
    folders = service.children().list(folderId = folder_id,
            q = "mimeType = 'application/vnd.google-apps.folder'").execute()
    return folders['items']

def get_google_docs_in_directory(service, folder_id):
    documents = service.children().list(folderId = folder_id,
            q = "mimeType = 'application/vnd.google-apps.document'").execute()
    return documents['items']

def get_list_of_all_google_docs(service, root_folder_id, documents = []):
    unexplored_folders = get_folders_in_directory(service = service,
            folder_id = root_folder_id)
    while unexplored_folders:
        unexplored_folder = unexplored_folders[0]
        del unexplored_folders[0]

        google_docs_in_directory = get_google_docs_in_directory(service,
                unexplored_folder['id'])
        if google_docs_in_directory:
            documents = documents + get_google_docs_in_directory(service,
                unexplored_folder['id'])

        folders_in_directory = get_folders_in_directory(service = service,
                folder_id = unexplored_folder['id'])
        if folders_in_directory:
            unexplored_folders = unexplored_folders + get_folders_in_directory(service = service,
                    folder_id = unexplored_folder['id'])

    return documents

def get_n_random_google_doc_links(google_docs, num_links):
    GOOGLE_DRIVE_LINK = 'https://docs.google.com/document/d/'
    return [GOOGLE_DRIVE_LINK + x['id'] for x in
            random.sample(google_docs, num_links)]

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v2', http=http)

    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('email.html')
    template_context = {}

    google_docs = get_list_of_all_google_docs(service = service,
            root_folder_id = COMMONPLACE_BOOK_FOLDER_ID)

    google_doc_links = get_n_random_google_doc_links(google_docs, 5)
    template_context['google_doc_links'] = google_doc_links

    html  =  template.render(template_context)
    email_info = json.load(open('emails.json'))
    sender = email_info["sender"]
    receivers = email_info["receivers"]

    msg = MIMEText(html, 'html')
    msg['Subject'] = "Common Book Daily Email"
    msg['From'] = sender
    msg['To'] = ",".join(receivers)

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    email_login_info = json.load(open('email_user_pass.json'))

    s.login(user = email_login_info['username'], password = email_login_info['password'])

    s.sendmail(sender, receivers, msg.as_string())

    s.quit()

if __name__ == '__main__':
    main()
