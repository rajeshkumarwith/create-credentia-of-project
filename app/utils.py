import os
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
import os.path
def verify_domain(domain):
    # Load the credentials from the JSON file
    credentials, project = google.auth.default()
    credentials = service_account.Credentials.from_service_account_file(
        f'{settings.BASE_DIR}/client.json',
        scopes=['https://www.googleapis.com/auth/webmasters']
    )

    # Build the Search Console service
    service = build('webmasters', 'v3', credentials=credentials)

    # Send a request to verify the domain
    request = service.sites().add(
        siteUrl=domain,
        verificationMethod='DNS_HTML_FILE'
    ).execute()

    return request
