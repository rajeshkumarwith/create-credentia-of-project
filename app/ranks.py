
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials



# Define function to get authorization
def gsc_auth(scopes):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('searchconsole', 'v1', credentials=creds)

    return service

scopes = ['https://www.googleapis.com/auth/webmasters']

service = gsc_auth(scopes)

# def searchdata(request):
#   query='art forms of himachal pradesh'
#   df = search_api(query) #returns the dataframe
#   context = {
#     'df_dict': df.to_dict(),
#     'df_rec': df.to_dict(orient='records')
#     }
#   print('df_dict','dfffffffffdfdfddddddd')
#   return render(request, 'index.html', context)



# def data(request):
#     df=gsc_auth()
#     context={
#         'df_dict':df.to_dict(),
#         'df_rec':df.to_dict(orient='records')
#     }
#     return render(request,'data.html',context)



def searchdataapi(request):
    scopes = ['https://www.googleapis.com/auth/webmasters']
    sevice=gsc_auth(scopes)
    sals_sitemaps=service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
    print(sals_sitemaps,'salssalssalssalssalssals')
    service=gsc_auth(scopes)
    request={
        "startDate":"2022-03-01",
        "endDate":"2022-10-15",
        "dimenssions":[
            "QUERY"
        ],
        "rowLimit":25000
    }
    gsc_search_analytics=serivce.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com').execute()
    print(gsc_search,'gsc_searchHHHHHHHHHHHHHHHHh')
    df=pd.DataFrame(gsc_search_analytics['rows'])
    # data=gsc_sa_df.head(3)
    context={
        'df_dict':df.to_dict(),
        'df_rec':df.to_dict(orient='records')
    }
    return render(request,'data.html',context)












