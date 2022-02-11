from uuid import uuid4

from fastapi import FastAPI
from models import User, Gender, Role
from typing import Optional, List

app = FastAPI(title='MrPythonAPI')

db: List[User] = [
    User(id=uuid4(), first_name='Jumilia', last_name='Ahmed', gender=Gender.female, roles=[Role.admin])

]


@app.get('/')
async def root():
    return {'hello': 'mundo'}


@app.get('/api/v1/users')
async def fetch_users():
    return db


@app.post('/api/v1/users')
async def add_user(user: User):
    db.append(user)
    return {'id': user.id}

