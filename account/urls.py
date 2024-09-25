from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView
from account import views


app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register'),
  
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_user, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard')
 
   
]
