import requests
import tokens
import os 
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

class Spotify: 

    url = "https://api.spotify.com/v1/"

    def __init__(self): 
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.access_token = tokens.access_token_spotify()
        self.redirect_uri = os.getenv("REDIRECT_URI")
        self.username = os.getenv("USERNAME")

    def searchArtist(self, artist_id):
         # search for artists, returns artist info
        headers = {
            'Authorization': 'Bearer ' + self.access_token
        }

        return requests.get((self.url + 'artists/' + artist_id), headers=headers).json()

      
    

    def searchSong(self, song_name: str, artist="-1"):
        # returns song uri
        headers = {
            "Authorization": "Bearer " + self.access_token
        }


        tracks = requests.get(self.url + "search/" + f"?q={song_name}%{artist}&type=track", headers=headers).json()["tracks"]["items"]
        for track in tracks: 
            song = {'name': track['name'], 'artist': track['artists'][0]['name']}

            if song_name.lower().strip(' ') == song['name'].lower().strip(): 
                # if artist was not provided
                if artist == "-1": 
                    return track['uri']
                # if artist is provided, we check 
                elif artist.lower().split()[0] == song['artist'].lower().split()[0]: 
                    return track['uri']
        
        return 'Not found'
    

    def add_to_playlist(self, playlist_id, track_uris): 
        # add songs to playlist
        # should receive track_uris as list 

        # manage security
        auth_manager = SpotifyOAuth(
            scope=['playlist-modify-public', 'playlist-modify-private'],
            username=self.username, 
            redirect_uri=self.redirect_uri, 
            client_id=self.client_id, 
            client_secret=self.client_secret

        )
        for i in range(len(track_uris)): 
            
            try: 
                sp = spotipy.Spotify(auth_manager=auth_manager)
                sp.playlist_add_items(playlist_id=playlist_id, items=[track_uris[i]])
                
            except Exception as e: 
                print(e)
                print('Failed to add song: ' + str(i))


    