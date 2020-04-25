#!/usr/bin/python
import os

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
from dotenv import load_dotenv

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
load_dotenv()
DEVELOPER_KEY = os.getenv('YOUTUBE_API_KEY')
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# options = "오직 두 사람"
def search_video(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
            q=options,  # options.q,
            part="snippet",  # "id,snippet",
            maxResults=9  # options.max_results
    ).execute()

    # print(search_response)
        

    videos = []
        # channels = []
        # playlists = []

        # Add each result to the appropriate list, and then display the lists of
        # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            # videos.append("%s (%s)" % (search_result["snippet"]["title"],
            #                         search_result["id"]["videoId"]))
            videos.append({
                'title':search_result["snippet"]["title"],
                'videoId':search_result["id"]["videoId"]
            })

    # print(videos)
    return videos
    # elif
    # elif search_result["id"]["kind"] == "youtube#channel":
    #     channels.append("%s (%s)" % (search_result["snippet"]["title"],
    #                                 search_result["id"]["channelId"]))
    # elif search_result["id"]["kind"] == "youtube#playlist":
    #     playlists.append("%s (%s)" % (search_result["snippet"]["title"],
    #                                 search_result["id"]["playlistId"]))

# print("Videos:\n", "\n".join(videos), "\n")
# print("Channels:\n", "\n".join(channels), "\n")
# print("Playlists:\n", "\n".join(playlists), "\n")


# if __name__ == "__main__":
#     argparser.add_argument("--q", help="Search term", default="Google")
#     argparser.add_argument("--max-results", help="Max results", default=25)
#     args = argparser.parse_args()

#     # try:
    #     youtube_search(args)
    # except HttpError, e:
    #     print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
