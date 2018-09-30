from newsapi import NewsApiClient
import private
import psycopg2
import time
import web
import webhoseio

run_id = int(time.time())
newsapi = NewsApiClient(api_key = private.API_KEY_NEWSAPI)
conn = psycopg2.connect(private.DB_CONNECTION_STRING)
webhoseio.config(token=private.API_KEY_WEBHOSE)

list_of_urls = web.get_urls(conn)
web.get_newsApi_china(conn, run_id, newsapi, list_of_urls)
web.get_webhose_china(conn, run_id, webhoseio, list_of_urls)
web.get_eastmoney(conn, run_id, list_of_urls)

results_df_html = web.get_results(conn)

subject = "News API Summary"
recipients = private.EMAIL_RECIPIENTS
email_body = u'Results:\n\n\n{}\n\n\nLove,\nEmail Bot'.format(results_df_html)

for recipient in recipients:
    print recipient
    web.send_html_email(email_body, recipient, subject)
