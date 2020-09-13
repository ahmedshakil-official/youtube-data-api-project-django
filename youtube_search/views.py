from django.shortcuts import render
from django.conf import settings
import requests
from isodate import parse_duration
# Create your views here.


def index(request):
    videos = []
    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'type': 'video'
        }
        req = requests.get(search_url, params=search_params)
        video_ids = []
        results = req.json()['items']
        for result in results:
            video_ids.append(result['id']['videoId'])

        video_params = {
            'part': 'snippet,contentDetails',
            'key': settings.YOUTUBE_DATA_API_KEY,
            'id': ','.join(video_ids),
        }
        req = requests.get(video_url, params=video_params)
        results = req.json()['items']

        print(results)
        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'video_url': f'https://www.youtube.com/watch?v={result["id"]}',
                'duration': parse_duration(result['contentDetails']['duration']),
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
                'description': result['snippet']['description']
            }

            videos.append(video_data)
    context = {'videos': videos}
    return render(request, 'search/index.html', context=context)
