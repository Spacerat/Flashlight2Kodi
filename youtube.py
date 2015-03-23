
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
  

class YoutubeSearch:
    def __init__(self, key):
        self.key = key

    def get(self, query, num=1):
        youtube = build("youtube", "v3", developerKey=self.key)

        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=num
        ).execute()

        videos = []

        for search_result in search_response.get("items", []):
            
            if search_result["id"]["kind"] == "youtube#video":
                title = search_result["snippet"]["title"].encode('utf-8', 'ignore')
                vid = search_result["id"]["videoId"]
                thumb = search_result['snippet']['thumbnails']['medium']['url']
                desc =  search_result['snippet']['description'].encode('utf-8', 'ignore')

                videos.append((title, vid, thumb, desc))
        return videos


### TESTING ###

def main():
    try:
        print YoutubeSearch("AIzaSyDYJ8TlWYDc1JYjivcByjJ9gHzZGLP1qNI").get("beethoven")
    except HttpError, e:
        print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

if __name__ == '__main__':
    main()
