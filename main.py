from fastapi import FastAPI
import uvicorn
from routers import users

app = FastAPI()

app.include_router(users.router)


@app.get('/')
def ping():
    return 'Hello, Sever running..'


if __name__ == '__main__':
    uvicorn.run(app)