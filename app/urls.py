from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from app import views
# from .views import *
from .console import *
# from app import ranks
# from .ranks import *

from rest_framework import routers

router=routers.DefaultRouter()
router.register('kewords',views.TopqueriesAPI, basename='profile')
router.register('pages',views.TopPageAPI,basename='page')
router.register('save',views.SearchAPIView, basename='save')



# router.register('list',views.SearchListdataView,basename='list')
urlpatterns=[
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path('data/',views.searchdata,name='search'),
    path('page/',views.PageAPI,name='sitemap'),
    # path('show',searchdataapiview,name='show'),
    path('searchdata',views.searchdataapi,name='searchdata'),
    path('chart/',showchartapi,name='graph'),
    # path('plot/',views.plot_png,name='plot'),
    path('figure/',create_figure,name='figure'),
    path('figuredata/',figure,name='figure'),
    path('mpl',mpl,name='mpl'),
    # path('d/',DataAPIView.as_view(),name='datad'),
    path('country/',GetCountryAPI.as_view(),name='country'),
    path('device/',GetDeviceAPI,name='device'),
    path('date/',DateAPI.as_view(),name='date'),
    path('filter/',DateFilter.as_view(),name='filter'),
    path('api/',QueryAPI.as_view(),name='api'),
    path('verify/',DomainVerify.as_view(),name='verify'),
    path('search/',SearchConsoleAPIView.as_view(),name='search'),
    path('queryfilter/',QueryFilterApi.as_view(),name='queryufilter'),
    # path('questionfilter/',QuestionsAPIView.as_view(),name='question'),
    path('list/',SearchListdataView.as_view(),name='list'),
    path('save/',SearchConsoleDataView.as_view(),name='save'),
    path('loginuser/',GoogleSocialAuthView.as_view(),name='google'),
    path('credential/',CustomAuthToken.as_view(),name='credebtial'),
    path('keywordlist/',KeywordListAPIView.as_view(),name='keywordlist'),
    path('manual/',ManualSearchAPIVIew.as_view(),name='manual'),
    path('domain/',DomainsAPIView.as_view(),name='doamain'),
    path('google/',authenticate,name='google'),
    path('query/',QueryFilter.as_view(),name='query'),
    path('google_search_console_login/',google_search_console_login,name='google_search_console_login'),
    path('google_search_console_login_redirect/',google_search_console_login_redirect,name='google_search_console_login_redirect'),
    path('data/',gsc_auth,name='call'),
    path('token/',TokenDataApi.as_view(),name='token')
  
 
   
  

    


   
    


] + router.urls




