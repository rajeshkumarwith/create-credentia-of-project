from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from app import views
from .views import *
# from app import ranks
# from .ranks import *

urlpatterns=[
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', views.HelloView.as_view(), name='hello'),
    path('data/',views.searchdata,name='search'),
    path('search',views.data,name='sitemap'),
    path('show',searchdataapiview,name='show'),
    path('searchdata',views.searchdataapi,name='searchdata'),
    path('profile/',views.ProfileAPIView.as_view(), name='profile'),
    path('graph/',views.showdataapi.as_view(),name='graph'),
    path('chart/',showchartapi,name='graph'),
    path('plot/',views.plot_png,name='plot'),
    path('figure/',create_figure,name='figure'),
    path('figuredata/',figure,name='figure'),
    path('mpl',mpl,name='mpl'),
    path('d/',DataAPIView.as_view(),name='datad'),
    path('pie/',pie_chart,name='pie'),

]




