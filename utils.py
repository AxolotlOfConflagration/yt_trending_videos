import json
import pickle
import pandas as pd
import googleapiclient.discovery
from googleapiclient.errors import HttpError

from tinydb import TinyDB, Query


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

    def find_related(self, idx, minDate="2006-07-23T08:24:11+00:00", maxDate="2018-06-14T01:31:53+00:00"):
        request = self.youtube.search().list(
            part="snippet",
            maxResults=50,
            publishedAfter=minDate,
            publishedBefore=maxDate,
            relatedToVideoId=idx,
            type="video"
        )
        return request.execute()


def video_id_without_categories(df):
    return df[df.category_id.isna()].index


if __name__ == "__main__":
    config = read_config('config.json')
    start_transaction = lambda: TinyDB('data/not_trending_db.json')
    # yt = YTDownloader(config['apikey'])
    yt = YTDownloader(config['apikey_alt'])


    for _ in range(105):
        Video = Query()
        with start_transaction() as db:
            doc = db.get(~(Video.related.exists()))
            print("Query for:", doc['video_id'])
            try:
                doc['related'] = yt.find_related(doc['video_id'])
                db.update(doc, Video.video_id == doc['video_id'])
                
            except HttpError as ex:
                print(ex)
                if (ex.resp['status'] == "404"):
                    print(f"Updating {doc['video_id']} with empty string")
                    doc['related'] = ""
                    db.update(doc, Video.video_id == doc['video_id'])
                else:
                    print(ex.resp['status'], "exiting")
                    exit(0)
                
            except Exception as ex:
                print(ex)
                exit(0)

    # df = pd.read_pickle('data/chkp1.pkl')
    # idx = video_id_without_categories(df)

    # bsize = 10
    # results = [yt.details_by_id(idx[x*bsize:(x+1)*bsize]) for x in range((len(idx) // bsize)+1) ]

    # with open('data/category_id.pkl', 'wb') as fh:
    #     pickle.dump(results, fh)
