from googleapiclient.discovery import build
from utils.config import API_KEY

def get_video_details(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    video_response = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    ).execute()

    if not video_response['items']:
        return None

    video = video_response['items'][0]
    details = {
        'title': video['snippet']['title'],
        'description': video['snippet']['description'],
        'channel': video['snippet']['channelTitle'],
        'published_at': video['snippet']['publishedAt'],
        'view_count': video['statistics'].get('viewCount', 0),
        'like_count': video['statistics'].get('likeCount', 0),
        'comment_count': video['statistics'].get('commentCount', 0)
    }
    return details

def get_comments(video_id, max_results=100):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    comments = []
    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=max_results,
        textFormat='plainText'
    )
    response = request.execute()

    for item in response.get('items', []):
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)
    return comments
