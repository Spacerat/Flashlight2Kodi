import soundcloud
from xbmcjson import XBMC, PLAYER_VIDEO

XBMC_URL = "http://10.42.69.10:8080/jsonrpc"

# create a client object with access token
# client = 

# find all sounds of buskers licensed under 'creative commons share alike'
# tracks = client.get('/tracks', q='buskers', license='cc-by-sa')

class SoundcloudSearch():
    def __init__(self, client_id):
        self.client = soundcloud.Client(client_id=client_id)

    def get(self, query, num = 1):
        tracks = self.client.get('/tracks', q=query, limit=num)
        videos = []
        for t in tracks:
            title = t.title.encode('utf-8', 'ignore')
            vid = t.id
            thumb = t.artwork_url
            #desc =  search_result['snippet']['description'].encode('utf-8', 'ignore')
            desc = ""

            videos.append((title, vid, thumb, desc))


        return videos




def main():
    s = SoundcloudSearch("aa2f5d9818b648290db2e3d3cd3fc3d0").get("wat", 1)
    idd = s[0][1]
    print s[0]
    xbmc = XBMC(XBMC_URL, "admin", "entertheddwrt")
    xbmc.Player.Open({"item": {"file" : "plugin://plugin.audio.soundcloud/play/?audio_id={}".format(idd)}})

if __name__ == '__main__':
    main()