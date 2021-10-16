

import requests
from dotenv import load_dotenv
import os


def createPost(category='jod'):
    r = requests.get(f'https://api.jokes.one/jod?category={category}')
    response = r.json()
    joke  = response['contents']['jokes'][0]['joke']['text']
    load_dotenv() # load enviroment variables
    token = os.environ.get('FB_TOKEN')
    page_id = os.environ.get('PG_ID')
    requests.post(f"https://graph.facebook.com/{page_id}/feed?&access_token={token}")