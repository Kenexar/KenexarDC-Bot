import itsdangerous
from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKey, APIKeyHeader, APIKeyCookie
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

import mysql.connector

import config

auto_err = False

API_KEY = '123456861kdsl'
API_KEY_NAME = 'access_token'
COOKIE_DOMAIN = 'localhost.test'

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


def get_api_key(api_key_query: str = Security(api_key_query),
                    api_key_header: str = Security(api_key_header),
                    api_key_cookie: str = Security(api_key_cookie)):

    if api_key_query == API_KEY:
        return api_key_query

    if api_key_header == API_KEY:
        return api_key_header

    if api_key_cookie == API_KEY:
        return api_key_cookie

    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Could not validate your API Key')


@app.get('/')
async def root():
    return 'Welcome to the Security test'


@app.get('/docs')
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    res = get_swagger_ui_html(openapi_url='/openapi.json', title='Docs')
    res.set_cookie(API_KEY_NAME, value=api_key, domain=COOKIE_DOMAIN, httponly=True, max_age=1800, expires=1800)
    return res


@app.get('/logout')
async def route_logout_and_remove_cookie():
    res = RedirectResponse('/')
    res.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return res


@app.get('/secure_endpoint', tags=['Testing some stuff'])
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    res = 'How cool is that john ?'
    return res


@app.get('/api/v1/get_whitelist_{}')
async def get_whitelist_member(bot_name: str, api_key: APIKey = Depends(get_api_key)):
    return 0


@app.get('/api/v1/get_server_channel')
async def get_server_channel():
    cur = config.db.cursor()

    cur.execute()
