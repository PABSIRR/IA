from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = "users"

urlpatterns = [
    #Login
    path('login/', LoginView.as_view(template_name='Users/login.html'), name='login'),
    #Logout
    path('logout/', LogoutView.as_view(template_name='Users/logout.html'), name='logout'),
    #Register
    path('register/', views.register, name='register'),
]