# CSC-app

This is a python FastAPI app that utilizes GitHub OAuth2 authentication and lets users to retrieve their public starred repositories using GitHub API.

## Configuration

Before running the application, you need to have OAuth2 credentials from GitHub:

1. Create a new OAuth App on GitHub through settings -> developer settings
2. Set the Homepage URL to `http://127.0.0.1:8000/` and Authorization callback URL to `http://127.0.0.1:8000/callback`
3. Copy the "Client ID" and "Client Secret" and update them in the `main.py` file as follows:

    ```python
    github_client_id = '' #your client id
    github_client_secret = '' #your client secret
    ```

## Running the application

1. Install the required dependencies:

   ```bash
   pip install fastapi
   ```
   
   ```bash
   pip install httpx
   ```
   
2. For running the FastAPI server you need to install the uvicorn:
   
   ```bash
   pip install "uvicorn[standard]"
   ```

3. Then you can start running the server:

   ```bash
   uvicorn main:app --reload
   ```

The App will be accessible at `http://127.0.0.1:8000/`

## Testing

For testing the application:

1. Go to `http://127.0.0.1:8000/` in your web browser
2. To authenticate yourself, click on the "Login with GitHub" button
3. Give permission to authorize your GitHub account
4. After authorization you will be redirected back to the application and you will see your public starred repositories.
