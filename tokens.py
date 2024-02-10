import requests
import os 
from dotenv import load_dotenv

def access_token_spotify(): 

    load_dotenv()

    url = "https://accounts.spotify.com/api/token"

    data = {
    'grant_type': 'client_credentials',
    'client_id': os.getenv("CLIENT_ID"),
    'client_secret': os.getenv("CLIENT_SECRET")
}
    response = requests.post(url, data=data).json()

    return response['access_token']

