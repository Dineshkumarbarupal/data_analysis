from googleapiclient.discovery import build 
import pandas as pd
from IPython.display import JSON
# import json

api_keys = "AIzaSyC7IItxesghU2QTADvmEZusDD8KebGeFso"
channel_ids = ['UCeVMnSShP_Iviwkknt83cww']

api_service_name = "youtube"
api_version = "v3"


# Get credentials and create an API client
youtube = build(
    api_service_name, api_version, developerKey=api_keys)

# request = youtube.channels().list(
#     part="snippet,contentDetails,statistics",
#     id=",".join(channel_ids)
# )
# response = request.execute()
# print(response)

def get_channel_stats(youtube, channel_ids):
    all_data = []

    # Create request to get channel details
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=",".join(channel_ids)
    )
    response = request.execute()

    # Loop through the items in the response
    for item in response['items']:
        data = {
            'channelName': item['snippet']['title'],
            'subscribers': item['statistics']['subscriberCount'],
            'views': item['statistics']['viewCount'],
            'totalVideos': item['statistics']['videoCount'],
            'playlistId': item['contentDetails']['relatedPlaylists']['uploads']
        }
        all_data.append(data)

    # Return data as a Pandas DataFrame
    return pd.DataFrame(all_data)
# print(response)

channel_data = get_channel_stats(youtube,channel_ids)
print(channel_data)


playlist_id = "UUeVMnSShP_Iviwkknt83cww"  # Example playlist ID
def get_video_ids(youtube, playlist_id):
    video_ids = []

    # Create request to get playlist items
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()

    # Loop through the items in the response
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])

    next_page_token =  response.get('nextpagetoken')
    while next_page_token is not None:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50
        )
        response = request.execute()

        for item in response['items']:
            video_ids.append(item['contentDetails']['videoId'])

        next_page_token = response.get('nextpagetoken')

    return video_ids

video_ids = get_video_ids(youtube,playlist_id)
print(video_ids)
print(len(video_ids))

