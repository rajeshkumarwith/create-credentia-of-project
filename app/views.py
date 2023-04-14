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
                "startDate": "2022-03-01",
                "endDate":"2022-03-15",
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