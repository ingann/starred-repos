from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from httpx import HTTPStatusError
import httpx

app = FastAPI()
#add your own client_id and client_secret credentials to github_client_id and github_client_secret
github_client_id = ''
github_client_secret = ''

#for the github_login and callback functions I utilized this tutorial https://www.youtube.com/watch?v=Pm938UxLEwQ
@app.get('/')
async def github_login():
    return RedirectResponse(f'https://github.com/login/oauth/authorize?client_id={github_client_id}', status_code=302)

@app.get('/callback')
async def callback(code: str):
    if not code:
        raise HTTPException(status_code=400, detail="Invalid code parameter")

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
        response.raise_for_status()
        response_json = response.json()
        access_token = response_json['access_token']
        async with httpx.AsyncClient() as client:
            headers.update({'Authorization': f'Bearer {access_token}'})
            response = await client.get('https://api.github.com/user/starred', headers=headers)
        response.raise_for_status()
        response_json = response.json()
        return get_starred_repos(response_json)
    except HTTPStatusError as http_error:
        handle_status_error(http_error.response.status_code)
    except Exception:
        handle_general_error()


def handle_status_error(status_code: int):
    if status_code == 401:
        raise HTTPException(status_code=401, detail="Unauthorized. Check that you have an existing and valid access token.")
    elif status_code == 403:
        raise HTTPException(status_code=403, detail="Forbidden. Check that you have correct scopes and/or permissions in your access token.")
    else:
        raise HTTPException(status_code=500, detail="Internal Server Error")


def handle_general_error():
    raise HTTPException(status_code=500, detail="Internal Server Error")

def create_repo_object(repo):
    topics = ', '.join(repo.get('topics', []))
    obj = {
        'name': repo['full_name'],
        'description': repo['description'] if repo['description'] else '',
        'URL': repo['html_url'],
        'license': repo['license']['name'] if repo['license'] else '',
        'topics': topics
    }
    return obj

def get_starred_repos(response):
    repos = []
    amount = 0
    for repo in response:
        if not repo['private']:
            repos.append(create_repo_object(repo))
            amount += 1
    result = {'number_of_public_starred_repositories': amount, 'starred_repositories': repos}
    return result