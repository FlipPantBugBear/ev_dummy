from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('stations/', views.station_list, name='station_list'),
    path('stations/<int:station_id>/', views.station_detail, name='station_detail'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/stations/', views.manage_stations, name='manage_stations'),
    path('admin/stations/add/', views.add_station, name='add_station'),
    path('admin/stations/edit/<int:station_id>/', views.edit_station, name='edit_station'),
    path('admin/stations/delete/<int:station_id>/', views.delete_station, name='delete_station'),
    path('admin/users/', views.manage_users, name='manage_users'),
]
