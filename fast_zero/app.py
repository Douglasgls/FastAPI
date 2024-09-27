from fastapi import FastAPI

from fast_zero.routers.auth import router as auth
from fast_zero.routers.todos import router as todos
from fast_zero.routers.users import router as users

app = FastAPI()

app.include_router(users)
app.include_router(auth)
app.include_router(todos)


@app.get('/')
def read_root():
    return {'message': 'Olar Mundo!'}
