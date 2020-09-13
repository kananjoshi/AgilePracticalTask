from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path(r'login/', auth_views.login, name='login'),
    path(r'logout/', auth_views.logout, name='logout'),

]
