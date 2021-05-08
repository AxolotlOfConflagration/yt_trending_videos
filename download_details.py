import json
import pickle
import pandas as pd
import googleapiclient.discovery
from googleapiclient.errors import HttpError

from tinydb import TinyDB, Query
from utils import read_config, YTDownloader


def get_unique_ids(docs):
    results = []
    for doc in docs:
        for video in doc['related']['items']:
            results.append(video['id']['videoId'])

    return set(results)


if __name__ == "__main__":
    config = read_config('config.json')
    start_transaction = lambda: TinyDB('data/not_trending_db.json')
    # yt = YTDownloader(config['apikey'])
    yt = YTDownloader(config['apikey_alt'])

    with start_transaction() as db:
        Video = Query()

        doc = db.search(Video.related.exists() and Video.related != "")
        trending_ids = set([d['video_id'] for d in db.all()])
        print(len(trending_ids))
        
        non_trending_ids = get_unique_ids(doc)
        print(len(non_trending_ids))
        print(len(non_trending_ids - trending_ids))
        values = list(non_trending_ids - trending_ids)[:10]
        print(values)


        # print("Query for:", doc['video_id'])
        # try:
        #     doc['related'] = yt.find_related(doc['video_id'])
        #     db.update(doc, Video.video_id == doc['video_id'])
            
        # except HttpError as ex:
        #     print(ex)
        #     if (ex.resp['status'] == "404"):
        #         print(f"Updating {doc['video_id']} with empty string")
        #         doc['related'] = ""
        #         db.update(doc, Video.video_id == doc['video_id'])
        #     else:
        #         print(ex.resp['status'], "exiting")
        #         exit(0)
            
        # except Exception as ex:
        #     print(ex)
        #     exit(0)


    # idx = video_id_without_categories(df)

    # bsize = 10
    # results = [yt.details_by_id(idx[x*bsize:(x+1)*bsize]) for x in range((len(idx) // bsize)+1) ]

    # with open('data/category_id.pkl', 'wb') as fh:
    #     pickle.dump(results, fh)
