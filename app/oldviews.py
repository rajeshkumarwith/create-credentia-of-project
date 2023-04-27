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
CURR_DIR ='/home/ocode-22/Documents/dockerwithdjango/project'
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

# class  DomainVerify(APIView):
#     def get(self,request,*args,**kwargs):
#         scopes = ['https://www.googleapis.com/auth/webmasters']
#         service = gsc_auth(scopes)
#         project=self.request.query_params.get('project')
#         sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:'+str(project)).execute()
#         service = gsc_auth(scopes)
#         list=[]
#         print(service,'sssssssssss')
#         request = {
#             "startDate": "2022-03-01",
#             "endDate": "2022-03-15",
#             "dimensions": ['query', 'country', 'device', 'page'],
#         "rowLimit": 25000
#             }
#         response = service.searchanalytics().query(siteUrl='sc-domain:'+str(project), body=request).execute()
#         df=pd.DataFrame(response['rows'])
#         if df is not None:
#             # return Response(status=status.HTTP_200_OK)
#             return Response(df)


import re
class  DomainVerify(APIView):
    def get(self,request,*args,**kwargs):
        try:
            scopes = ['https://www.googleapis.com/auth/webmasters']
            service = gsc_auth(scopes)
            project=self.request.query_params.get('project')
            query=self.request.query_params.get('query')
            sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:'+str(project)).execute()
            service = gsc_auth(scopes)
            list=[]
            print(service,'sssssssssss')
            request = {
                "startDate": "2022-03-01",
                "endDate": "2022-03-15",
                "dimensions": ['query'],
            "rowLimit": 25000
                }
            response = service.searchanalytics().query(siteUrl='sc-domain:'+str(project), body=request).execute()
            df=pd.DataFrame(response['rows'])
            # df = pd.DataFrame(columns=['keywords', 'clicks', 'impressions', 'ctr','position'])
            data=[]
            for row in response['rows']:
                query=query
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
            df=pd.DataFrame(data)
            df['ctr']=df['ctr'].round(2)
            df['position']=df['position'].round(2)
            df['impressions']=df['impressions'].round(2)
            final_row_data=[]
            for index ,rows in df.iterrows():
                final_row_data.append(rows.to_dict())
            if df is not None:
                # return Response(status=status.HTTP_200_OK)
                return Response(final_row_data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)   

        
class  VerifyQuery(APIView):
    def get(self,request,*args,**kwargs):
        try:
            scopes = ['https://www.googleapis.com/auth/webmasters']
            service = gsc_auth(scopes)
            project=self.request.query_params.get('project')
            query=self.request.query_params.get('query')
            if not query:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:'+str(project)).execute()
            service = gsc_auth(scopes)
            list=[]
            print(service,'sssssssssss')
            request = {
                "startDate": "2022-03-01",
                "endDate": "2022-03-15",
                "dimensions": ['query', 'country', 'device', 'page'],
            "rowLimit": 25000
                }
            response = service.searchanalytics().query(siteUrl='sc-domain:'+str(project), body=request).execute()
            df=pd.DataFrame(response['rows'])
            data=[]
            for row in response['rows']:
                query=row['keys'][0]
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
            # df = pd.DataFrame(data, columns=['page', 'clicks', 'impressions', 'ctr','position'])
            df=pd.DataFrame(data)
            df['ctr']=df['ctr'].round(2)
            df['position']=df['position'].round(2)
            df['impressions']=df['impressions'].round(2)
            final_row_data=[]
            for index ,rows in df.iterrows():
                final_row_data.append(rows.to_dict())
            if df is not None:
                # return Response(status=status.HTTP_200_OK)
                return Response(final_row_data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)   

# class DomainVerify(viewsets.ModelViewSet):
#     def get_queryset(self):
#         scopes = ['https://www.googleapis.com/auth/webmasters']
#         service = gsc_auth(scopes)
#         project=self.request.query_params.get('project')
#         sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:'+str(project)).execute()
#         service = gsc_auth(scopes)
#         list=[]
#         print(service,'sssssssssss')
#         request = {
#             "startDate": "2022-03-01",
#             "endDate": "2022-03-15",
#             "dimensions": ['query', 'country', 'device', 'page'],
#         "rowLimit": 25000
#             }
#         response = service.searchanalytics().query(siteUrl='sc-domain:'+str(project), body=request).execute()
#         df=pd.DataFrame(response['rows'])
#         if df is not None:
#             return 
       
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
            # country=self.request.query_params.get('country')
            # device=self.request.query_params.get('device')
            # page=self.request.query_params.get('page')
            # scopes = ['https://www.googleapis.com/auth/webmasters']
            # service = gsc_auth(scopes)
            # sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:hptourtravel.com').execute()
            # service = gsc_auth(scopes)
            # list=[]
            # print(service,'sssssssssss')
            # request = {
            #     "startDate": "2022-03-01",
            #     "endDate":"2022-03-15",
            #     "dimensions": ['query', 'country', 'device', 'page'],
            # "rowLimit": 25000
            # }
            # # gsc_search_analytics = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
            # # df = pd.DataFrame(gsc_search_analytics['rows'])
            # response = service.searchanalytics().query(siteUrl='sc-domain:hptourtravel.com', body=request).execute()
            # df=pd.DataFrame(response['rows'])
            # # list=[]
            # data=[]
            # for row in response['rows']:
            #     query=row['keys'][0]
            #     country=row['keys'][1]
            #     device=row['keys'][2]
            #     page=row['keys'][3]
            #     clicks=row['clicks']
            #     ctr=row['ctr']
            #     impressions=row['impressions']
            #     position=row['position']
            #     data.append({
            #         'query':query,
            #         'country':country,
            #         'device':device,
            #         'page':page,
            #         'clicks':clicks,
            #         'ctr':ctr,
            #         'impressions':impressions,
            #         'position':position
            #     })
            # # df = pd.DataFrame(data, columns=['page', 'clicks', 'impressions', 'ctr','position'])
            # df=pd.DataFrame(data)
            # df['ctr']=df['ctr'].round(2)
            # df['position']=df['position'].round(2)
            # df['impressions']=df['impressions'].round(2)
            # final_row_data=[]
            # for index ,rows in df.iterrows():
            #     final_row_data.append(rows.to_dict())
            
            return Response(None)
        
# class QueryAPI(viewsets.ModelViewSet):
#     serializer_class=ProfileDataSerializer
#     pagination_class = CustomPagination
#     def get_queryset(self):
#         try:
#             project=self.request.query_params.get('project')
#             country=self.request.query_params.get('country')
#             device=self.request.query_params.get('device')
#             page=self.request.query_params.get('page')
#             scopes = ['https://www.googleapis.com/auth/webmasters']
#             service = gsc_auth(scopes)
#             sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:' + str(project)).execute()
#             if not sals_sitemaps:
#                 pass
#             service = gsc_auth(scopes)
#             list=[]
#             print(service,'sssssssssss')
#             request = {
#                 "startDate": "2022-03-01",
#                 "endDate": "2022-03-15",
#                 "dimensions": ['query', 'country', 'device', 'page'],
#             "rowLimit": 25000
#             }
#             response = service.searchanalytics().query(siteUrl='sc-domain:' + str(project), body=request).execute()
#             if not response:
#                 pass
#             df=pd.DataFrame(response['rows'])
#             if not df:
#                 pass
#             # list=[]
#             data=[]
#             for row in response['rows']:
#                 query=row['keys'][0]
#                 # country=row['keys'][1]
#                 # device=row['keys'][2]
#                 # page=row['keys'][3]
#                 clicks=row['clicks']
#                 ctr=row['ctr']
#                 impressions=row['impressions']
#                 position=row['position']
#                 data.append({
#                     'query':query,
#                     # 'country':country,
#                     # 'device':device,
#                     # 'page':page,
#                     'clicks':clicks,
#                     'ctr':ctr,
#                     'impressions':impressions,
#                     'position':position
#                 })
#             # df = pd.DataFrame(data, columns=['page', 'clicks', 'impressions', 'ctr','position'])
#             df=pd.DataFrame(data)
#             df['ctr']=df['ctr'].round(2)
#             df['position']=df['position'].round(2)
#             df['impressions']=df['impressions'].round(2)
#             final_row_data=[]
#             for index ,rows in df.iterrows():
#                 final_row_data.append(rows.to_dict())
#             return final_row_data
#         except:
#             data=User.objects.all().values()
#             if not data:
#                 pass
#             return data












    


# # Create your views here.

# class HelloView(APIView):
#     permission_classes = (IsAuthenticated,)
#     def get(self, request):
#         content = {'message': 'Hello, World!'}
#         return Response(content)


from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer



# class RegisterUserAPIView(generics.GenericAPIView):
#     def get(self,request,*args,**kwargs):
#         return Response({'msg':'login succssfully','status':200})


class LoginApi(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        email = data['email']
        password = data['password']

        try:
            user = User.objects.get(email = email)
            validate = check_password(password, user.password)
            if validate:
                token = str(RefreshToken.for_user(user))
                access = str(RefreshToken.for_user(user).access_token)
                return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "access": access,
                "refresh": token,

                })
            else:
                content = {"detail": "Password Do not Match"}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        except:
            content = {"detail": "No active account found with the given credentials"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)




class ResetPasswordAppAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)
    def post(self, request):
        # User_id=self.request.user
        email=request.data['email']
        # User_id=request.data['User_id']
        u=User.objects.get(email=email)
        # password=request.data['password']
        pwd=str(request.data['password'])
        u.set_password(pwd)
        u.save()
        return Response({
            "msg":'Your password is changed successfully.',
            "status":200
        })  



# class AllUsersAPI(generics.GenericAPIView):
#     permission_classes = (AllowAny,)
#     def get(self,reqeust,*args):
#         email = self.request.query_params.get('email')
#         data=User.objects.filter(email=email).values('email')
#         if not data:
#             pass
#             # return Response({'msg':'User Not Found','status':400})
#         return Response(data)
    


# from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class ProjectModelViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['name', 'slug']
    filterset_fields = ['name','slug' ]

   

class CheckListAPI(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    serializer_class=CheckListSerializer
    queryset=CheckList.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['name', 'is_completed']
    filterset_fields = ['is_completed', ]
 
    
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
  
  
class HomeView(APIView):
    permission_classes = (AllowAny, )
  
    def get(self, request):
        content = {'message': 'Welcome to the Social Authentication (Email) page using React Js and Django!'}
        return Response(content)
    

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter





from rest_framework.authtoken.models import Token

from .models import User
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
        if provider == filtered_user_by_email[0].auth_provider:
            new_user = User.objects.get(email=email)

            registered_user = User.objects.get(email=email)
            registered_user.check_password(settings.SOCIAL_SECRET)

            Token.objects.filter(user=registered_user).delete()
            Token.objects.create(user=registered_user)
            new_token = list(Token.objects.filter(
                user_id=registered_user).values("key"))

            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': str(new_token[0]['key'])}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
        user = {
            'username': email, 'email': email,
            'password': settings.SOCIAL_SECRET
        }
        user = User.objects.create_user(**user)
        user.is_active = True
        user.auth_provider = provider
        user.save()
        new_user = User.objects.get(email=email)
        new_user.check_password(settings.SOCIAL_SECRET)
        Token.objects.create(user=new_user)
        new_token = list(Token.objects.filter(user_id=new_user).values("key"))
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': str(new_token[0]['key']),
        }


import json
import requests
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import jwt

@api_view(['POST'])
def google_login(request):
    google_token = request.data.get('token')
    try:
        id_info = id_token.verify_oauth2_token(google_token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)
        email = id_info['email']
        username = email.split('@')[0]
        payload = {
            'username': username,
            'email': email,
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY)
        return Response({'token': jwt_token})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class SearchConsoleAPIView(APIView):
    def get(self,request,*args,**kwargs):
            project=self.request.query_params.get('project')
            query=self.request.query_params.get('query')
            scopes = ['https://www.googleapis.com/auth/webmasters']
            service = gsc_auth(scopes)
            sals_sitemaps = service.sitemaps().list(siteUrl='sc-domain:' + str(project)).execute()
            service = gsc_auth(scopes)
            list=[]
            print(service,'sssssssssss')
            request = {
            'startDate': "2022-03-01",
            'endDate': "2022-04-01",
            'dimensions': ['query'],
            'dimensionFilterGroups': [{
            'filters': [{
                'dimension': 'country',
                'expression': 'ind'
            }]
            }],
            'rowLimit': 10
            }
            response = service.searchanalytics().query(siteUrl='sc-domain:' +str(project), body=request).execute()
            df=pd.DataFrame(response['rows'])
            # list=[]
            data=[]
            for row in response['rows']:
                query=query
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
            return Response(data)
    

from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SearchAnalytics

class SearchAnalyticsView(APIView):
    def get(self, request):
        
        credentials = Credentials.from_authorized_user_info(request.user.auth_token)
        service = build('webmasters', 'v3', credentials=credentials)
        end_date = datetime.now().date() - timedelta(days=1)
        start_date = end_date - timedelta(days=7)
        response = service.searchanalytics().query(
            siteUrl='sc-domain:hptourtravel.com',
            body={
                'startDate': start_date.strftime('%Y-%m-%d'),
                'endDate': end_date.strftime('%Y-%m-%d'),
                'dimensions': ['date'],
                'rowLimit': 1000,
            }
        ).execute()
        for row in response['rows']:
            date = datetime.strptime(row['keys'][0], '%Y-%m-%d').date()
            clicks = row['clicks']
            impressions = row['impressions']
            ctr = row['ctr']
            position = row['position']
            SearchAnalytics.objects.update_or_create(
                date=date,
                defaults={
                    'clicks': clicks,
                    'impressions': impressions,
                    'ctr': ctr,
                    'position': position,
                }
            )
        return Response(status=200)

from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status, generics, filters, views
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.hashers import check_password
from django.template.defaultfilters import slugify
from .paginations import *
# Create your views here.

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)



class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        responce = super(RegisterUserAPIView, self).create(request, *args, **kwargs)
        if responce.status_code == 201:
            user = User.objects.get(pk = responce.data['id'])

            token = str(RefreshToken.for_user(user))
            access = str(RefreshToken.for_user(user).access_token)
            return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "access": access,
            "refresh": token,

            }, status = status.HTTP_201_CREATED)
        return responce



class Login(generics.GenericAPIView):
    def post(self,request,*args,**kwargs):
        return Response({'msg':'login succssfully','status':200})


class LoginApi(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        email = data['email']
        password = data['password']

        try:
            user = User.objects.get(email = email)
            validate = check_password(password, user.password)
            if validate:
                token = str(RefreshToken.for_user(user))
                access = str(RefreshToken.for_user(user).access_token)
                return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "access": access,
                "refresh": token,

                })
            else:
                content = {"detail": "Password Do not Match"}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        except:
            content = {"detail": "No active account found with the given credentials"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)




class ResetPasswordAppAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        User_id=self.request.user
        # User_id=request.data['User_id']
        u=User.objects.get(id=User_id)
        pwd=str(request.data['password'])
        u.set_password(pwd)
        u.save()
        return Response({
            "msg":'Your password is changed successfully.',
            "status":200
        })



class AllUsersAPI(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    def get(self,reqeust,*args):
        email = self.request.query_params.get('email')
        if not email:
            da=User.objects.all().values('email')
            return Response(da)
        data=User.objects.filter(email=email).values('email')
        if not data:
            pass
        return Response(data)


class ProjectModelViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['name', 'slug' ,'user__first_name']
    filterset_fields = ['name','slug', 'user']

class CheckListAPI(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    serializer_class=CheckListSerializer
    queryset=CheckList.objects.all()
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['name', 'is_completed']
    filterset_fields = ['is_completed', ]

class CreateProjectChecklistAPI(views.APIView):

    def post(self, request, *args, **kwargs):

        project_id = request.data.get('project_id', None)
        checklists = request.data.get('checklist', None)

        if project_id and checklists:
            try:
                project = Project.objects.get(pk = project_id)
                for checklist in checklists:
                    CheckList.objects.create(
                        name=checklist,
                        project=project
                    )
                return Response({"message": "Checklist Created"}, status=status.HTTP_200_OK)
            except:
                return Response({"message": "Somthing Went Wrong"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Pass project ID and Checklist"}, status=status.HTTP_204_NO_CONTENT)
    

class CreateProjectAndChecklistAPI(views.APIView):

    def post(self, request, *args, **kwargs):

        name = request.data.get('name', None)
        checklists = request.data.get('checklist', None)
        user_id = request.data.get('user_id', None)

        if name and checklists and user_id:
            try:
                user = User.objects.get(pk = user_id)
                slug = slugify(name)
                project = Project.objects.create(user=user, name=name, slug= slug)
                for checklist in checklists:
                    CheckList.objects.create(
                        name=checklist,
                        project=project
                    )
                return Response({"message": "Checklist Created"}, status=status.HTTP_200_OK)
            except:
                return Response({"message": "Somthing Went Wrong"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Pass project ID and Checklist"}, status=status.HTTP_204_NO_CONTENT)












# from rest_framework import serializers

# from .models import *

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import APIException
from rest_framework import status
from django.utils.encoding import force_str


class CustomValidation(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'
    def __init__(self, detail, field, detail2,field2,status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail),field2: int(force_str(detail2))}
        else: self.detail = {'detail': force_str(self.default_detail)}

class SignupSerializer(serializers.ModelSerializer):
    def validate(self, value):
        if User.objects.filter(email=value['email']):
            raise CustomValidation('Email already exists.','msg',400,'status', status_code=status.HTTP_200_OK)
        return value
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name','password')
        # fields = ('id', 'email', 'password')
        extra_kwargs = {'password':{'write_only':True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'], validated_data['email'],validated_data['first_name'],validated_data['last_name'],validated_data['password'])
        # user = User.objects.create_user(validated_data['email'], validated_data['email'],validated_data['password'])

        return user

from rest_framework import serializers
from .models import User,Project,CheckList



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','phone_no')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','password', 'last_name','first_name','phone_no')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    def create(self, validated_data):
        user = User.objects.create_user(validated_data['email'],
                                        password = validated_data['password'],
                                        first_name = validated_data['first_name'],
                                        phone_no=validated_data['phone_no'],
                                        last_name=validated_data['last_name'],
                                    )

        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)




class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields="__all__"



class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model=CheckList
        fields="__all__"



