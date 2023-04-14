from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from app import views
from .views import *
# from app import ranks
# from .ranks import *
from rest_framework import routers

router=routers.DefaultRouter()
router.register('kewords',views.TopqueriesAPI, basename='profile')
router.register('pages',views.TopPageAPI,basename='page')
# router.register('api',views.QueryAPI,basename='api')

urlpatterns=[
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('data/',views.searchdata,name='search'),
    path('page/',views.PageAPI,name='sitemap'),
    path('show',searchdataapiview,name='show'),
    path('searchdata',views.searchdataapi,name='searchdata'),
    path('chart/',showchartapi,name='graph'),
    path('plot/',views.plot_png,name='plot'),
    path('figure/',create_figure,name='figure'),
    path('figuredata/',figure,name='figure'),
    path('mpl',mpl,name='mpl'),
    path('d/',DataAPIView.as_view(),name='datad'),
    path('country/',GetCountryAPI,name='country'),
    path('device/',GetDeviceAPI,name='device'),
    path('date/',DateAPI.as_view(),name='date'),
    path('filter/',DateFilter.as_view(),name='filter'),
    path('api/',QueryAPI.as_view(),name='api'),
    # path('auth/',GoogleSearchConsoleAPIView.as_view(),name='auth'),
    path('auth/',GoogleSearchConsoleAPIView.as_view(),name='auth')
    

   
    


] + router.urls




