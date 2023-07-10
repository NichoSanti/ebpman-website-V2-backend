import traceback
import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.timezone import now, timedelta
from decouple import config
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from .models import Contact
from .serializers import ContactSerializer

API_KEY = config("API_KEY")
CHANNEL_ID = config("CHANNEL_ID")


@api_view(['POST'])
def createContact(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        first_name = serializer.validated_data['first_name']
        last_name = serializer._validated_data['last_name']
        email = serializer.validated_data['email_address']
        message = serializer.validated_data['message']

        send_email(first_name, last_name, email, message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_email(first_name, last_name, email, message):
    subject = 'New contact form submission'
    from_email = 'your_email@example.com'
    to_email = settings.DEFAULT_FROM_EMAIL
    body = f"Name: {first_name} {last_name}\nEmail: {email}\nMessage: {message}"

    send_mail(subject, body, from_email, [to_email], fail_silently=False)


@api_view(['GET'])
def getContacts(request):
    contacts = Contact.objects.all().order_by('-created')
    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getLatestVideo(request):

    video_id = cache.get('latestVideo')

    if video_id is None:
        response = requests.get(
            'https://www.googleapis.com/youtube/v3/search',
            params={
                'key': API_KEY,
                'channelId': CHANNEL_ID,
                'part': 'snippet',
                'order': 'date',
                'maxResults': 5,
                'type': 'video',
            },
        )
        response.raise_for_status()
        data = response.json()

        for item in data['items']:
            video_id = item['id']['videoId']

            video_response = requests.get(
                'https://www.googleapis.com/youtube/v3/videos',
                params={
                    'key': API_KEY,
                    'id': video_id,
                    'part': 'snippet',
                },
            )
            video_response.raise_for_status()
            video_data = video_response.json()

            if video_data['items']:
                live_broadcast_content = video_data['items'][0]['snippet']['liveBroadcastContent']
                if live_broadcast_content != 'upcoming':
                    break
        else:
            video_id = None

        cache.set('latestVideo', video_id, 60 * 60)

    return Response({'videoId': video_id})


@api_view(['GET'])
def getChannelViews(request):

    viewCount = cache.get('viewCount')

    if viewCount is None:
        response = requests.get(
            'https://www.googleapis.com/youtube/v3/channels',
            params={
                'key': API_KEY,
                'id': CHANNEL_ID,
                'part': 'statistics',
            },
        )
        response.raise_for_status()
        data = response.json()
        viewCount = data['items'][0]['statistics']['viewCount']

        cache.set('viewCount', viewCount, 60 * 60)

    return Response({'viewCount': viewCount})


@api_view(['GET'])
def getSubscriberCount(request):

    subscriber_count = cache.get('subscriberCount')

    if subscriber_count is None:
        response = requests.get(
            'https://www.googleapis.com/youtube/v3/channels',
            params={
                'key': API_KEY,
                'id': CHANNEL_ID,
                'part': 'statistics',
            },
        )
        response.raise_for_status()
        data = response.json()
        subscriber_count = data['items'][0]['statistics']['subscriberCount']

        cache.set('subscriberCount', subscriber_count, 60 * 60)

    return Response({'subscriberCount': subscriber_count})


@api_view(['GET'])
def getVideoCount(request):

    video_count = cache.get('videoCount')

    if video_count is None:
        response = requests.get(
            'https://www.googleapis.com/youtube/v3/channels',
            params={
                'key': API_KEY,
                'id': CHANNEL_ID,
                'part': 'statistics',
            },
        )
        response.raise_for_status()
        data = response.json()
        video_count = data['items'][0]['statistics']['videoCount']

        cache.set('videoCount', video_count, 60 * 60)

    return Response({'videoCount': video_count})


@api_view(['GET'])
def getPlaylistVideos(request, playlist_id, max_results=5):
    playlist_videos = cache.get(f'playlistVideos-{playlist_id}')

    if playlist_videos is None:
        try:
            response = requests.get(
                'https://www.googleapis.com/youtube/v3/playlistItems',
                params={
                    'key': API_KEY,
                    'playlistId': playlist_id,
                    'part': 'snippet',
                    'maxResults': max_results,
                },
            )

            response.raise_for_status()
            data = response.json()

            print(data)

            # Check if the 'items' list is empty and handle it
            if not data.get('items'):
                print("No items in response")
                return Response({"message": "No items in response"}, status=status.HTTP_400_BAD_REQUEST)

            playlist_videos = [item['snippet']['resourceId']
                               ['videoId'] for item in data['items']]
            cache.set(f'playlistVideos-{playlist_id}',
                      playlist_videos, 60 * 60)

        except Exception as e:

            print(str(e))

            return Response({"message": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'playlistVideos': playlist_videos})
