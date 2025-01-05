from googleapiclient.discovery import build 
import pandas as pd
from IPython.display import JSON
from dateutil import parser
import seaborn as sns
import matplotlib.pyplot as plt



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

def get_video_details(youtube, video_ids):
    all_video_info = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet, contentDetails, statistics",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()

        stats_to_keep = {
            'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
            'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
            'contentDetails': ['duration', 'definition', 'caption']
        }

        for video in response['items']:
            video_info = {}
            video_info['video_id'] = video['id']

            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None

            all_video_info.append(video_info)

    return pd.DataFrame(all_video_info)

videos_data = get_video_details(youtube,video_ids)

# print(videos_data)


ax = sns.barplot(x= 'title', y= 'viewCount',data= videos_data.sort_values('viewCount',ascending=False)[0:9])
# plot = ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: '{:,.0f} k'.format(x / 1000)))
plt.show()

