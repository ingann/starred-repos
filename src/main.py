
from fastapi import FastAPI, Response
from fastapi import responses
from fastapi.responses import RedirectResponse
import httpx

app = FastAPI()
github_client_id = 'bc59d750d6799f0c983e'
github_client_secret = 'cfc728e4c0b74460c596bb2b9636efe00d6bb4a8'

@app.get('/github_login')
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code=302)

@app.get('/callback')
async def callback(code: str):
    params = {
        'client_id': github_client_id,
        'client_secret': github_client_secret,
        'code': code
    }

    headers = {
        'Accept': 'application/json'
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url='https://github.com/login/oauth/access_token', params=params, headers=headers)
    response_json = response.json()
    access_token = response_json['access_token']
    async with httpx.AsyncClient() as client:
        headers.update({'Authorization': f'Bearer {access_token}'})
        response = await client.get('https://api.github.com/user', headers=headers)
    return response.json()