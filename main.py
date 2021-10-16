

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def http():
    return {'message':'hello world'}