from django.urls import path
from . import views
urlpatterns = [
    path('events/', views.GetUserEventsView.as_view(), name='get_user_events'),
    path('create/', views.CreateEventView.as_view(), name='create_event'),
]