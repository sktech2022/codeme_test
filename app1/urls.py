from django.urls import path
from .views import *

urlpatterns = [
    path('',all_login,name='all_login'),
    path('logout/',logoutall,name='logout'),
    path('user_register/',user_register,name='user_register'),
    path('user_home/',user_home,name='user_home'),
    path('admin_home/',admin_home,name='admin_home'),
    path('approve/',admin_approve,name='approve'),
    path('add_task/',add_task,name='add_task'),
    path('test/',test,name='test'),
    path('complete/<str:mark>/<int:count>/',complete,name='complete'),
]