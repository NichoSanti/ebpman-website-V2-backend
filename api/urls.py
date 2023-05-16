from django.urls import path
from . import views

urlpatterns = [
    path('', views.getContacts, name='contacts'),
    path('create/', views.createContact, name='create-contact'),
    path('latest-video/', views.getLatestVideo, name='latest-video')
]
