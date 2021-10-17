
import requests
from bs4 import BeautifulSoup
from os import environ
from datetime import datetime
from dateparser.search import search_dates
from pytz import timezone    
from dotenv import load_dotenv


def sendNews():
    r = requests.get('http://www.adaderana.lk/hot-news/',headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"})
    #create instance variable        
    soup = BeautifulSoup(r.content,'lxml')  
    stories =  soup.find_all('div',class_='news-story')
    #sri lanka timezone
    colombo = timezone('Asia/Colombo')
    now = datetime.now(tz=colombo)
    #load enviroment variable
    load_dotenv()
    for story in stories:
        time = story.find('div',class_='comments pull-right').select('span')[0].text
        entity = search_dates(time)[0][1]    
        if entity.strftime('%d:%H') == now.strftime('%d:%H'):
            head  = story.select('h2 a')[0].text
            body = story.find('p').text
            image = story.find('img').get('src')
            time = now.strftime('%b %d %Y %H:%M:%S')
            news = f'''<b>{head}</b>
                    <pre>{body}</pre>
                    <code>{time}</code>
                    '''
            token = environ.get('BOT_TOKEN')
            chat_id = environ.get('CHAT_ID')
            url = f'https://api.telegram.org/{token}/sendPhoto?chat_id=-{chat_id}&photo={image}&caption={news}&parse_mode=html'
            requests.get(url)