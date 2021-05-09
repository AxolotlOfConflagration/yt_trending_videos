import json
import pickle
import pandas as pd
import googleapiclient.discovery
from googleapiclient.errors import HttpError

from tinydb import TinyDB, Query
from utils import read_config, YTDownloader
from tqdm import tqdm

def get_unique_ids(docs):
    results = []
    for doc in docs:
        for video in doc['related']['items']:
            results.append(video['id']['videoId'])

    return set(results)


def to_dict(video):
    results = {'video_id': video['id']}
    results = {**results, **video['snippet'], **video['statistics']}
    return results
    
    
if __name__ == "__main__":
    config = read_config('config.json')
    start_transaction = lambda: TinyDB('data/not_trending_db.json')
    # yt = YTDownloader(config['apikey'])
    yt = YTDownloader(config['apikey_alt'])

    with open('data/chkp5/data.json') as fh:
        non_trending_movies = json.load(fh)
        downloaded_ids = set(m['video_id'] for m in non_trending_movies)

    with open('data/chkp5/data_old.json', 'w') as fh:
        json.dump(non_trending_movies, fh)

    with start_transaction() as db:
        Video = Query()

        doc = db.search(Video.related.exists() and Video.related != "")
        trending_ids = set([d['video_id'] for d in db.all()])
        print(len(trending_ids))
        
        non_trending_ids = get_unique_ids(doc)
        print("All ids", len(non_trending_ids))
        non_trending_ids -= trending_ids
        print("All non-trending ids", len(non_trending_ids))
        non_trending_ids -= downloaded_ids
        print("Non-trending ids do download", len(non_trending_ids))
        non_trending_ids = list(non_trending_ids)

    try:
        bsize = 25
        for x in tqdm(range((len(non_trending_ids) // bsize)+1)):
            downloaded = yt.details_by_id(non_trending_ids[x*bsize:(x+1)*bsize])
            non_trending_movies += [to_dict(d) for d in downloaded['items']]

    except HttpError as ex:
        print(ex)
        print("Status code:", ex.resp['status'])
    except Exception as ex:
        print(ex)
    finally:
        print("Movies total:", len(non_trending_movies))
        with open('data/chkp5/data.json', 'w') as fh:
            json.dump(non_trending_movies, fh)


    # idx = video_id_without_categories(df)

    # bsize = 10
    # results = [yt.details_by_id(idx[x*bsize:(x+1)*bsize]) for x in range((len(idx) // bsize)+1) ]

    # with open('data/category_id.pkl', 'wb') as fh:
    #     pickle.dump(results, fh)
