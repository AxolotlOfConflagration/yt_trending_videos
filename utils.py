import json
import pickle
import pandas as pd
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

    def details_by_id(self, idx):
        request = self.youtube.videos().list(
            part="snippet",
            id=','.join(idx)
        )
        return request.execute()


def video_id_without_categories(df):
    return df[df.category_id.isna()].index


if __name__ == "__main__":
    df = pd.read_pickle('data/chkp1.pkl')
    idx = video_id_without_categories(df)
    config = read_config('config.json')
    yt = YTDownloader(config['apikey'])

    bsize = 10
    results = [yt.details_by_id(idx[x*bsize:(x+1)*bsize]) for x in range((len(idx) // bsize)+1) ]

    with open('data/category_id.pkl', 'wb') as fh:
        pickle.dump(results, fh)
