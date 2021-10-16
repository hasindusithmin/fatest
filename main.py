

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


sched.add_job(job1, CronTrigger.from_crontab('59 * * * *'))
sched.start()