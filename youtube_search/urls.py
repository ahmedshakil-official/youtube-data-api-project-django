from django.urls import path
from youtube_search import views

app_name = 'search'

urlpatterns = [
    path('', views.index, name='home')
]
