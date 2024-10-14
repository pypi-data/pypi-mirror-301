from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze_emotion/', views.analyze_emotion, name='analyze_emotion'),
    path('google-calendar/init/', views.google_calendar_init, name='google_calendar_init'),
    path('google-calendar/callback/', views.google_calendar_callback, name='google_calendar_callback'),
    path('get_todays_events_and_tasks/', views.get_todays_events_and_tasks, name='get_todays_events_and_tasks'),
    path('logout/', views.logout, name='logout'),
    path('clear-credentials/', views.clear_credentials, name='clear_credentials'),
    path('get_weather/', views.weather_view, name='get_weather'),
    path('submit_emotion/', views.submit_emotion, name='submit_emotion'),
    path('logout/', views.logout_view, name='logout'),
]