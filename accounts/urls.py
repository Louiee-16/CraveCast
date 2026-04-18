from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', auth_page, name='auth'),
    path('admin_login/', views.admin_management_view, name='admin-management'),

]
