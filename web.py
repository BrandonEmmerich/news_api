import datetime
import private
import requests
import time
import uuid

def get_urls(conn):
    '''Query database to get a list of existing news URLs'''
    cur = conn.cursor()
    cur.execute(private.QUERY_GET_URLS)
    list_of_urls = [tuple_[0] for tuple_ in cur.fetchall()]

    return list_of_urls

def get_newsApi_china(conn, run_id, newsapi, list_of_urls):
    '''Get China business news and write to DB'''
    cur = conn.cursor()
    headlines = newsapi.get_top_headlines(category = 'business', country = 'cn')
    data = headlines['articles']

    for d in data:

        row = {
                'run_id': run_id,
                'uuid' : str(uuid.uuid4()),
                'service': 'news_api',
                'publish_date' : datetime.datetime.strptime(d['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'),
                'source': d['source']['name'],
                'url' : d['url'],
                'title' : d['title'],
                'description' : d['description'],
            }

        if row['url'] not in list_of_urls:
            cur.execute(private.QUERY_INSERT, row)
            conn.commit()
        else:
            print 'We good on this: ' + row['url']

def get_webhose_china(conn, run_id, webhoseio, list_of_urls):
    '''Get China business news from WebHose and write to DB'''
    cur = conn.cursor()
    query_params = {
        "q": "thread.country:CN site_category:business site_type:news",
        "sort": "crawled"
    }

    output = webhoseio.query("filterWebContent", query_params)
    data = output['posts']

    for d in data:

        row = {
                'run_id': run_id,
                'uuid' : str(uuid.uuid4()),
                'service': 'webhose',
                'publish_date' : datetime.datetime.strptime(d['published'][0:19], '%Y-%m-%dT%H:%M:%S'),
                'source': d['thread']['site'],
                'url' : d['url'],
                'title' : d['title'],
                'description' : d['text'][:100],
            }

        if row['url'] not in list_of_urls:
            cur.execute(private.QUERY_INSERT, row)
            conn.commit()
        else:
            print 'We good on this: ' + row['url']

def get_eastmoney(conn, run_id, list_of_urls):
    '''Get news stories from the eastmoney API'''
    cur = conn.cursor()
    url = 'http://newsapi.eastmoney.com/kuaixun/v2/api/yw?limit=100'
    res = requests.get(url)
    data = res.json()['news']

    for d in data:
        row = {
            'run_id': run_id,
            'uuid' : str(uuid.uuid4()),
            'service': 'eastmoney',
            'publish_date' : datetime.datetime.strptime(d['showtime'], '%Y-%m-%d %H:%M:%S'),
            'source': d['Art_Media_Name'],
            'url' : d['url_w'],
            'title' : d['title'],
            'description' : d['digest'],
        }

        if row['url'] not in list_of_urls:
            cur.execute(private.QUERY_INSERT, row)
            conn.commit()
        else:
            print 'We good on this: ' + row['url']
