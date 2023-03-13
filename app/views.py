from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from rest_framework import generics
from rest_framework.decorators import api_view
import requests

class HelloView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all().order_by('date_joined')


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()

SEARCH_KEY="AIzaSyCYux7cSQyCqy9jaNi0ZBpvJfjV1sNTZRY"
SEARCH_ID="3077dc85d6a014700"
COUNTRY="in"
SEARCH_URL = "https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={query}&start={start}&num=10&gl=" + COUNTRY
RESULT_COUNT=20
 
# import requests 
# import pandas as pd
import logging
def search_api(request):
    pages=int(RESULT_COUNT/10)
    results = []
    query='python'
    for i in range(0, pages):
        start = i*10+1
        url = SEARCH_URL.format(
            key=SEARCH_KEY,
            cx=SEARCH_ID,
            # query=quote_plus(query),
            query=query,
            start=start
        )
        response = requests.get(url)
        data = response.json()
        results += data["items"]
    res_df = pd.DataFrame.from_dict(results)
    res_df["rank"] = list(range(1, res_df.shape[0] + 1))
    res_df = res_df[["link", "rank", "snippet", "title"]]
    print(res_df, 'resresrresresresresresresresresresr')
    # context={"data":res_df}
    # return render(request,'my_page.html',{'res_df':res_df.to_dict()})
    return res_df

def searchdata(request):
  query='art forms of himachal pradesh'
  df = search_api(query) #returns the dataframe
  print(df,'ddfddffddfdfdfddfdf')
  print(type(df),'typetypetypetypetypetypetypetypetypetype')
  print(type(df['link']),'typelink')
  context = {
    'df_dict': df.to_dict(),
    'df_rec': df.to_dict(orient='records')
    }
  
  return render(request, 'index.html', context)




import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# 'credentials.json'={"installed":{"client_id":"695543285061-mnt3b45di36ua2pugvthvadbqabnijo8.apps.googleusercontent.com","project_id":"hptourtravel1","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}
CURR_DIR ='/home/ocode-22/Documents/dockerwithdjango/project'
TOKEN_DIR='/home/ocode-22/Documents/dockerwithdjango/project/TOKEN_FILE'

def gsc_auth(scopes):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('TOKEN_FILE'):
        creds = Credentials.from_authorized_user_file('TOKEN_FILE', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CURR_DIR)+'/credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('TOKEN_FILE', 'w') as token:
            token.write(creds.to_json())

    service = build('searchconsole', 'v1', credentials=creds)

    return service

scopes = ['https://www.googleapis.com/auth/webmasters']

service = gsc_auth(scopes)

@api_view(['GET'])
def data(request):
    scopes = ['https://www.googleapis.com/auth/webmasters']
    service = gsc_auth(scopes)
    sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
    service = gsc_auth(scopes)
    print(service,'sssssssssss')
    request = {
        "startDate": "2022-03-01",
        "endDate": "2022-03-15",
        "dimensions": [
        "QUERY"
    ],
    "rowLimit": 25000
    }
    gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
    # context={
    #     'df_dict':df.to_dict(),
    #     'df_rec':df.to_dict(orient='records')
    # }
    # return render(request,'data.html',context)
    return Response(gsc_search_analytics)








# from rest_framework import *
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import viewsets

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from oauth2client.client import SignedJwtAssertionCredentials
from httplib2 import Http




def gsc_auth(scopes):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('TOKEN_FILE'):
        creds = Credentials.from_authorized_user_file('TOKEN_FILE', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CURR_DIR)+'/credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('TOKEN_FILE', 'w') as token:
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

import pandas as pd


def searchdataapiview(request):
    scopes = ['https://www.googleapis.com/auth/webmasters']
    service = gsc_auth(scopes)
    requestdata = {
        "startDate": "2022-03-01",
        "endDate": "2022-03-15",
        "dimensions": [
        "QUERY"
    ],
    "rowLimit": 25000
    }
    gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=requestdata).execute()
    gsc_sa_df = pd.DataFrame(gsc_search_analytics['rows'])
    # df=gsc_sa_df.head()
    # for key,value in df.items():
    #     print(key,value)
    # print(df,'sgscgscgscsgsdgscgsc')
    # print(df,'ddfdfdddddfdffffffffffff')
    # print(type(df),'typetypetypetypetypetypetypetyeptype')
    # print(type(df['keys']),'keyskeyskeyskeys')
    # print(type(df['ctr']),'ctrctrctexctecter')
    # print(type(df['impressions']),'impressionimpressionimpressionimpression')
    # print(type(df['position']),'positionpostioitinpostionion')
    # print(type(df['clicks']),'clickeclikcclikcclickclickclick')
    # context={
    #     "df":df['keys']
    # }
    # print(context,'context')
    # return render(request,'my_page.html',context)
    # df = pd.DataFrame(df['keys'])
    context = {
    'df_dict': gsc_sa_df.to_dict(),
    'df_rec': gsc_sa_df.to_dict(orient='records')
    }
    return render(request, 'page.html',context)




# class searchdataapiview(View):    
#     def get(self,request, *args, **kwargs):
#         scopes = ['https://www.googleapis.com/auth/webmasters']
#         service = gsc_auth(scopes)
#         request = {
#             "startDate": "2022-03-01",
#             "endDate": "2022-03-15",
#             "dimensions": [
#             "QUERY"
#         ],
#         "rowLimit": 25000
#         }
#         gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
#         gsc_sa_df = pd.DataFrame(gsc_search_analytics['rows'])
#         data=gsc_sa_df.head(3)
#         return render(request, 'my_page.html', {'df_dict': data.to_dict(), 'df_rec': data.to_dict(orient='records')})

#     def post(request, *args, **kwargs):
#         pass

import json
def searchdataapi(request):
  df = pd.DataFrame({
    'col1': [1,2,3,4],
    'col2': ['A','B', 'C', 'D']
    })
  gsc_sa_df = pd.DataFrame(df['rows'])
  context = {
        'df_dict': gsc_sa_df.to_dict(),
        'df_rec': gsc_sa_df.to_dict(orient='records')
        }
  return render(request,'show.html',context)


class ProfileAPIView(generics.GenericAPIView):
    serializer_class=ProfiledataSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.serializer_class(request.data)
        # data=Profile.objects.filter(id=request.data['id']).values()[0]['username']
        dictV=dict()
        dictV['username']=Profile.objects.filter(id=request.data['id']).values_list('username')
        FriendIDS=Friend.objects.filter(id=request.data['id']).values()
        data=Profile.objects.filter(id__in=FriendIDS).values()
        return Response({'data':dictV ,'msg':200})






