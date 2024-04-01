import feedparser
from news.models import News
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Thread


def get_news():
    print('get news start')
    NewsFeed = feedparser.parse("https://rsshub.bai3401.eu.org/ouc/it/0")
    for i in NewsFeed.entries:

        if News.objects.filter(title=i.title).exists():
            continue
        soup = BeautifulSoup(i.summary, 'html.parser')
        img = soup.find('img')
        if img:
            img = img['src']
        else:
            img = ''
        News.objects.create(title=i.title, published=i.published, content=i.id, image=img)


scheduler = BackgroundScheduler()
# get_news()
t = Thread(target=get_news)
t.start()
scheduler.add_job(get_news, 'interval', minutes=60)
scheduler.start()
print('scheduler start')  # Path: news/apps.py
