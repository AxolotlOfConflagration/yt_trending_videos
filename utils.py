import json
import googleapiclient.discovery

def read_config(config_filename: str):
    with open(config_filename, 'r') as f:
        return json.load(f)


class YTDownloader:
  def __init__(self, apikey):
    self.youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=apikey)

  def get_id(self, title, channel):
    request = self.youtube.search().list(
        part="snippet",
        maxResults=1,
        q=f"{title} {channel}")
    response = request.execute()
    print(f'For {title} and {channel} the response is: {response}')
    return response
