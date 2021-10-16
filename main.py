

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
from dateparser.search import search_dates
from pytz import timezone    
from dotenv import load_dotenv


app = FastAPI()
sched = BackgroundScheduler()


@app.get('/')
def http():
    return {'message':'hello world'}

def job1():
    r = requests.get('http://www.adaderana.lk/hot-news/',headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"})
        
    soup = BeautifulSoup(r.content,'lxml')  

    stories =  soup.find_all('div',class_='news-story')


    colombo = timezone('Asia/Colombo')

    now = datetime.now(tz=colombo)


    for story in stories:
        time = story.find('div',class_='comments pull-right').select('span')[0].text
        entity = search_dates(time)[0][1]    
        if entity.strftime('%d') == now.strftime('%d'):
            head  = story.select('h2 a')[0].text
            body = story.find('p').text
            load_dotenv()
            if now.strftime('%H') == entity.strftime('%H'):
                token = os.environ.get('BOT_TOKEN')
                news = f'''
                    <b>{head}</b>
                    <pre>{body}</pre>
                '''
                requests.get(f'https://api.telegram.org/{token}/sendMessage?chat_id=-647851516&text={news}&parse_mode=HTML')

def job2(cat):
    load_dotenv()
    r = requests.get(f'https://api.jokes.one/jod?category={cat}')
    res = r.json()
    contents = res['contents']
    jokes = contents['jokes'][0]
    text = jokes['joke']['text']
    token = os.environ.get('FB_TOKEN')
    pgid = os.environ.get('PG_ID')
    r = requests.post(f'https://graph.facebook.com/{pgid}/feed',data={'access_token':token,'message':text}) 
    print(r.status_code)


sched.add_job(job1, CronTrigger.from_crontab('59 * * * *'))
sched.add_job(job2,CronTrigger.from_crontab('30 2 * * *'),args=['jod'])
sched.add_job(job2,CronTrigger.from_crontab('30 4 * * *'),args=['animal'])
sched.add_job(job2,CronTrigger.from_crontab('30 6 * * *'),args=['blonde'])
sched.add_job(job2,CronTrigger.from_crontab('30 8 * * *'),args=['knock-knock'])


sched.start()