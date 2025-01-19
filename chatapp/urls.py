from django.urls import path

from . import views


urlpatterns = [
    path("", views.rooms, name="rooms"),
    path("<str:slug>", views.room, name="room"),
    path('get_sentiment/', views.get_sentiment_score, name='get_sentiment'),
]