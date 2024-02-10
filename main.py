from Spotify import Spotify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fastapi import FastAPI

# so that code can run in localhost
app = FastAPI()
# initialize the spotify object
spotify = Spotify()

def retrieve_songs(): 
    # get songs from billboard 100, returns as tuple (track name, artist)

    # selenium configuration
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(options=options)
    driver.get('https://www.billboard.com/charts/hot-100/')
    # array to store songs retrieved
    song_info = []
    try: 
        # wait for a song to appear to know if we can continue
        song = WebDriverWait(driver, 3).until(
            #EC.presence_of_element_located((By.ID, "title-of-a-story"))
            EC.presence_of_element_located((By.CLASS_NAME, "o-chart-results-list__item"))
        )

        # get all songs
        songs = driver.find_elements(By.CLASS_NAME, "o-chart-results-list__item")
        
        # iterate through list of songs to get name and artist
        for i in range(len(songs)): 

            if i > 200: 
                break
            try: 
                song_title = song.find_element(By.XPATH, f'/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[{i + 2}]/ul/li[4]/ul/li[1]/h3').text         
                artist = song.find_element(By.XPATH, f'/html/body/div[4]/main/div[2]/div[3]/div/div/div/div[2]/div[{i+2}]/ul/li[4]/ul/li[1]/span').text
                song_info.append((song_title, artist))
            except: 
                # ads may affect the scraping
                continue 

    finally: 

        driver.quit()
    return song_info

def get_song_uris(song_info): 
    # change song information into uri
    # returns in list form
    # array to store song uris
    song_uris = []
    for song in song_info: 

        # search song to get uri
        song_uri = spotify.searchSong(song_name=song[0], artist=song[1])
        song_uris.append(song_uri)

    return song_uris

@app.get('/{playlist_id}')
def add_songs(playlist_id: str): 

    print('Adding songs')
    
    song_info = retrieve_songs()

    song_uris = get_song_uris(song_info)

    spotify.add_to_playlist(playlist_id=playlist_id, track_uris=song_uris)

    return {'Songs added to playlist: ', playlist_id}






