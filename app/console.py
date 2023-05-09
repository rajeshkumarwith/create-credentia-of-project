from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from rest_framework import generics
from rest_framework.decorators import api_view,permission_classes
import requests
from .paginations import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .serializers import *
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.hashers import check_password
from .paginations import *
from django.contrib.auth.models import User

        
from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from django.views.decorators.csrf import csrf_exempt

# Create your views here.



class HelloView(APIView):
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class=UserSerializer
#     queryset=User.objects.all().order_by('date_joined')


# class GroupViewSet(viewsets.ModelViewSet):
#     serializer_class=UserSerializer
#     queryset=User.objects.all()

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
    query='art forms of himachal pradesh'
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
CURR_DIR ='/home/ocode-22/Documents/dockerwithdjango/project/app/'
TOKEN_DIR='/home/ocode-22/Documents/dockerwithdjango/project/TOKEN_FILE'
# CURR_DIR ='/home/ocode-22/Documents/google search api/project/app/credentials.json'
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

# @api_view(['GET'])
# def data(request):
#     pagination_class=CustomPagination()
#     scopes = ['https://www.googleapis.com/auth/webmasters']
#     service = gsc_auth(scopes)
#     sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
#     service = gsc_auth(scopes)
#     list=[]
#     print(service,'sssssssssss')
#     request = {
#         "startDate": "2022-03-01",
#         "endDate": "2022-03-15",
#         "dimensions": [
#         "QUERY"
#     ],
#     "rowLimit": 25000
#     }
#     gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
#     df = pd.DataFrame(gsc_search_analytics['rows'])
#     output_rows=[]
#     for row in gsc_search_analytics['rows']:
#             keyword = row['keys'][0]
#             page = row['keys'][1]
#             country = row['keys'][2]
#             device = row['keys'][3]
#             output_row = [keyword, page, country, device, row['clicks'], row['impressions'], row['ctr'], row['position']]
#             output_rows.append(output_row)
#     df['keys'] = df['keys'].str.get(0)
#     df['ctr']=df['ctr'].round(2)
#     df['impressions']=df['impressions'].round(2)
#     df['position']=df['position'].round(2)
#     df['clicks']=df['clicks'].round(2)
#     list.append(df)
#     column_names = df.columns.tolist()
#     final_row_data=[]
#     for index ,rows in df.iterrows():
#         final_row_data.append(rows.to_dict())
#     # return Response(column_names)
#     return Response(output_rows)

@api_view(['GET'])
def GetCountryAPI(request):
    scopes = ['https://www.googleapis.com/auth/webmasters']
    service = gsc_auth(scopes)
    sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
    service = gsc_auth(scopes)
    list=[]
    print(service,'sssssssssss')
    request = {
        "startDate": "2022-03-01",
        "endDate": "2022-03-15",
        "dimensions": [
        "QUERY","Country"
    ],
    "rowLimit": 25000
    }
    gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
    df = pd.DataFrame(gsc_search_analytics['rows'])
    response = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()

    output_rows=[]
    for row in response['rows']:
            # keyword=row['keys'][0]
            # page = row['keys'][1]
            country = row['keys'][1]
            # device = row['keys']
            output_row = [ country,  row['clicks'], row['impressions'], row['ctr'], row['position']]
            output_rows.append(output_row)
    if "rows" in response:
        df['country'] =response["rows"][1]["keys"][1]
    df = pd.DataFrame(output_rows, columns=['country', 'clicks', 'impressions', 'ctr','position'])
    # df['country']=df['country'].str.get('country')
    # df['country']=df['country'].str.get(0)
    df['country']=df['country'].str.capitalize()
    df['ctr']=df['ctr'].round(2)
    df['position']=df['position'].round(2)
    df['impressions']=df['impressions'].round(2)
    final_row_data=[]
    for index ,rows in df.iterrows():
        final_row_data.append(rows.to_dict())
    # return Response(output_rows)
    return Response(final_row_data)

@api_view(['GET'])
def GetDeviceAPI(request):
    scopes = ['https://www.googleapis.com/auth/webmasters']
    service = gsc_auth(scopes)
    sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
    service = gsc_auth(scopes)
    list=[]
    print(service,'sssssssssss')
    request = {
        "startDate": "2022-03-01",
        "endDate": "2022-03-15",
        "dimensions": [
        "QUERY","Country"
    ],
    "rowLimit": 25000
    }
    gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
    df = pd.DataFrame(gsc_search_analytics['rows'])
    response = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()

    output_rows=[]
    for row in response['rows']:
            # keyword=row['keys'][0]
            # page = row['keys'][1]
            device = row['keys'][1][0]
            # device = row['keys']
            output_row = [ device,  row['clicks'], row['impressions'], row['ctr'], row['position']]
            output_rows.append(output_row)
    df = pd.DataFrame(output_rows, columns=['device', 'clicks', 'impressions', 'ctr','position'])
    df['device'] = df['device'].apply(lambda x: df[x] if x in df['device'] else x)
    df['device']=df['device'].str.capitalize()
    df['ctr']=df['ctr'].round(2)
    df['position']=df['position'].round(2)
    df['impressions']=df['impressions'].round(2)
    final_row_data=[]
    for index ,rows in df.iterrows():
        final_row_data.append(rows.to_dict())
    # return Response(output_rows)
    return Response(final_row_data)


@api_view(['GET'])
def PageAPI(request):
    scopes = ['https://www.googleapis.com/auth/webmasters']
    service = gsc_auth(scopes)
    sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
    service = gsc_auth(scopes)
    list=[]
    print(service,'sssssssssss')
    request = {
        "startDate": "2022-03-01",
        "endDate": "2022-03-15",
        "dimensions": [
        "QUERY","Page"
    ],
    "rowLimit": 25000
    }
    gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
    df = pd.DataFrame(gsc_search_analytics['rows'])
    response = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()

    output_rows=[]
    for row in response['rows']:
            keyword = row['keys'][0]
            page = row['keys'][1]
                # country = row['keys'][2]
                # device = row['keys'][3]
            output_row = [ page,  row['clicks'], row['impressions'], row['ctr'], row['position']]
            output_rows.append(output_row)
    df = pd.DataFrame(output_rows, columns=['page', 'clicks', 'impressions', 'ctr','position'])
    df['ctr']=df['ctr'].round(2)
    df['position']=df['position'].round(2)
    df['impressions']=df['impressions'].round(2)
    final_row_data=[]
    for index ,rows in df.iterrows():
        final_row_data.append(rows.to_dict())
    # return Response(output_rows)
    return Response(final_row_data)

import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np

class DateAPI(APIView):
    def get(self,request,*args,**kwargs):
        try:
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            # start_date = self.kwargs['start_date']
            # end_date=self.kwargs['end_date']
            print(start_date, "fdgfdgdfgfdg")
            print(end_date, "sdfgdend_dategffdg  end_date")
            scopes = ['https://www.googleapis.com/auth/webmasters']
            service = gsc_auth(scopes)
            sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
            service = gsc_auth(scopes)
            list=[]
            print(service,'sssssssssss')
            request = {
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": [
                "QUERY","Page"
            ],
            "rowLimit": 25000
            }
            gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
            df = pd.DataFrame(gsc_search_analytics['rows'])
            response = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()

            output_rows=[]
            for row in response['rows']:
                keys = row['keys'][0]
                # page = row['keys'][1]
                # country = row['keys'][1]
                # device = row['keys'][1][0]
                output_row = [ keys,  row['clicks'], row['impressions'], row['ctr'], row['position']]
                output_rows.append(output_row)
            print(output_rows)
            df['keys'] = df['keys'].str.get(0)
            df['ctr']=df['ctr'].round(2)
            df['impressions']=df['impressions'].round(2)
            df['position']=df['position'].round(2)
            df['clicks']=df['clicks'].round(2)
            list.append(df)
            column_names = df.columns.tolist()
            final_row_data=[]
            for index ,rows in df.iterrows():
                final_row_data.append(rows.to_dict())
            return Response(final_row_data)
        except:
            scopes = ['https://www.googleapis.com/auth/webmasters']
            service = gsc_auth(scopes)
            sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
            service = gsc_auth(scopes)
            list=[]
            print(service,'sssssssssss')
            request = {
            "startDate": "2022-03-01",
            "endDate": "2022-03-15",
            "dimensions": [
            "QUERY","Page"
        ],
        "rowLimit": 25000
        }
        gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
        df = pd.DataFrame(gsc_search_analytics['rows'])
        response = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()

        output_rows=[]
        for row in response['rows']:
                keyword = row['keys'][0]
                page = row['keys'][1]
                # country = row['keys'][2]
                # device = row['keys'][3]
                output_row = [ keyword, page,  row['clicks'], row['impressions'], row['ctr'], row['position']]
                output_rows.append(output_row)
        print(output_rows)
        df['keys'] = df['keys'].str.get(0)
        df['ctr']=df['ctr'].round(2)
        df['impressions']=df['impressions'].round(2)
        df['position']=df['position'].round(2)
        df['clicks']=df['clicks'].round(2)
        list.append(df)
        column_names = df.columns.tolist()
        final_row_data=[]
        for index ,rows in df.iterrows():
            final_row_data.append(rows.to_dict())
        return Response(final_row_data)


class DateFilter(APIView):
    pagination_class = CustomPagination
    def get(self,request,*args,**kwargs):
            start_date = self.request.query_params.get('start_date')
            end_date = self.request.query_params.get('end_date')
            if start_date and end_date:
                pass
            else:
                start_date = "2022-03-01"
                end_date = "2022-03-15"
            country=request.data.get('country')
            device=request.data.get('device')
            page=request.data.get('page')
            scopes = ['https://www.googleapis.com/auth/webmasters']
            service = gsc_auth(scopes)
            sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
            service = gsc_auth(scopes)
            list=[]
            print(service,'sssssssssss')
            request = {
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": ['query', 'country', 'device', 'page'],
            "rowLimit": 25000
            }
            # gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
            # df = pd.DataFrame(gsc_search_analytics['rows'])
            response = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
            df=pd.DataFrame(response['rows'])
            # list=[]
            data=[]
            for row in response['rows']:
                query=row['keys'][0]
                country=row['keys'][1]
                device=row['keys'][2]
                page=row['keys'][3]
                clicks=row['clicks']
                ctr=row['ctr']
                impressions=row['impressions']
                position=row['position']
                data.append({
                    'query':query,
                    'country':country,
                    'device':device,
                    'page':page,
                    'clicks':clicks,
                    'ctr':ctr,
                    'impressions':impressions,
                    'position':position
                })
            # df = pd.DataFrame(data, columns=['page', 'clicks', 'impressions', 'ctr','position'])
            df=pd.DataFrame(data)
            df['ctr']=df['ctr'].round(2)
            df['position']=df['position'].round(2)
            df['impressions']=df['impressions'].round(2)
            final_row_data=[]
            for index ,rows in df.iterrows():
                final_row_data.append(rows.to_dict())
            return Response(final_row_data)
       
# import necessary modules
import datetime
import google.auth
from googleapiclient.discovery import build
from django.shortcuts import render
from django.http import JsonResponse

@api_view(['GET'])
def search_console_data(request):
    # authenticate user and get access token
    credentials, project_id = google.auth.default(
       scopes = ['https://www.googleapis.com/auth/webmasters'])
    webmasters_service = build('webmasters', 'v3', credentials=credentials)

    # extract query parameters from request
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    country = request.GET.get('country')
    device = request.GET.get('device')
    page = request.GET.get('page')

    # convert dates to API-friendly format
    # start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    # end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d')

    # fetch data from Search Console API
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['query', 'country', 'device', 'page'],
        'rowLimit': 10000,
        'dimensionFilterGroups': [
            {
                'filters': [
                    {
                        'dimension': 'country',
                        'operator': 'equals',
                        'expression': country
                    },
                    {
                        'dimension': 'device',
                        'operator': 'equals',
                        'expression': device
                    },
                    {
                        'dimension': 'page',
                        'operator': 'equals',
                        'expression': page
                    }
                ]
            }
        ],
        'fields': ['rows(clicks,ctr,impressions,position)']
    }
    response =service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()

    # extract relevant data from API response
    data = []
    for row in response['rows']:
        query = row['keys'][0]
        country = row['keys'][1]
        device = row['keys'][2]
        page = row['keys'][3]
        clicks = row['clicks']
        ctr = row['ctr']
        impressions = row['impressions']
        position = row['position']
        data.append({
            'query': query,
            'country': country,
            'device': device,
            'page': page,
            'clicks': clicks,
            'ctr': ctr,
            'impressions': impressions,
            'position': position
        })

    # return data in JSON format
    return JsonResponse({'data': data})






@api_view(['GET'])
def PageAPI(request):
    scopes = ['https://www.googleapis.com/auth/webmasters']
    service = gsc_auth(scopes)
    sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
    service = gsc_auth(scopes)
    list=[]
    print(service,'sssssssssss')
    request = {
        "startDate": "2022-03-01",
        "endDate": "2022-03-15",
        "dimensions": [
        "QUERY","Page"
    ],
    "rowLimit": 25000
    }
    gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
    df = pd.DataFrame(gsc_search_analytics['rows'])
    response = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()

    output_rows=[]
    for row in response['rows']:
            keyword = row['keys'][0]
            page = row['keys'][1]
                # country = row['keys'][2]
                # device = row['keys'][3]
            output_row = [ page,  row['clicks'], row['impressions'], row['ctr'], row['position']]
            output_rows.append(output_row)
    df = pd.DataFrame(output_rows, columns=['page', 'clicks', 'impressions', 'ctr','position'])
    df['ctr']=df['ctr'].round(2)
    df['position']=df['position'].round(2)
    df['impressions']=df['impressions'].round(2)
    final_row_data=[]
    for index ,rows in df.iterrows():
        final_row_data.append(rows.to_dict())
    # return Response(output_rows)
    return Response(final_row_data)

@api_view(['GET'])
def CSVReaderToJson(request):
    result_status = 'FAILURE'
    result_data = []
    csv_url = gsc_search_analytics

    try:
        url_content = requests.get(csv_url).content
        csv_data = pd.read_csv(io.StringIO(url_content.decode('utf-8')))

        row_count = csv_data.shape[0]
        column_count = csv_data.shape[1]
        column_names = csv_data.columns.tolist()

        # Option [1]
        # row_json_data = csv_data.to_json(orient='records')

        # Option [2]
        final_row_data = []
        for index, rows in csv_data.iterrows():
            final_row_data.append(rows.to_dict())

        json_result = {'rows': row_count, 'cols': column_count, 'columns': column_names, 'rowData': final_row_data}
        result_data.append(json_result)
        result_status = 'SUCCESS'
    except:
        result_data.append({'message': 'Unable to process the request.'})

    return Response(result_status, result_data)





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

import math
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
    df = pd.DataFrame(gsc_search_analytics['rows'])
    df['keys'] = df['keys'].str.get(0)
    df['ctr']=df['ctr'].round(2)
    df['impressions']=df['impressions'].round(2)
    df['position']=df['position'].round(2)
    df['clicks']=df['clicks'].round(2)
    context = {
    'df_dict': df.to_dict(),
    'df_rec': df.to_dict(orient='records')
    }
    return render(request, 'page.html',context)


import pandas as pd
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
# def GK():
#     return render_template('pandas.html',
#                            PageTitle = "Pandas",
#                            table=[GK_roi.to_html(classes='data', index = False)], titles= GK_roi.columns.values)
from rest_framework.decorators import api_view

# @api_view(['GET'])
def showchartapi(request):
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
    df = pd.DataFrame(gsc_search_analytics['rows'])
    df['keys'] = df['keys'].str.get(0)
    df['ctr']=df['ctr'].round(2)
    df['impressions']=df['impressions'].round(2)
    df['position']=df['position'].round(2)
    df['clicks']=df['clicks'].round(2)
    table=[df.to_html(classes='data', index=False)]
    # return Response([df.to_html(classes='data', index=False)])
    return render(request,'chart.html',{"table":table})


# def mpl():
#     return render_template('matplot.html',
#                            PageTitle = "Matplotlib")

# @app.route('/plot.png')
# def plot_png():
#     fig = create_figure()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

@api_view(['GET'])
def plot_png(request):
    if request.method=='GET':
        fig=create_figure()
        output=id.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')

def mpl(request):
    return render(request,'matplot.html')

import json
def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

import jsonpickle
@api_view(['GET'])
def create_figure(request):
    fig, ax = plt.subplots(figsize = (6,4))
    fig.patch.set_facecolor('#E8E5DA')
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
    df = pd.DataFrame(gsc_search_analytics['rows'])
    x = df.position
    y = df.ctr
    ax.bar(x,y, color = "#304C89")
    print(ax.bar(x,y, color = "#304C89"),'aaaaaaaaaaaxxxxxxxxxxxx')
    plt.xticks(rotation = 30, size = 5)
    print(plt.xticks(rotation = 30, size = 5),'xxxxxxxxxxxxxxxxxxx')
    plt.ylabel("Expected Clean Sheets", size = 5)
    print(plt.ylabel("Expected Clean Sheets", size = 5),'yyyyyyyyyyyyyyyyyyy')
    return Response(jsonpickle.encode(fig))



#Three lines to make our compiler able to draw:
import sys
import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv('data.csv')

# df.plot()

# plt.show()

# #Two  lines to make our compiler able to draw:
# plt.savefig(sys.stdout.buffer)
# sys.stdout.flush()


@api_view(['GET'])
def figure(request):
    df = pd.DataFrame({
        'team': [1,2,3,4],
        'gw1': [1.2,.8,3.1,4.15]
        })
    df.plot(kind = 'scatter', x = 'team', y = 'gw1')
    plt.show()
    # return Response(jsonpickle.encode(data))
    return Response(plt.show())


class DataAPIView(generics.GenericAPIView):
    def get(self,request,*args,**kwargs):
        fig, ax = plt.subplots(figsize = (6,4))
        fig.patch.set_facecolor('#E8E5DA')
        df = pd.DataFrame({
            'team': [1,2,3,4],
            'gw1': [1.2,.8,3.1,4.15]
            })
        x = df.team
        y = df.gw1
        ax.bar(x, y, color = "#304C89")
        print(ax.bar(x,y,color="#304c89"),'aaaaaaaaaaa')
        plt.xticks(rotation = 30, size = 100)
        plt.ylabel("Expected Clean Sheets", size = 5)
        print(fig,'fffffffffffffffff')
        print(type(fig),'tttttttttttt')
        return Response(fig)



import json
import numpy as np
def searchdataapi(request):
  df = pd.DataFrame({
    'col1': [1,2,3,4],
    'col2': [1.27897,.89,3.190778,4.15]
    })
  df = pd.DataFrame(df)
  print(df['col2'],'cccccccc')
#   data=np.ceil(df['col2'])
  df['col2']=df['col2'].round(2)
  print(data,'dddddddddddd')
  context = {
        'df_dict': df.to_dict(),
        'df_rec': df.to_dict(orient='records')
        }
  return render(request,'show.html',context)
from django.utils import timezone

class TopqueriesAPI(viewsets.ModelViewSet):
    serializer_class=ProfileDataSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
            start_date = self.request.query_params.get('start_date')
            end_date = self.request.query_params.get('end_date')
            if start_date and end_date:
                pass
            else:
                start_date = "2022-03-01"
                end_date = "2022-03-15"
            country=self.request.query_params.get('country')
            device=self.request.query_params.get('device')
            page=self.request.query_params.get('page')
            scopes = ['https://www.googleapis.com/auth/webmasters']
            service = gsc_auth(scopes)
            sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
            service = gsc_auth(scopes)
            list=[]
            print(service,'sssssssssss')
            request = {
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": ['query', 'country', 'device', 'page'],
            "rowLimit": 25000
            }
            response = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
            df=pd.DataFrame(response['rows'])
            # list=[]
            data=[]
            for row in response['rows']:
                query=row['keys'][0]
                country=row['keys'][1]
                device=row['keys'][2]
                page=row['keys'][3]
                clicks=row['clicks']
                ctr=row['ctr']
                impressions=row['impressions']
                position=row['position']
                data.append({
                    'query':query,
                    'country':country,
                    'device':device,
                    'page':page,
                    'clicks':clicks,
                    'ctr':ctr,
                    'impressions':impressions,
                    'position':position
                })
            # df = pd.DataFrame(data, columns=['page', 'clicks', 'impressions', 'ctr','position'])
            df=pd.DataFrame(data)
            df['ctr']=df['ctr'].round(2)
            df['position']=df['position'].round(2)
            df['impressions']=df['impressions'].round(2)
            final_row_data=[]
            for index ,rows in df.iterrows():
                final_row_data.append(rows.to_dict())
            return final_row_data
       
from rest_framework import status



# import re
# class  DomainVerify(APIView):
#     def post(self,request,*args,**kwargs):

#         try:
#             scopes = ['https://www.googleapis.com/auth/webmasters']
#             # service = gsc_auth(scopes)
#             credentials = Credentials.from_authorized_user_info({"token": "ya29.a0AWY7CklGQ2Rk5m2qb6Let9O3e8XuEeoigFSfkna_ykl7O7iJEbMPk9ox2rNrPhoQDmtu4_tJcA5QYwDgNDu3SNE37gM-7Cq8KlyB7Few0k7LTesUlPBBko39Ys5T8KHGlz2APHijZvh49O544OVzTZIpjZuBWZzzaCgYKAY4SARASFQG1tDrpS8rerqNq5QrNEWpB52hjmA0167", "refresh_token": "1//0gTCczJ9NH_EPCgYIARAAGBASNwF-L9Irk3KNeZ0IpOk3OpABFzuztmKLv-mSROuQ6Vrl6q5PMaMt56pai7ovJh5Mi9llAdwy0o0", "token_uri": "https://oauth2.googleapis.com/token", "client_id": "857134565960-c8itki1b1mml47692pemc05voj1slebo.apps.googleusercontent.com", "client_secret": "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", "scopes": ["https://www.googleapis.com/auth/webmasters"], "expiry": "2023-05-03T11:25:49.380563Z"})
#             service = build('webmasters', 'v3', credentials=credentials)
#             project=request.data.get('project')
            
#             # project_name=self.request.query_params.get('project_name')
#             # if not project_name:
#             #     project_name='raj'            
#             sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:'+str(project)).execute()
#             service = gsc_auth(scopes)
#             list=[]
#             print(service,'sssssssssss')
#             request = {
#                 "startDate": "2022-03-01",
#                 "endDate": "2022-03-15",
#                 "dimensions": ['query'],
#             "rowLimit": 25000
#                 }
#             response = service.searchanalytics().query(siteUrl='sc-domain:'+str(project), body=request).execute()
            
#             df=pd.DataFrame(response['rows'])
#             print(df,'dddddddddddddd')
#             # df = pd.DataFrame(columns=['keywords', 'clicks', 'impressions', 'ctr','position'])
#             data=[]
#             for row in response['rows']:
#                 query=row['keys'][0]
#                 clicks=row['clicks']
#                 ctr=row['ctr']
#                 impressions=row['impressions']
#                 position=row['position']
#                 data.append({
#                     'query':query,
#                     'clicks':clicks,
#                     'ctr':ctr,
#                     'impressions':impressions,
#                     'position':position
#                 })
#             df=pd.DataFrame(data)
#             df['ctr']=df['ctr'].round(2)
#             df['position']=df['position'].round(2)
#             df['impressions']=df['impressions'].round(2)
#             final_row_data=[]
#             for index ,rows in df.iterrows():
#                 final_row_data.append(rows.to_dict())
#             if df is not None:
#                 return Response(status=status.HTTP_200_OK)
#                     # return Response(final_row_data)
#         except:
#             return Response({"message": "fdgfdg"},status=status.HTTP_400_BAD_REQUEST)   
      
# views.py


       
# class DomainVerify(APIView):
#     def get(self,request,*args,**kwargs):
#         try:
#             url = request.POST.get('url')
            
#             # Initialize the credentials
#             creds = Credentials.from_authorized_user_file('/home/ocode-22/Documents/dockerwithdjango/project/TOKEN_FILE', ['https://www.googleapis.com/auth/webmasters'])

#             # Build the service object
#             service = build('webmasters', 'v3', credentials=creds)

#             # Use the sites().get() method to retrieve the details of the domain
#             site_data = service.sites().get(siteUrl='sc-domain:'+str(url)).execute()
#             if site_data['siteVerificationMethod'] == 'HTML file' or site_data['siteVerificationMethod'] == 'DNS record':
#                 verified = True
#                 verification_method = site_data['siteVerificationMethod']
#             else:
#                 verified = False
#                 verification_method = ''
#         except KeyError:
#                 verified = False
#                 verification_method = ''

#         return JsonResponse({'verified': verified, 'verification_method': verification_method})

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings

#   project=request.data.get('project')
#         # Build the Search Console API client using the credentials
#         search_console = build('webmasters', 'v3', credentials=credentials)

#         try:
#             # Make the API request to verify the domain in Search Console
#             response = search_console.sites().add(siteUrl='https://' + project + '/').execute()
#             return Response(status=status.HTTP_200_OK)
class DomainVerify(APIView):
    def post(self, request):
        project = request.data.get('project')
        # creds = Credentials.from_authorized_user_file(f'{settings.BASE_DIR}/TOKEN_FILE', ['https://www.googleapis.com/auth/webmasters'])
        creds = Credentials.from_service_account_file(f'{settings.BASE_DIR}/credentials.json', scopes=['https://www.googleapis.com/auth/webmasters'])
        search_console = build('webmasters', 'v3', credentials=creds)
        try:
            response = search_console.sites().add(siteUrl='https://' + project + '/').execute()

            return Response(status=status.HTTP_200_OK)

        except HttpError as error:
            # Handle HttpError exceptions
            return Response({'error': error.resp.status}, status=error.resp.status)

        except KeyError:
            # Handle KeyError exceptions
            return Response({'error': 'siteVerificationMethod key not found'}, status=400)




class TopPageAPI(viewsets.ModelViewSet):
    serializer_class=PageDataSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
            start_date = self.request.query_params.get('start_date')
            end_date = self.request.query_params.get('end_date')
            if start_date and end_date:
                pass
            else:
                start_date = "2022-03-01"
                end_date = "2022-03-15"
            country=self.request.query_params.get('country')
            device=self.request.query_params.get('device')
            page=self.request.query_params.get('page')
            scopes = ['https://www.googleapis.com/auth/webmasters']
            service = gsc_auth(scopes)
            sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
            service = gsc_auth(scopes)
            list=[]
            print(service,'sssssssssss')
            request = {
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": ['query', 'country', 'device', 'page'],
            "rowLimit": 25000
            }
            # gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
            # df = pd.DataFrame(gsc_search_analytics['rows'])
            response = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
            df=pd.DataFrame(response['rows'])
            # list=[]
            data=[]
            for row in response['rows']:
                query=row['keys'][0]
                country=row['keys'][1]
                device=row['keys'][2]
                page=row['keys'][3]
                clicks=row['clicks']
                ctr=row['ctr']
                impressions=row['impressions']
                position=row['position']
                data.append({
                    'query':query,
                    'country':country,
                    'device':device,
                    'page':page,
                    'clicks':clicks,
                    'ctr':ctr,
                    'impressions':impressions,
                    'position':position
                })
            # df = pd.DataFrame(data, columns=['page', 'clicks', 'impressions', 'ctr','position'])
            df=pd.DataFrame(data)
            df['ctr']=df['ctr'].round(2)
            df['position']=df['position'].round(2)
            df['impressions']=df['impressions'].round(2)
            datalist=[{'page':row['keys'][1], 'clicks':row['clicks'], 'impressions':row['impressions']} for row in response['rows']]

            # print(response['rows'],'ssssssssssoooooooooorrrrrrrrr')
            final_row_data=[]
            for index ,rows in df.iterrows():
                final_row_data.append(rows.to_dict())
            return final_row_data
            # return datalist
       
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def my_data(request, page_url):
    data = [{'query': row['keys'][0], 'clicks': row['clicks'], 'impressions': row['impressions']} for row in response['rows']]
    # Return the serialized data
    return Response(data)




class QueryAPI(generics.ListCreateAPIView):
    serializer_class=ProfileDataSerializer
    pagination_class = CustomPagination
    def get(self,request,*args,**kwags):
        try:
            country=self.request.query_params.get('country')
            device=self.request.query_params.get('device')
            page=self.request.query_params.get('page')
            project=self.request.query_params.get('project')
            scopes = ['https://www.googleapis.com/auth/webmasters']
            service = gsc_auth(scopes)
            sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:' + str(project)).execute()
            service = gsc_auth(scopes)
            list=[]
            print(service,'sssssssssss')
            request = {
                "startDate": "2022-03-01",
                "endDate":"2022-03-15",
                "dimensions": ['query', 'country', 'device', 'page'],
            "rowLimit": 25000
            }
            # gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
            # df = pd.DataFrame(gsc_search_analytics['rows'])
            response = service.searchanalytics().query(siteUrl='sc-domain:' +str(project), body=request).execute()
            df=pd.DataFrame(response['rows'])
            # list=[]
            data=[]
            for row in response['rows']:
                query=row['keys'][0]
                country=row['keys'][1]
                device=row['keys'][2]
                page=row['keys'][3]
                clicks=row['clicks']
                ctr=row['ctr']
                impressions=row['impressions']
                position=row['position']
                data.append({
                    'query':query,
                    'country':country,
                    'device':device,
                    'page':page,
                    'clicks':clicks,
                    'ctr':ctr,
                    'impressions':impressions,
                    'position':position
                })
            # df = pd.DataFrame(data, columns=['page', 'clicks', 'impressions', 'ctr','position'])
            df=pd.DataFrame(data)
            df['ctr']=df['ctr'].round(2)
            df['position']=df['position'].round(2)
            df['impressions']=df['impressions'].round(2)
            final_row_data=[]
            for index ,rows in df.iterrows():
                final_row_data.append(rows.to_dict())
            return Response(final_row_data)
        except:
            
            return Response(None)
        

# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow

# CLIENT_SECRET_FILE = '/home/ocode-22/Documents/dockerwithdjango/project/credentials.json'
# API_NAME = 'searchconsole'
# API_VERSION = 'v1'

# # Set up the credentials flow
# flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, scopes=['https://www.googleapis.com/auth/webmasters.readonly'])
# creds = flow.run_local_server(port=0)
# creds_dict = {
#     'token': creds.token,
#     'refresh_token': creds.refresh_token,
#     'id_token': creds.id_token,
#     'token_uri': creds.token_uri,
#     'client_id': creds.client_id,
#     'client_secret': creds.client_secret,
#     'scopes': creds.scopes
# }
# creds = Credentials.from_authorized_user_info(creds_dict)

from googleapiclient.discovery import build
from datetime import datetime

from rest_framework import filters
class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])

class SearchDataApi(generics.ListCreateAPIView):
    filter_backends = (DynamicSearchFilter,)
    serializer_class=QueryRelatedSerializer
    def get(self,request,*args,**kwags):
            project=self.request.query_params.get('project')
            query=request.GET.get('q','')
            # if not query:
            #     return Response(status=status.HTTP_400_BAD_REQUEST)
            scopes = ['https://www.googleapis.com/auth/webmasters']
            service = gsc_auth(scopes)
            sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:' + str(project)).execute()
            service = gsc_auth(scopes)
            list=[]
            print(service,'sssssssssss')
            request = {
                'startDate': '2022-01-01',
                'endDate': '2022-04-30',
                'dimensions': ['query'],
                'query': query
             }
            # gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
            # df = pd.DataFrame(gsc_search_analytics['rows'])
            # response = service.searchanalytics().query(siteUrl='sc-domain:' +str(project), body=request).execute()
            # df=pd.DataFrame(response['rows'])
            response = service.searchanalytics().query(siteUrl='sc-domain:' + str(project), body=request).execute()
            # print(df.head(),'hhhhhhhh')
            output_rows=[]
            # for row in response['rows']:
            #     # query=self.request.query_params.get('query')
            #     # query=row['keys'][0]
            #     output_row = [ query,  row['clicks'], row['impressions'], row['ctr'], row['position']]
            #     output_rows.append(output_row)
            # df = pd.DataFrame(output_rows, columns=['query', 'clicks', 'impressions', 'ctr','position'])
            # df['ctr']=df['ctr'].round(2)
            # df['position']=df['position'].round(2)
            # df['impressions']=df['impressions'].round(2)
            # final_row_data=[]
            # for index ,rows in df.iterrows():
            #     final_row_data.append(rows.to_dict())
            for row in response['rows']:
                query=query
                output_row = [ query,  row['clicks'], row['impressions'], row['ctr'], row['position']]
                output_rows.append(output_row)
            df=pd.DataFrame(output_row, columns=['query', 'clicks', 'impressions', 'ctr','position'])
            return Response(df)



class QueryFilter(APIView):
    pagination_class = CustomPagination
    def get(self,request,*args,**kwargs):
            start_date = self.request.query_params.get('start_date')
            end_date = self.request.query_params.get('end_date')
            query=self.request.query_params.get('query')
            if start_date and end_date:
                pass
            else:
                start_date = "2022-03-01"
                end_date = "2022-03-15"
            # country=request.data.get('country')
            # device=request.data.get('device')
            # page=request.data.get('page')
            scopes = ['https://www.googleapis.com/auth/webmasters']
            service = gsc_auth(scopes)
            sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
            service = gsc_auth(scopes)
            list=[]
            print(service,'sssssssssss')
            request = {
                "startDate": start_date,
                "endDate": end_date,
                # 'query':query,
                "dimensions": ['query'],
            "rowLimit": 20
            }
            # gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
            # df = pd.DataFrame(gsc_search_analytics['rows'])
            response = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
            df=pd.DataFrame(response['rows'])
            # list=[]
            data=[]
            for row in response['rows']:
                # query=row['keys'][0]
               
                clicks=row['clicks']
                ctr=row['ctr']
                impressions=row['impressions']
                position=row['position']
                data.append({
                    'query':query,
                    'clicks':clicks,
                    'ctr':ctr,
                    'impressions':impressions,
                    'position':position
                })
            # query=response['rows']['keys']
            print(query,'qqqqqqqqqqqq')
            # df = pd.DataFrame(data, columns=['page', 'clicks', 'impressions', 'ctr','position'])
            df=pd.DataFrame(data)
            df['ctr']=df['ctr'].round(2)
            df['position']=df['position'].round(2)
            df['impressions']=df['impressions'].round(2)
            final_row_data=[]
            for index ,rows in df.iterrows():
                final_row_data.append(rows.to_dict())
            return Response(final_row_data)
    


class SearchAPIView(viewsets.ModelViewSet):
    serializer_class=SearchSerailizer
    queryset=Search.objects.all()
    def get_queryset(self):
        return super().get_queryset()
    

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class SearchConsoleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        scopes = ['https://www.googleapis.com/auth/webmasters']
        service = gsc_auth(scopes)
        project=self.request.query_params.get('project')
        sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:' +str(project)).execute()
        service = gsc_auth(scopes)
        request = {
            'startDate': '2022-01-01',
            'endDate': '2022-02-01',
            'dimensions': ['query'],
            'rowLimit': 10
        }
        response = service.searchanalytics().query(siteUrl='sc-domain: ' + str(project), body=request).execute()
        
        # Save the data to the database            
        for row in response['rows']:
            keyword = row['keys'][0]
            clicks = row['clicks']
            ctr = row['ctr']
            impressions = row['impressions']
            position = row['position']
            search_console_data = SearchResult(
                keyword=keyword,
                clicks=clicks,
                ctr=ctr,
                impressions=impressions,
                position=position
            )
            data=SearchResult(project=project)
            data.save()
            search_console_data.save()
        
        # Return a success response
        return Response({'message': 'Data saved successfully'})



class QueryFilterApi(APIView):
    def get(self,request,*args,**kwargs):
        # keyword=self.request.query_params.get('keyword')
        # data=Search.objects.filter(keyword=keyword).values('keyword','clicks','ctr','impressions','position')
        data=Search.objects.all().values()
        return Response(data)
    
from django.db.models import Q
from rest_framework.generics import ListAPIView

class SearchListdataView(ListAPIView):
    serializer_class = SearchSerailizer
    def get_queryset(self):
        query_params = self.request.query_params.get('keyword', None)
        if query_params is not None:
            values = query_params.split(',')
            print(values,'vvvvvvvvvvvv')
            queries = [Q(keyword=value) for value in values]
            print(queries,'qqqqqqqqqqqq')
            query = queries.pop()
            print(query,'eeeeeeeeeee')
            for q in queries:
                query |= q
            # stuff=SearchConsoleData.objects.all()[:10]
            queryset = SearchConsoleData.objects.filter(query)
           
            print(queryset,'qquuuuuuuuuuuuu')
        else:
            queryset = SearchConsoleData.objects.all()
        return queryset

# class SearchListdataView(ListAPIView):
#     serializer_class=SearchConsoleDataSerializer
#     def get_queryset(self):
#         # project=self.request.query_params.get('project')
#         data=SearchConsoleData.objects.all().values('id','keyword').order_by('-keyword')[:20]
#         return data

class KeywordListAPIView(APIView):
    serializer_class=SearchDataSerializer
    def get(self,request,*args,**kwargs):
        project=self.request.query_params.get('project')
        # data=SearchConsoleData.objects.filter(project=project).values('keyword')[:20]
        search=SearchConsoleData.objects.filter(project=project).values('id','keyword').order_by('keyword')[:20]
        # serializer=SearchDataSerializer(search, many=True)
        return Response(search)


from allauth.socialaccount.models import SocialAccount
from django.shortcuts import redirect

def google_auth_callback(request):
    social_account = SocialAccount.objects.filter(provider='google', user=request.user).first()
    if social_account:
        user = social_account.user
        print(user,'uuuuuuuuu')
        user.email = social_account.extra_data['email']
        print(user.email,'eeeeeeeeeeeeee')
        user.save()

    return 'data'

class Googleauthcallback(generics.GenericAPIView):
    def get(self,request,*args,**kwargs):
        social_account=SocialAccount.objects.filter(provider='google',user=request.user).first()
        print(social_account,'ssssssssssssssss')
        if social_account:
            user=social_account.user
            user.email=social_account.extra_data['email']
            user.save()
        return Response({'save successfully'})




from rest_framework.generics import GenericAPIView
from .serializers import*
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes


@permission_classes((AllowAny, ))
class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        print(data,'ddddddddddddddd')
        return Response(data, status=status.HTTP_200_OK)
    

# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from rest_auth.registration.views import SocialLoginView
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .serializers import UserSerializer


# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     client_class = OAuth2Client

#     def process_login(self):
#         token = self.get_token(self.request.user)
#         user = self.request.user
#         serializer = UserSerializer(user)
#         response = Response(serializer.data)
#         response.set_cookie('jwt', token)
#         print(response,'rrrrrrrrrrr')
#         return response


class UserAPIView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.http import JsonResponse
from .models import SearchResult

def update_search_results(request):
    credentials = service_account.Credentials.from_service_account_file('/home/ocode-22/Documents/dockerwithdjango/project/credentials.json')
    searchconsole = build('searchconsole', 'v1', credentials=credentials)
    user = request.user
    project = user.project_set.first()
    keywords = project.keyword_set.all()
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now()

    for keyword in keywords:
        query = {
            'startDate': start_date.strftime('%Y-%m-%d'),
            'endDate': end_date.strftime('%Y-%m-%d'),
            'dimensions': ['query'],
            'rowLimit': 50,
            'searchType': 'web',
            'startRow': 0,
            'aggregationType': 'auto',
            'dimensionFilterGroups': [{
                'filters': [{
                    'dimension': 'query',
                    'operator': 'equals',
                    'expression': keyword.name
                }]
            }]
        }
        response = searchconsole.searchanalytics


# class update_search_results(APIView):
#     def get(self,request,*args,**kwargs):
#             # credentials = service_account.Credentials.from_service_account_file('/home/ocode-22/Documents/dockerwithdjango/project/credentials.json')
#             # searchconsole = build('searchconsole', 'v1', credentials=credentials)
#             scopes = ['https://www.googleapis.com/auth/webmasters']
#             searchconsole = gsc_auth(scopes)
#             # credentials = service_account.Credentials.from_service_account_file('/path/to/service_account.json')
#             # searchconsole = build('searchconsole', 'v1', credentials=credentials)
#             user = request.user
#             project = Project.objects.filter(user=user).first()
#             keywords = Keyword.objects.filter(project=project)
#             start_date = datetime.now() - timedelta(days=30)
#             end_date = datetime.now()

#             for keyword in keywords:
#                 query = {
#                     'startDate': start_date.strftime('%Y-%m-%d'),
#                     'endDate': end_date.strftime('%Y-%m-%d'),
#                     'dimensions': ['query'],
#                     'rowLimit': 50,
#                     'searchType': 'web',
#                     'startRow': 0,
#                     'aggregationType': 'auto',
#                     'dimensionFilterGroups': [{
#                         'filters': [{
#                             'dimension': 'query',
#                             'operator': 'equals',
#                             'expression': keyword.name
#                         }]
#                     }]
#                 }
#                 response = searchconsole.searchanalytics().query(siteUrl='sc-domain', body=query).execute()
#                 for row in response['rows']:
#                     clicks = row['clicks']
#                     ctr = row['ctr']
#                     impressions = row['impressions']
#                     position = row['position']
#                     SearchResult.objects.create(keyword=keyword, clicks=clicks, ctr=ctr, impressions=impressions, position=position)

#             return Response({"msg":'database create successfully'})
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .models import SearchConsoleData
from .serializers import SearchConsoleDataSerializer
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

class SearchConsoleDataView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        project=request.data['project']
        scopes = ['https://www.googleapis.com/auth/webmasters']
        service = gsc_auth(scopes)
        # Call the Google Search Console API to retrieve data
        try:
            response = service.searchanalytics().query(
                body={
                    'startDate': '2022-01-01',
                    'endDate': '2022-04-01',
                    'dimensions': ['query'],
                    'rowLimit': 100
                },
                siteUrl='sc-domain:' +str(project)).execute()

            # Save data to the database
            for row in response['rows']:
                data = {
                    'project': project,
                    'keyword': row['keys'][0],
                    'clicks': row['clicks'],
                    'ctr': row['ctr'],
                    'impressions': row['impressions'],
                    'position': row['position']
                }
                serializer = SearchConsoleDataSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
        except HttpError as error:
            return Response({'error': error.resp.status}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Data saved successfully'}, status=status.HTTP_200_OK)



# Execute the query and retrieve the response
# response = search_console_service.searchanalytics().query(siteUrl='http://www.example.com', body=query).execute()

# # Process the response and save the data to the database
# rows = response.get('rows', [])
# for row in rows:
#     data = SearchConsoleData(
#         user=user_email,
#         project=site_url,
#         keyword=row['keys'][1],
#         clicks=row['clicks'],
#         ctr=row['ctr'],
#         position=row['position'],
#         impressions=row['impressions']
#     )
#     data.save()





class RemoveSearch(APIView):
    def get(self,request,*args,**kwargs):
        SearchConsoleData.objects.all().delete()
        return Response({'msg':'remove all data'})

# from apiclient import discovery
# import httplib2
# from oauth2client import client

# class SearchData(APIView):
#     def get(self,request,*args,**kwargs):
#         if not request.headers.get('X-Requested-With'):
#             abort(403)

#         CURR_DIR  ='/home/ocode-22/Documents/dockerwithdjango/project'

#         # Exchange auth code for access token, refresh token, and ID token
#         credentials = client.credentials_from_clientsecrets_and_code(
#              str(CURR_DIR)+'/credentials.json',
#             ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
#             auth_code)

#         # Call Google API
#         http_auth = credentials.authorize(httplib2.Http())
#         drive_service = discovery.build('drive', 'v3', http=http_auth)
#         appfolder = drive_service.files().get(fileId='appfolder').execute()

#         # Get profile info from ID token
#         userid = credentials.id_token['sub']
#         email = credentials.id_token['email']
#         return Response(email)
    
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.pk,
            'email': user.email
        })
    

from django.db.models.functions import Round

class ManualSearchAPIVIew(APIView):
    def get(self,request,*args,**kwargs):
        keyword=self.request.query_params.get('keyword')
        data=SearchConsoleData.objects.filter(keyword=keyword).values('id','keyword','clicks','position','ctr','impressions')
        return Response(data)
# class DataSearchAPIView(APIView):
#     def get(self,request,*args,**Kwargs):
#         keyword=self.request.query_params.get('keyword')
#         data=SearchConsoleData.objects.filter(kewyowrd=keyword).values()
#         return Response(data)


from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response

# Set the path to your private key JSON file
KEY_FILE_LOCATION = 'path/to/your/private/key.json'

# Set the scopes for the Search Console API
SCOPES = ['https://www.googleapis.com/auth/webmasters']

class GoogleSearchConsoleView(APIView):
    def get(self, request):
        # Get the credentials object from Django settings
        creds_data =f'{settings.BASE_DIR}/credentials.json'
        creds = Credentials.from_authorized_user_info(info=creds_data, scopes=SCOPES)

        # Refresh the token if it has expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Get the access token
        access_token = creds.token

        # Make your API requests using the access token
        # ...

        return Response({'access_token': access_token})

from django.conf import settings
from django.http import JsonResponse
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def domains(request):
    # Load credentials from the specified key file
    creds = Credentials.from_service_account_file(
        settings.GOOGLE_SERVICE_ACCOUNT_KEYFILE,
        scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )

    # Create a client for the Search Console API
    webmasters_service = build('webmasters', 'v3', credentials=creds)

    # Retrieve the list of verified domains for the specified account
    domains = webmasters_service.sites().list(
        verifiedOwnerUser=settings.GOOGLE_SEARCH_CONSOLE_ACCOUNT_ID
    ).execute().get('siteEntry', [])

    # Save the domains to the database
    for domain in domains:
        Domain.objects.get_or_create(name=domain['siteUrl'])

    # Return the domains as JSON
    return JsonResponse({'domains': list(Domain.objects.values('name'))})

class DomainsAPIView(APIView):
    def post(self,request,*args,**kwargs):
        credentials = Credentials.from_service_account_file(f'{settings.BASE_DIR}/credentials.json', scopes=['https://www.googleapis.com/auth/webmasters'])
        project=request.data.get('project')
        # Build the Search Console API client using the credentials
        search_console = build('webmasters', 'v3', credentials=credentials)

        try:
            # Make the API request to verify the domain in Search Console
            response = search_console.sites().add(siteUrl='https://' + project + '/').execute()
            return Response(status=status.HTTP_200_OK)
        except HttpError as error:
            return Response({'status': 'error', 'message': 'An error occurred while verifying the domain.'})

    


@csrf_exempt
def authenticate(request):
    flow = Flow.from_client_secrets_file(
            f'{settings.BASE_DIR}/client.json',
            scopes=['https://www.googleapis.com/auth/webmasters'],
            redirect_uri='http://localhost:8000/search-console/callback'
        )
    authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
    # request.session['state'] = state
    return redirect(authorization_url)  
    


@csrf_exempt
def google_search_console_login(request):
    # create a Flow object for the Google OAuth2 authorization flow
    flow = InstalledAppFlow.from_client_secrets_file(
      f'{settings.BASE_DIR}/client.json',
        scopes=['https://www.googleapis.com/auth/webmasters.readonly'],
        redirect_uri='https://app.doddlehq.com/google-auth',
        state=request.session.session_key,
       
    )

    # start the authorization flow
    authorization_url, state = flow.authorization_url(prompt='consent')

    # store the state token in the user's session
    request.session['google_state'] = state

    # redirect the user to the Google OAuth2 authorization page
    return redirect(authorization_url)


@csrf_exempt
def google_search_console_login_redirect(request):
    # create a Flow object for the Google OAuth2 authorization flow
    flow = InstalledAppFlow.from_client_secrets_file(
       f'{settings.BASE_DIR}/client.json',
        scopes=['https://www.googleapis.com/auth/webmasters.readonly'],
        redirect_uri='https://app.doddlehq.com/google-auth',
        state=request.session.get('google_state'),
    )
    # exchange the authorization code for an access token and refresh token
    flow.fetch_token(authorization_response=request.get_full_path())

    # store the access token and refresh token in the Django database
    credentials = Credentials.from_authorized_user_info(info=flow.credentials.to_json())
    print(credentials,'cccccccccccccc')
    GoogleSearchConsoleTokenData.objects.update_or_create(
        user=request.user,
        provider='google_search_console',
        defaults={
            'access_token': credentials.access_token,
            'refresh_token': credentials.refresh_token,
        }
    )

    # redirect the user to the homepage
    return redirect('/')
