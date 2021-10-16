
from dotenv import load_dotenv
import requests
import os

def sendMessage(cat):
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

