from django.urls import path
from . import views

urlpatterns = [
    path('', views.getContacts, name='contacts'),
    path('create/', views.createContact, name='create-contact'),
    path('latest-video/', views.getLatestVideo, name='latest-video'),
    path('channel-views/', views.getChannelViews, name='channel-views'),
    path('channel-subscriber-count/', views.getSubscriberCount,
         name='channel-subscriber-count'),
    path('channel-video-count/', views.getVideoCount, name='video-count'),
    path('playlist-videos/<str:playlist_id>/<int:max_results>/',
         views.getPlaylistVideos, name='playlist-videos'),
]
