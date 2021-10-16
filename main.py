


from fastapi import BackgroundTasks, FastAPI,Depends, HTTPException, status
from jobs.tele import sendNews
from jobs.fb import createPost
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()
security = HTTPBasic()

#microservices
origins = [
    "https://ia88q1.deta.dev",
    "https://blwam9.deta.dev",
    "https://09a2hc.deta.dev",
    "https://45lrqm.deta.dev",
    "https://7pli6t.deta.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username,os.environ.get('USER_NAME'))
    correct_password = secrets.compare_digest(credentials.password,os.environ.get('PASS_WORD'))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return "the task in the background"

@app.get('/')
def index():
    return {'message':'hello world'}

@app.get("/telegram")
async def send_notification(background_tasks: BackgroundTasks,message:str=Depends(auth)):
    background_tasks.add_task(sendNews)
    return {"message": message}

@app.get('/facebook/{category}')
async def create_post(category:str,background_tasks: BackgroundTasks,message:str=Depends(auth)):
    background_tasks.add_task(createPost,category)
    return {"message": message}
