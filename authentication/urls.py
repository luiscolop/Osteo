from django.urls import path
from authentication.views.auth.views import *
from authentication.views.user.views import *
from authentication.views.dashboard.views import *

app_name= 'authentication'

urlpatterns = [
  path('login/', LoginFormView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'), 
  path('user/', UserListView.as_view(), name='user'),
  path('user/create/',UserCreateView.as_view(), name='user_create'),
  path('user/<int:pk>/edit/',UserUpdateView.as_view(), name='user_edit'),
  path('dashboard/',DashboardTemplateView.as_view(),name='dashboard')
]
