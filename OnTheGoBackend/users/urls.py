from django.urls import path
from .views import CustomUserCreate, BlacklistTokenView,UserDetails

app_name='users'

urlpatterns = [
    path('register/',CustomUserCreate.as_view(),name='create_user'),
    path('logout/blacklist/',BlacklistTokenView.as_view(),name='blacklist'),
    path('<int:pk>/', UserDetails.as_view(),name="userdetailscreate"),
    
]