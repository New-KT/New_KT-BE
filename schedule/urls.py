from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetUserEventsView.as_view(), name='get_user_events'),
    path('create/', views.CreateEventView.as_view(), name='create_event'),
    path('eventdelete/', views.EventDelete.as_view(), name='event_delete'),
    path('loginhome/', views.LoginHomeView.as_view(), name='login_home'),
    path('eventclick/<int:event_id>', views.EventClick.as_view(), name='event_click'),
    path('eventdelete/<int:event_id>', views.EventDelete.as_view(), name='event_delete'),
]