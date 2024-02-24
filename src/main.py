from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from httpx import HTTPStatusError
import httpx

app = FastAPI()
github_client_id = 'bc59d750d6799f0c983e'
github_client_secret = ''

@app.get('/')
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
        'Accept': 'application/vnd.github+json'
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url='https://github.com/login/oauth/access_token', params=params, headers=headers)
        response_json = response.json()
        access_token = response_json['access_token']
        async with httpx.AsyncClient() as client:
            headers.update({'Authorization': f'Bearer {access_token}'})
            response = await client.get('https://api.github.com/user', headers=headers)
        return response.json()
    except HTTPStatusError as http_error:
        status_code = http_error.response.status_code
        if status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized")
        elif status_code == 403:
            raise HTTPException(status_code=403, detail="Forbidden")
        else:
            raise HTTPException(status_code=500, detail="Internal Server Error")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
